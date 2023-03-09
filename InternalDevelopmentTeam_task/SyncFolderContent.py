# Please implement a program in Python that synchronizes two folders: source and replica.
# The program should maintain a full, identical copy of source folder at replica folder

#Using the shutil module to copy files and directories,
#and the os module to check if a file or directory exists.
import sys
import os
import shutil
import logging

import schedule
import time
import hashlib

import argparse

class MySyncClass:

    def local_main(self, source_dir, replica_dir):#, log_filename):

        '''
        define source and replica directories
        source_dir = "/path/to/source"
        replica_dir = "/path/to/replica"
        '''
        print('SOURCE DIRECTORY:  ', source_dir)
        print('REPLICA DIRECTORY: ', replica_dir)
        logging.info('')
        logging.info('Synchronization started.')
        #logging.basicConfig(filename=log_filename, encoding='utf-8', filemode='w', level=logging.DEBUG) #will generate new log file at each run

        # check if source directory exists
        if not os.path.exists(source_dir):
            print("Source directory does not exist.")
            logging.info('Source directory does not exist.')
            exit()

        # check if replica directory exists
        if not os.path.exists(replica_dir):
            os.makedirs(replica_dir)

        # copy files and directories from source to replica
        for item in os.listdir(source_dir):
            s = os.path.join(source_dir, item)
            r = os.path.join(replica_dir, item)

            # copy file
            if os.path.isfile(s):
                replica_file = os.path.isfile(r)
                sourcefile_hash=hashlib.md5(open(s,'rb').read())

                if replica_file==True:
                    print("file:", r ,  " already exist in the target dir")
                    logging.info('this file already exist in the target dir %s', r)
                    replicafile_hash=hashlib.md5(open(r,'rb').read())
                    print("source file md5 sum:  ", sourcefile_hash.hexdigest())  # to get a printable str instead of bytes
                    print("replica file md5 sum: ", replicafile_hash.hexdigest()) # to get a printable str instead of bytes

                    if(sourcefile_hash.hexdigest()==replicafile_hash.hexdigest()):
                        print("Files in the source and replica directories are identical. Skip this file from Synchronization")
                        logging.info('Files in the source and replica directories are identical. Skip this file from Synchronization.')
                    else:
                        print("File in the replica directory is different. It will be updated with source file")
                        logging.warning('File in the replica directory is different. Replaced by the source file.')
                        shutil.copy2(s, r)
                        logging.warning('copying file %s', s)
                else:
                    print("There is no such file in the replica directory.")
                    logging.warning('There is no such file in the replica directory.')
                    shutil.copy2(s, r)
                    logging.warning('copying file %s', s)

            # copy directory
            elif os.path.isdir(s):
                shutil.copytree(s, r, symlinks=True)
                logging.info('copying directory %s', s)


        logging.info('Synchronization complete.')
        print("Synchronization complete.")



if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(prog='SyncFolderContent.py', prefix_chars='-+')
        parser.add_argument('--sd', type=str, nargs='?', help='source directory')
        parser.add_argument('--rd', type=str, nargs='?', help='replica directory')
        parser.add_argument('--sync_period', type=int, nargs='?', help='sync periodicity in seconds')
        parser.add_argument('--logfile', type=str, nargs='?', help='log filename')
        parser.add_argument('--verbosity', type=int, nargs='?', help='log verbosity level')
        parser.parse_args('--sd --rd --sync_period --logfile --verbosity'.split())
        args = parser.parse_args()

        source_dir   = args.sd
        replica_dir  = args.rd
        periodicity  = args.sync_period
        log_filename = args.logfile
        verbosity    = args.verbosity

        print('sync periodicity: ',periodicity)

        if verbosity==1:
            logging.basicConfig(filename=log_filename, encoding='utf-8', filemode='w', level=logging.INFO) #will generate new log file at each run
        elif verbosity==2:
            logging.basicConfig(filename=log_filename, encoding='utf-8', filemode='w', level=logging.DEBUG) #will generate new log file at each run
        else:
            logging.basicConfig(filename=log_filename, encoding='utf-8', filemode='w', level=logging.DEBUG) #will generate new log file at each run


        cg = MySyncClass()
        cg.local_main(source_dir, replica_dir)#, log_filename)

        # schedule the main function to run every periodicity seconds
        schedule.every(periodicity).seconds.do(cg.local_main, source_dir, replica_dir)#, log_filename)

        while True:
            # run the scheduled jobs
            schedule.run_pending()
            # wait for one second before checking again
            time.sleep(1)

    except AttributeError:
        print("--- ERROR IN : ", sys.argv[1])
        raise
