import argparse
from mpi4py import MPI


parser = argparse.ArgumentParser()
parser.add_argument('--input_file', type = str)
parser.add_argument('--merge_method', type = str)
sparser.add_argument('--test_file', type = str)

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()



if rank == 0:
    data = [(i+1)**2 for i in range(size)]
else:
    data = None
data = comm.scatter(data, root=0)