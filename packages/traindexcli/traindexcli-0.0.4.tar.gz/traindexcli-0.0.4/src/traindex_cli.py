import boto3
import argparse
from datetime import datetime

class S3Helper:

    def __init__(self):
        self.client = boto3.client("s3")
        self.s3 = boto3.resource('s3')

    def create_folder(self, path):
        path_arr = path.rstrip("/").split("/")
        if len(path_arr) == 1:
            return self.client.create_bucket(Bucket=path_arr[0])
        parent = path_arr[0]
        bucket = self.s3.Bucket(parent)
        status = bucket.put_object(Key="/".join(path_arr[1:]) + "/")
        return status


import os
import sys
import threading

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()




def main():
    parser = argparse.ArgumentParser(prog ='traindex_cli', 
                                     description ='traindex-cli program.')
    parser.add_argument('-folder','--foldername',required=True,  
                        default = False,  type=str, 
                        help ="Folder you want to create on our S3 bucket for your data.") 
    parser.add_argument('-file','--filename', required=True,
                        default = False, type=str,
                        help ='Path to the file that you want to upload to s3') 
	
    args = parser.parse_args() 

	# Creating folder

    original_filename = ""
    if "/" in args.filename:
        original_filename = args.filename.split("/")[-1]
    else:
        original_filename = args.filename

    prefix = datetime.now().ctime()
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file( args.filename, "traindex-cli", "{}/{}".format(str(prefix)+"  - "+args.foldername,original_filename),Callback=ProgressPercentage(args.filename))
    print ()
