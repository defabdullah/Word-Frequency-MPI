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
master = None
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
worker_num = size-1

master = Master(worker_num)
if rank == 0:
    data = master.even_distributed_data(args.input_file)
else:
    data = None

data = comm.scatter(data)

## Burada her worker datayı aldı
method = parse_args().merge_method
if rank==0:
    #print("rank:",rank,"number of sentences:",len(data))
    if method == "MASTER":
        unigram_count, bigram_count = master.receive_and_merge_master()
    else:
        unigram_count, bigram_count = master.receive_and_merge_worker()
    print(f'unigram count: {unigram_count}', f'bigram count: {bigram_count}', sep="\n")
    #pass
else:
    worker = Worker(data,args.merge_method, master, rank)
    print("rank:",worker.rank,"number of sentences:",len(worker.data))
    #print(data)
    worker.merge()

