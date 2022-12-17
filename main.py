import argparse
from mpi4py import MPI

from master import Master
from worker import Worker

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type = str)
    parser.add_argument('--merge_method', type = str)
    parser.add_argument('--test_file', type = str)
    args=parser.parse_args()
    return args

args=parse_args()

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
worker_num = size-1

if rank == 0:
    master = Master(worker_num)
    data = master.even_distributed_data(args.input_file)
else:
    data = None

data = comm.scatter(data)

## Burada her worker datayı aldı

if rank==0:
    pass
else:
    print("rank:",rank,"number of sentences:",len(data))
    worker = Worker(data,args.merge_method)
    worker.merge()
