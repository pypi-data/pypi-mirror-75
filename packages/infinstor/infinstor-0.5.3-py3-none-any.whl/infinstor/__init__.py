import sys
import os
import io
import boto3
from io import StringIO
from multiprocessing.connection import wait
from multiprocessing import Process, Pipe, Queue
from queue import Empty
import pandas as pd
from pandas import DataFrame
from tqdm import tqdm
import ast
import subprocess
import tempfile
import pickle
from . import infin_ast
from datetime import datetime, timedelta
import time
from mlflow import start_run, end_run, log_metric, log_param, log_artifacts, set_experiment
from os.path import sep
import mlflow.projects
from contextlib import contextmanager,redirect_stderr,redirect_stdout
import pprint
import types

# import astpretty

TRANSFORM_RAW_PD = "infin_transform_raw_to_pd"
TRANSFORM_RAW_DS = "infin_transform_raw_to_ds"
TRANSFORM_CSV_PD = "infin_transform_csv_to_pd"
TRANSFORM_CSV_DS = "infin_transform_csv_to_ds"
TRANSFORM_ONE_OBJ = "infin_transform_one_object"

verbose = False

def num_threads():
    return 8

class FuncLister(ast.NodeVisitor):
    def __init__(self, glbs):
        self.glbs = glbs;

    def visit_FunctionDef(self, node):
        self.glbs[node.name] = "'" + node.name + "'";
        # print('>> Funclister: ' + node.name)
        self.generic_visit(node)

# fills out array_of_files with all the files in this prefix
def list_one_dir(client, bucket, prefix_in, recurse, array_of_files):
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix_in, Delimiter="/")
    for page in page_iterator:

        # print('Files:')
        contents = page.get('Contents')
        if (contents != None):
            # print('   ' + str(contents))
            count = 0;
            for one_content in contents:
                object_name = one_content['Key']
                full_object_name = object_name
                # print(full_object_name)
                array_of_files.append(full_object_name)
                count += 1
            if (count > 0):
                print(str(count) + " files in " + prefix_in)

        # print('Directories:')
        common_prefixes = page.get('CommonPrefixes')
        if (common_prefixes != None):
            for prefix in common_prefixes:
                this_prefix = str(prefix['Prefix'])
                # print('   ' + this_prefix)
                if (bool(recurse) and this_prefix != None ):
                    list_one_dir(client, bucket, this_prefix, recurse, array_of_files)

# returns parentdir (with no leading or trailing /) and filename
def get_parent_dir_and_fn(full_object_key):
    components = full_object_key.split(sep)
    parentdir = ''
    for comp in components[0:len(components) -1]:
        if (parentdir == ''):
            parentdir = comp
        else:
            parentdir = parentdir + sep + comp
    return parentdir, components[len(components) - 1]

# fills out dict_of_arrays_of_files with a dict of parentdir -> array_of_files_in_parent_dir
def list_dir_by_dir(client, bucket, prefix_in, recurse, dict_of_arrays_of_files):
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix_in, Delimiter="/")
    for page in page_iterator:

        # print('Files:')
        contents = page.get('Contents')
        if (contents != None):
            # print('   ' + str(contents))
            count = 0;
            for one_content in contents:
                object_name = one_content['Key']
                full_object_name = object_name
                # print(full_object_name)
                parent_dir, filename = get_parent_dir_and_fn(object_name)
                if (parent_dir in dict_of_arrays_of_files):
                    files_in_this_dir = dict_of_arrays_of_files[parent_dir]
                else:
                    files_in_this_dir = []
                    dict_of_arrays_of_files[parent_dir] = files_in_this_dir
                files_in_this_dir.append(filename)
                count += 1
            if (count > 0):
                print(str(count) + " files in " + prefix_in)

        # print('Directories:')
        common_prefixes = page.get('CommonPrefixes')
        if (common_prefixes != None):
            for prefix in common_prefixes:
                this_prefix = str(prefix['Prefix'])
                # print('   ' + this_prefix)
                if (bool(recurse) and this_prefix != None ):
                    list_dir_by_dir(client, bucket, this_prefix, recurse, dict_of_arrays_of_files)

def info(msg):
    now = datetime.now()
    print(__name__ + '[' + str(os.getpid()) + '][' + now.strftime('%Y-%m-%d %H:%M:%S') + ']' + msg)

class download_task:
    def __init__(self, command, bucketname, parentdir, filename):
        self.command = command
        self.bucketname = bucketname
        self.parentdir = parentdir
        self.filename = filename

def s3downloader(download_task_q, write_pipe, endpoint, glb):
    # info('s3downloader: started. endpoint=' + endpoint)

    if (glb != None):
        namespaced_infin_transform_one_object =\
                namespaced_function(glb['infin_transform_one_object'], glb, None, True)

    session = boto3.session.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)
    while (True):
        try:
            if (verbose == True):
                start = datetime.now()
            download_task = download_task_q.get()
            if (verbose == True):
                end = datetime.now()
                td = end - start
                ms = (td.days * 86400000) + (td.seconds * 1000) + (td.microseconds / 1000)
                if (ms > 10):
                    info('s3downloader: q.get took ' + str(ms) + ' ms')
        except Empty as e:
            info('s3downloader: No more entries in download_task_q. Exiting..')
            write_pipe.close()
            break
        op = download_task.command
        if (op == 'download'):
            bucketname = download_task.bucketname
            parentdir = download_task.parentdir
            filename = download_task.filename
            if (parentdir == ''):
                full_object_key = filename
            else:
                full_object_key = parentdir + sep + filename
            if (verbose == True):
                info('s3downloader: starting download of ' + full_object_key\
                        + ' from ' + bucketname)
                start = datetime.now()
            obj = client.get_object(Bucket=bucketname, Key=full_object_key)
            content_length = obj['ContentLength']
            if (verbose == True):
                end = datetime.now()
                info('s3downloader: finished download of ' + full_object_key\
                        + ' from ' + bucketname)
                td = end - start
                ms = (td.days * 86400000) + (td.seconds * 1000) + (td.microseconds / 1000)
                if (ms > 500):
                    info('s3downloader: download of size ' + str(content_length) + ' took '\
                        + str(ms) + ' ms')

            strbody = obj['Body']
            dtm = obj['LastModified']
            bts = strbody.read()
            key = dtm.strftime('%Y-%m-%d %H:%M:%S') + ' ' + bucketname + '/' + full_object_key
            if (glb == None):
                if (not write_pipe.writable):
                    info('s3downloader: WARNING write pipe not writable')
                    time.sleep(1)
                try:
                    write_pipe.send(key)
                    write_pipe.send(bts)
                except Exception as e:
                    status_str = str(e)
                    info("Error sending bytes back: " + status_str)
            else:
                try:
                    namespaced_infin_transform_one_object(bucketname, parentdir, filename, bts)
                except Exception as e:
                    status_str = str(e)
                    info("Error executing infin_transform_one_object: " + status_str)
                else:
                    status_str = 'Success'
                write_pipe.send(key)
                write_pipe.send(status_str)
        elif (op == 'quit'):
            # info('s3downloader: Received quit')
            write_pipe.close()
            break
        else:
            info('s3downloader: Unknown command ' + op)
            write_pipe.close()
            break

def namespaced_function(function, global_dict, defaults=None, preserve_context=False):
    '''
    Redefine (clone) a function under a different globals() namespace scope
        preserve_context:
            Allow keeping the context taken from orignal namespace,
            and extend it with globals() taken from
            new targetted namespace.
    '''
    if defaults is None:
        defaults = function.__defaults__

    if preserve_context:
        _global_dict = function.__globals__.copy()
        _global_dict.update(global_dict)
        global_dict = _global_dict
    new_namespaced_function = types.FunctionType(
        function.__code__,
        global_dict,
        name=function.__name__,
        argdefs=defaults,
        closure=function.__closure__
    )
    new_namespaced_function.__dict__.update(function.__dict__)
    return new_namespaced_function

def load_one_csv_from_bytearray(bts):
    s = str(bts, 'utf-8')
    sio = StringIO(s)
    return pd.read_csv(sio)

def download_objects(endpoint, bucketname, parentdir, array_of_files, is_csv, glb):
    try:
        start_run()
        return download_objects_inner(endpoint, bucketname, parentdir, array_of_files, is_csv, None)
    finally:
        end_run()

# returns a pandas DataFrame with index 'YY-MM-dd HH:MM:SS bucketname/filename'
# and one column named RawBytes that contains the raw bytes from the object
# This inner method is called after the outer method wraps in mlflow start_run
def download_objects_inner(endpoint, bucketname, parentdir, array_of_files, is_csv, glb):
    log_param("object_count", len(array_of_files))

    command_q = Queue(len(array_of_files) + num_threads())
    for onefile in array_of_files:
        command_q.put(download_task('download', bucketname, parentdir, onefile))
    for i in range(num_threads()):
        command_q.put(download_task('quit', '', '', ''))

    pipe_from_child = []
    processes = []
    for i in range(num_threads()):
        r1, w1 = Pipe(False)
        pipe_from_child.append(r1)
        p = Process(target=s3downloader, args=(command_q, w1, endpoint, glb,))
        p.start()
        processes.append(p)
        w1.close()

    filebytes = []
    filekeys = []
    step = 0
    with tqdm(total=len(array_of_files)) as pbar:
        files_read = 0
        while pipe_from_child:
            ready = wait(pipe_from_child, timeout=10)
            for read_pipe in pipe_from_child:
                try:
                    while (read_pipe.poll()):
                        key = read_pipe.recv()
                        bts = read_pipe.recv()
                        filekeys.append(key)
                        filebytes.append(bts)
                        pbar.update(1)
                        files_read += 1
                        if ((files_read % 10) == 0):
                            log_metric("downloaded", files_read, step=step)
                            step += 1
                except EOFError:
                    pipe_from_child.remove(read_pipe)

    for i in range(num_threads()):
        processes[i].join()
    if (is_csv == True):
        rv = pd.concat(map(load_one_csv_from_bytearray, filebytes))
    else:
        data = {'RawBytes': filebytes}
        rv = DataFrame(data, index=filekeys)
    log_metric("downloaded", files_read, step=step)
    return rv

def actually_run_transformation(client, endpoint, cache_path, is_pandas_df, bucketname,\
        prefix_in, is_csv, xformname):
    xform_obj = client.get_object(Bucket='infinstor-pseudo-bucket', Key='transforms/' + xformname)
    strbody = xform_obj['Body']
    bts = strbody.read()
    s = str(bts, 'utf-8')
    # print(s)

    array_of_files = []
    list_one_dir(client, bucketname, prefix_in, True, array_of_files)
    print('Total Number Of Objects: ' + str(len(array_of_files)))
    try:
        start_run()
        objects = download_objects_inner(endpoint, bucketname, '', array_of_files, is_csv, None)
    finally:
        end_run()

    transformAst = infin_ast.extract_transform(TRANSFORM_RAW_PD, src_str=s)
    # XXX we should use the following statement to figure out what
    # kind of an object the infin_transform function returns
    # infin_ast.add_type_statements(transformAst)
    transformSrc = infin_ast.get_source(transformAst)

    if (verbose == True):
        print('transformSrc=' + transformSrc);

    if (is_csv):
        if (is_pandas_df):
            xn = TRANSFORM_CSV_PD
        else:
            xn = TRANSFORM_CSV_DS
    else:
        if (is_pandas_df):
            xn = TRANSFORM_RAW_PD
        else:
            xn = TRANSFORM_RAW_DS

    transformSrc = transformSrc + "\n" + xn + "(objects)\n"

    tree = ast.parse(transformSrc)
    # Add all functions in xformcode to the globals dictionary
    glb = {}
    fl = FuncLister(glb)
    fl.visit(tree)
    glb['objects'] = objects;
    #astpretty.pprint(tree)
    compliedcode = compile(tree, "<string>", "exec")
    exec(compliedcode, glb)
    # save result of transformation in cache
    if (is_pandas_df == True):
        fd, tmpf_name = tempfile.mkstemp(suffix='.pkl')
        os.close(fd)
        objects.to_pickle(tmpf_name)
        client.put_object(Body=open(tmpf_name, 'rb'), Bucket='infinstor-pseudo-bucket',\
                Key=cache_path)
        os.remove(tmpf_name)
    else:
        print('saving tf.data.Dataset unimplemented')
    return objects

def read_raw_and_xform_to_pd(time_spec, service_name, bucketname, prefix_in, is_csv, xformname):
    endpoint = "https://" + time_spec + ".s3proxy." + service_name + ".com:443/";
    session = boto3.session.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)

    # check if we can download a cached version
    cache_path = 'cache/' + xformname + '/' + time_spec + '/'\
            + bucketname + '/' + prefix_in + 'pd.DataFrame'
    print('Looking up cache entry ' + cache_path)
    try:
        s3obj = client.get_object(Bucket='infinstor-pseudo-bucket', Key=cache_path)
        print('cache hit for ' + cache_path)
        body_bytes = s3obj['Body'].read()
        cached_obj = pickle.loads(body_bytes)
    except client.exceptions.NoSuchKey:
        print('cache miss for ' + cache_path)
        cached_obj = actually_run_transformation(client, endpoint, cache_path, True,\
                bucketname, prefix_in, is_csv, xformname)
    finally:
        return cached_obj

def read_raw_and_xform_to_ds(time_spec, service_name, bucketname, prefix_in, is_csv, xformname):
    endpoint = "https://" + time_spec + ".s3proxy." + service_name + ".com:443/";
    session = boto3.session.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)

    # check if we can download a cached version
    cache_path = 'cache/' + xformname + '/' + time_spec + '/'\
            + bucketname + '/' + prefix_in + 'tf.data.Dataset'
    print('Looking up cache entry ' + cache_path)
    try:
        cached_obj = client.get_object(Bucket='infinstor-pseudo-bucket', Key=cache_path)
        print('cache hit for ' + cache_path)
        # XXX read and deserialize here
    except client.exceptions.NoSuchKey:
        print('cache miss for ' + cache_path)
        cached_obj = actually_run_transformation(client, endpoint, cache_path, False,\
                bucketname, prefix_in, is_csv, xformname)
    finally:
        return cached_obj

def run_xform_periodically(seconds, service_name, bucketname, prefix_in, xformname):
    while (True):
        start_time = datetime.utcnow()
        time.sleep(seconds)
        end_time = datetime.utcnow()
        time_spec = 'tm' + start_time.strftime("%Y%m%d%H%M%S")\
                + '-tm' + end_time.strftime("%Y%m%d%H%M%S")
        read_raw_and_xform_to_pd(time_spec, service_name, bucketname, prefix_in, False, xformname)

def read_raw_and_xform_one_object(time_spec, service_name, bucketname,\
        prefix_in, xformname):
    endpoint = "https://" + time_spec + ".s3proxy." + service_name + ".com:443/";
    session = boto3.session.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)

    xform_obj = client.get_object(Bucket='infinstor-pseudo-bucket', Key='transforms/' + xformname)
    strbody = xform_obj['Body']
    bts = strbody.read()
    s = str(bts, 'utf-8')
    # print(s)

    transformAst = infin_ast.extract_transform(TRANSFORM_ONE_OBJ, src_str=s)
    transformSrc = infin_ast.get_source(transformAst)
    # transformSrc = transformSrc + "\ninfin_transform_one_object(bucket, key, object_bytes)\n"
    tree = ast.parse(transformSrc)
    # astpretty.pprint(tree)
    compiledcode1 = compile(tree, "<string>", "exec")

    dict_of_arrays_of_files = dict()
    list_dir_by_dir(client, bucketname, prefix_in, True, dict_of_arrays_of_files)
    try:
        start_run()
        for parentdir in dict_of_arrays_of_files:
            array_of_files = dict_of_arrays_of_files[parentdir]
            info('Number Of Objects in parentdir ' + parentdir + ' = ' + str(len(array_of_files)))
            # Add all functions in xformcode to the globals dictionary
            glb = {}
            fl = FuncLister(glb)
            fl.visit(tree)
            try:
                exec(compiledcode1, glb)
            except Exception as e:
                status_str = str(e)
            else:
                status_str = 'Success'
            # print('Globals=')
            # pprint.pprint(glb)
            info("Execution of global statics for parentdir " + parentdir\
                    + " complete. status_str=" + status_str)
            objects = download_objects_inner(endpoint, bucketname, parentdir, array_of_files,\
                    False, glb)
    finally:
        end_run()
    return objects

def look_for_transform(transform_string, transform_symbol):
    transformAst = infin_ast.extract_transform(transform_symbol, src_str=transform_string)
    transformSrc = infin_ast.get_source(transformAst)
    if (verbose == True):
        print('transformSrc=' + transformSrc);
    tree = ast.parse(transformSrc)
    glb = {}
    fl = FuncLister(glb)
    fl.visit(tree)
    for key, value in glb.items():
        if (key == transform_symbol):
            return True
    return False

def run_transform_inline(time_spec, service_name, bucketname, prefix_in, xformname):
    endpoint = "https://" + time_spec + ".s3proxy." + service_name + ".com:443/";
    print('infinstor proxy endpoint=' + endpoint)
    session = boto3.session.Session(profile_name='infinstor')
    client = session.client('s3', endpoint_url=endpoint)

    xform_obj = client.get_object(Bucket='infinstor-pseudo-bucket', Key='transforms/' + xformname)
    strbody = xform_obj['Body']
    bts = strbody.read()
    transform_string = str(bts, 'utf-8')
    # print(s)

    if (look_for_transform(transform_string, TRANSFORM_RAW_PD)):
        return read_raw_and_xform_to_pd(time_spec, service_name, bucketname, prefix_in, False, xformname)
    elif (look_for_transform(transform_string, TRANSFORM_RAW_DS)):
        return read_raw_and_xform_to_ds(time_spec, service_name, bucketname, prefix_in, False, xformname)
    elif (look_for_transform(transform_string, TRANSFORM_CSV_PD)):
        return read_raw_and_xform_to_pd(time_spec, service_name, bucketname, prefix_in, True, xformname)
    elif (look_for_transform(transform_string, TRANSFORM_CSV_DS)):
        return read_raw_and_xform_to_ds(time_spec, service_name, bucketname, prefix_in, True, xformname)
    elif (look_for_transform(transform_string, TRANSFORM_ONE_OBJ)):
        return read_raw_and_xform_one_object(time_spec, service_name, bucketname, prefix_in, xformname)
    else:
        raise Exception("Cannot find a known transform function");

def run_transform_singlevm(time_spec, service_name, bucketname, prefix_in, xformname):
    # save the conda environment
    projdir = tempfile.mkdtemp()
    print('Project dir: ' + projdir)
    condayaml = os.open(projdir + sep + 'conda.yaml', os.O_CREAT|os.O_WRONLY, mode=0o644)
    cmd = ['conda', 'env', 'export', '--no-builds']
    print('Running cmd:')
    print(*cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,\
                stdin=subprocess.DEVNULL, close_fds=True)
    for line in process.stdout:
        os.write(condayaml, line)
    process.wait()

    with open(projdir + sep + 'MLproject', "w") as projfile:
        projfile.write('Name: run-' + xformname + '\n')
        projfile.write('conda_env: conda.yaml\n')
        projfile.write('\n')
        projfile.write('entry_points:' + '\n')
        projfile.write('  main:' + '\n')
        projfile.write('    parameters:\n')
        projfile.write('      timespec: string\n')
        projfile.write('      service: string\n')
        projfile.write('      bucket: string\n')
        projfile.write('      prefix: string\n')
        projfile.write('      xformname: string\n')
        projfile.write('    command: "python -c \'from infinstor import mlflow_run; mlflow_run.main()\'\
                    --timespec={timespec} --service={service}\
                    --bucket={bucket} --prefix={prefix} --xformname={xformname}"\n')

    child_env = os.environ.copy()
    child_env['MLFLOW_TRACKING_URI'] = 'infinstor://' + service_name + '/'
    cmd = ['mlflow', 'run', '-b', 'infinstor-backend', projdir,\
            '-P', 'timespec=' + time_spec,\
            '-P', 'service=' + service_name,\
            '-P', 'bucket=' + bucketname,\
            '-P', 'prefix=' + prefix_in,\
            '-P', 'xformname=' + xformname ]
    print('Running cmd:')
    print(*cmd)
    process = subprocess.Popen(cmd, env=child_env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,\
            stdin=subprocess.DEVNULL, close_fds=True)
    for line in process.stdout:
        print(line.decode('utf-8'))
    process.wait()

    return None

def run_transform_emr(time_spec, service_name, bucketname, prefix_in, xformname):
    print('Error: Unimplemented')
    return None

def run_transform(time_spec, service_name, bucketname, prefix_in, xformname, run_location):
    if (run_location == "inline"):
        return run_transform_inline(time_spec, service_name, bucketname, prefix_in, xformname)
    elif (run_location == "singlevm"):
        return run_transform_singlevm(time_spec, service_name, bucketname, prefix_in, xformname)
    elif (run_location == "emr"):
        return run_transform_emr(time_spec, service_name, bucketname, prefix_in, xformname)
