#!/usr/bin/env python3
# -.- coding: utf-8 -.-
"""Parallelism abstractions within AWS Lambda.

> Due to the Lambda execution environment not having /dev/shm 
(shared memory for processes) support, you can’t use multiprocessing.Queue or 
multiprocessing.Pool.
(https://aws.amazon.com/blogs/compute/parallel-processing-in-python-with-aws-lambda/)

NOTE:  This module is redundant with the mirrored API module.  Need some 
       internal package manager.

Includes:

Non-daemon process spawning.

Circumnavigates Python preventing daemon processes from spawning 
subprocesses.
"""

from multiprocessing import Process, Pipe
import multiprocessing
import multiprocessing.pool
import time

__copyright__ = 'Copyright © 2020 Omic'

CPU_COUNT = multiprocessing.cpu_count()
PROCESS_CAP = 30

class Counter(object):
    def __init__(self, initval=0):
        self.val = multiprocessing.Value('i', initval)
        self.lock = multiprocessing.Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def value(self):
        with self.lock:
            return self.val.value

class NoDaemonProcess(multiprocessing.Process):
    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass

class NoDaemonContext(type(multiprocessing.get_context())):
    Process = NoDaemonProcess

# Source:  https://stackoverflow.com/questions/6974695/
#          python-process-pool-non-daemonic.
class NoDaemonPool(multiprocessing.pool.Pool):
    def __init__(self, *args, **kwargs):
        if 'cpu_count' in kwargs:
            args = [kwargs['cpu_count']] + list(args)
            del kwargs['cpu_count']
        else:
            args = [CPU_COUNT] + list(args)
        kwargs['context'] = NoDaemonContext()
        super(NoDaemonPool, self).__init__(*args, **kwargs)

    def kind_map(self, func, iterable, chunksize=None):
        # TODO:  Help with processing spawning issue.  OS prevents too many
        #        processes from spawning.
        return super().map(func, iterable)

# -------------------------------------------------------

def _worker(conn, func):
    """Finds total size of the EBS volumes attached to an EC2 instance.
    """
    output = func()
    conn.send(output)
    conn.close()

def _run_parallel_batch(batch):
    # create a list to keep all processes
    processes = []
    # create a list to keep connections
    parent_connections = []
    for func in batch:
        # create a pipe for communication
        parent_conn, child_conn = Pipe()
        parent_connections.append(parent_conn)
        # create the process, pass instance and connection
        process = Process(target=_worker, args=(child_conn, func,))
        processes.append(process)
    # start all processes
    for process in processes:
        process.start()
    # make sure that all processes have finished
    for process in processes:
        process.join()
    payloads = []
    for parent_connection in parent_connections:
        payloads.append(parent_connection.recv())
    return payloads

def run_parallel(workload: list, batch_size: int = None) -> list:
    """..."""
    batch_size = batch_size if batch_size else len(workload)
    assert len(workload) > 0 and batch_size > 2, \
           'What is the point of what you are doing?'
    batch = []
    payloads = []
    for i, func in enumerate(workload):            
        batch.append(func)
        if len(batch) == batch_size or i == len(workload) - 1:
            # Run and clear batch if full or workload is near done.
            payloads.extend(_run_parallel_batch(batch))
            batch = []
    return payloads

if __name__ == '__main__':
    _start = time.time()
    func = lambda: print('func:', 'ok')
    workload = [func] * 10
    total = run_parallel(workload)
    print("Total volume size: %s GB" % total)
    print("Sequential execution time: %s seconds" % (time.time() - _start))