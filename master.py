from mpi4py import MPI

class Master():
    def __init__(self,worker_num):
        self.worker_num=worker_num
        self.comm = MPI.COMM_WORLD
    
    def even_distributed_data(self,input_file):
        with open(input_file) as file:
            lines = [line.rstrip() for line in file]
        num_lines=len(lines)
        min_count = num_lines // self.worker_num
        remainder = num_lines % self.worker_num
        data=[[]]
        for i in range(self.worker_num):
            if (i < remainder):
                start = i * (min_count + 1)
                stop = start + min_count
            else:
                start = i * min_count + remainder
                stop = start + (min_count - 1)
            data.append(lines[start:stop+1])
        return data
    
    def receive_and_merge_master(self):
        unigram_arr = []
        bigram_arr = []
        unigram_count = 0
        bigram_count = 0
        for i in range(1, self.worker_num + 1):
            unigrams = self.comm.recv(source = i, tag = 11)
            bigrams = self.comm.recv(source = i, tag = 12)
            unigram_arr.extend(unigrams)
            bigram_arr.extend(bigrams)
        #print(unigram_arr)
        #print(bigram_arr)
        for j in unigram_arr:
            unigram_count += j
        for k in bigram_arr:
            bigram_count += k
        return unigram_count, bigram_count
    
    def receive_and_merge_worker(self):
        unigram_arr = self.comm.recv(source = self.worker_num, tag = 11)
        bigram_arr = self.comm.recv(source = self.worker_num, tag = 12)
        unigram_count = 0
        bigram_count = 0
        for j in unigram_arr:
            unigram_count += j
        for k in bigram_arr:
            bigram_count += k
        return unigram_count, bigram_count