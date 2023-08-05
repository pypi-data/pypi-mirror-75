'''Utility funcs and wrappers related to read and writing files and OS input / output (osio)'''
import json
import os
from contextlib import contextmanager
from threading  import Lock
import concurrent.futures
import logging
# FILE IO

def make_dir(path):
    '''Makes a dir at path if it does not exist, otherwise does nothing'''
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    # other errors
    except Exception as e:
        raise e

def list_files(path):
    '''Returns a list of all the files at path, excludes directories'''
    files = [file for file in sorted(os.listdir(path)) if not os.path.isdir(os.path.join(path,file))]
    return files

def list_dirs(path):
    '''Returns a list of all the directories at path, excludes files'''
    dirs = [d for d in sorted(os.listdir(path)) if os.path.isdir(os.path.join(path, d))]
    return dirs


def write_json(dictionary, filename):
    '''Writes a dictionary to json'''
    with open(filename,'w+') as f:
        json.dump(dictionary, f)

def read_json(filename):
    '''Reads a json file and returns a dictionary
    returns an empty dict if the file is not found'''
    try:
        with open(filename,'r') as f:
            users = json.load(f)
            return users
    # on not found return an empty dict
    except FileNotFoundError:
        print(f'"{filename}" not found, returning an empty dictionary')
        return {}

class RWLock(object):
    """
     Read-write lock. Taken from https://gist.github.com/tylerneylon/a7ff6017b7a1f9a506cf75aa23eacfd6

     RWLock class; this is meant to allow an object to be read from by
        multiple threads, but only written to by a single thread at a time. See:
        https://en.wikipedia.org/wiki/Readers%E2%80%93writer_lock

        Usage:

            from rwlock import RWLock

            my_obj_rwlock = RWLock()

            # When reading from my_obj:
            with my_obj_rwlock.r_locked():
                do_read_only_things_with(my_obj)

            # When writing to my_obj:
            with my_obj_rwlock.w_locked():
                mutate(my_obj)
    """

    def __init__(self):

        self.w_lock = Lock()
        self.num_r_lock = Lock()
        self.num_r = 0

    # ___________________________________________________________________
    # Reading methods.

    def r_acquire(self):
        self.num_r_lock.acquire()
        self.num_r += 1
        if self.num_r == 1:
            self.w_lock.acquire()
        self.num_r_lock.release()

    def r_release(self):
        assert self.num_r > 0
        self.num_r_lock.acquire()
        self.num_r -= 1
        if self.num_r == 0:
            self.w_lock.release()
        self.num_r_lock.release()

    @contextmanager
    def r_locked(self):
        """ This method is designed to be used via the `with` statement. """
        try:
            self.r_acquire()
            yield
        finally:
            self.r_release()

    # ___________________________________________________________________
    # Writing methods.

    def w_acquire(self):
        self.w_lock.acquire()

    def w_release(self):
        self.w_lock.release()

    @contextmanager
    def w_locked(self):
        """ This method is designed to be used via the `with` statement. """
        try:
            self.w_acquire()
            yield
        finally:
            self.w_release()


def execute_func_by_pool(func, list_of_args, max_workers=20,timeout=None, logging=True,verbose=True):
    '''Executes the func on list_of_args using a threadpool. Does not '''

    if logging:
        make_dir('logs')
        logging.basicConfig(filename=f'logs/{func.__name__}.log')


    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        jobs = len(list_of_args)
        jobs_processed = 0
        futures = [pool.submit(func, arg) for arg in list_of_args]
        for f in concurrent.futures.as_completed(futures):
            try:
                f.result(timeout=timeout)
            except Exception as e:
                if logging:
                    logging.exception(e, f)
            finally:
                jobs_processed += 1
                if verbose:
                    print(f'{func.__name__} : {jobs_processed}/{jobs}')

    pool.shutdown(wait=True)
