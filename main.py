import argparse
from mpi4py import MPI

from master import Master
from worker import Worker

def parse_args(): #parse the arguments. they will be used for some checkings like master method name etc.
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

method = parse_args().merge_method
if rank==0: #call merge methods corresponing to the method argument and outputs the results.
    if method == "MASTER":
        unigram_count, bigram_count = master.receive_and_merge_master()
    else:
        unigram_count, bigram_count = master.receive_and_merge_worker()
    print(f'unigram count: {unigram_count}', f'bigram count: {bigram_count}', sep="\n")
    master.calculate_bigram_probability(args.test_file)
else:
    worker = Worker(data,args.merge_method, master, rank)
    print("rank:",worker.rank,"number of sentences:",len(worker.data))
    worker.merge()