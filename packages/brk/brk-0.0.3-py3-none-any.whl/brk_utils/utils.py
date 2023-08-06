import json
import random
import re
import string
import datetime

from threading import Lock
import os
import time
import threading





ISO_LIKE_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
microsecond_dateformat = "%Y-%m-%d %H:%M:%S.%f"
__file_locks = {}

def get_all_combinations_lower_case(combination_length:int):
    if combination_length < 1:
        return []
    if combination_length > 4:
        raise Exception("Can't produce string combinations of length greater than 4")
    if combination_length == 1:
        return [chr(x + ord('a')) for x in range(26)]
    else:
        l = []
        for combination in get_all_combinations_lower_case(combination_length - 1):
            for x in range(26):
                l.append(combination + chr(ord('a') + x))
        return l



import traceback
def log_exception(filepath):
    append_string_to_file(datetime.datetime.now().strftime(ISO_LIKE_DATE_FORMAT) + " : " + str(traceback.format_exc()),filepath)

def log(filepath,line):
    append_string_to_file(datetime.datetime.now().strftime(ISO_LIKE_DATE_FORMAT) + " : " + line,
                          filepath)

def read_file(filepath):
    with open(filepath,"r") as f:
        content = f.read()
    return content


def thread_start(func,is_background:bool,*args):
    thread = threading.Thread(target=func, args=args)
    thread.daemon = is_background  # Daemonize thread
    thread.start()

def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

__file_write_queue = []
__file_write_queue_lock = Lock()
def file_write_thread():
    while True:
        __file_write_queue_lock.acquire()
        if len(__file_write_queue) > 0:
            item = __file_write_queue.pop(0)
            __file_write_queue_lock.release()
            filepath = item[0]
            line = item[1]
            f = open(filepath,"a")
            f.write(line + "\n")
            f.close()
        else:
            __file_write_queue_lock.release()
            time.sleep(2)

def append_string_to_file(filepath:str,line:str):
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.mkdir(directory)
    __file_write_queue_lock.acquire()
    __file_write_queue.append((filepath,line))
    __file_write_queue_lock.release()
thread_start(file_write_thread,True)






