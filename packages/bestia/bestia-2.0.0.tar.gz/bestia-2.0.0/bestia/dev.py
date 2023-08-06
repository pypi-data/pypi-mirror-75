# USE THIS MODULE TO TEST LIBRARY API BEFORE COMMITING/UPLOADING
import os, sys
from time import sleep

# DIRECTLY IMPORT SAME DIR MODULES
#   , NOT BESTIA INSTALLED MODULES
from connect import *
from proc import *
from error import *
from iterate import *
from misc import *
from output import *

from multiprocessing import Pool

def do_this(count):
    color = LoopedList(
        'red', 'blue', 'yellow', 'magenta', 'cyan'
    )
    for n in range(count):
        echo(n, color[n])
        sleep(1)

if __name__ == "__main__":

    # print(
    #     read_cmd(
    #         '/bin/hostname', 
    #         buffer_size=123,
    #     )[0].decode()
    # )

    pool = Pool(
        processes=2
    )

    pool.apply_async(do_this, args=[8], callback=None)
    pool.close() # Prevents any more tasks from being submitted to the pool. Once all the tasks have been completed the worker processes will exit.
    sleep(3)
    echo('waiting', 'blue')
    pool.join() # 

    pool.terminate() # Stops the worker processes immediately without completing outstanding work
    echo('DONE', 'red')
