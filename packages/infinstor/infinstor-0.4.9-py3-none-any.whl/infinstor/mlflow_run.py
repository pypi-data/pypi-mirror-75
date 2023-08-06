import sys
import argparse
from . import run_transform_inline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--timespec', help='InfinSnap/InfinSlice time specification')
    parser.add_argument('--service', help='infinstor|isstage?|isdemo?')
    parser.add_argument('--bucket', help='bucket name')
    parser.add_argument('--prefix', help='path in bucket')
    parser.add_argument('--xformname', help='name of transformation')
    args = parser.parse_args()
    return run_transform_inline(args.timespec, args.service, args.bucket, args.prefix, args.xformname)

if __name__ == "__main__":
    main()
