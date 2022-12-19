from mpi4py import MPI

class Master():
    def __init__(self,worker_num):
        self.worker_num=worker_num
        self.comm = MPI.COMM_WORLD
        self.unigrams = None
        self.bigrams = None
    
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
        unigram_dict = dict()
        bigram_dict = dict()
        for i in range(1, self.worker_num + 1):
            unigrams = self.comm.recv(source = i, tag = 11)
            bigrams = self.comm.recv(source = i, tag = 12)
            for unigram in unigrams.keys():
                if unigram not in unigram_dict:
                    unigram_dict[unigram]=0
                unigram_dict[unigram]+=unigrams[unigram]
                
            for bigram in bigrams.keys():
                if bigram not in bigram_dict:
                    bigram_dict[bigram]=0
                bigram_dict[bigram]+=bigrams[bigram]
                
        self.unigrams = unigram_dict
        self.bigrams = bigram_dict
        return sum(unigram_dict.values()),sum(bigram_dict.values())
    
    def receive_and_merge_worker(self):
        unigram_dict = self.comm.recv(source = self.worker_num, tag = 11)
        bigram_dict = self.comm.recv(source = self.worker_num, tag = 12)
        self.unigrams = unigram_dict
        self.bigrams = bigram_dict
        return sum(unigram_dict.values()),sum(bigram_dict.values())

    def calculate_bigram_probability(self,test_file):
        with open(test_file) as file:
            lines = [line.rstrip() for line in file]
        for line in lines:
            probability=0
            first, second=line.split()
            bigram = first + " " + second
            if bigram in self.bigrams:
                probability = self.bigrams[bigram] / self.unigrams[first]
            print(f'The conditional probability of bigram {bigram} is {probability}')