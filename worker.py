from mpi4py import MPI



class Worker():
    def __init__(self,data,merge_method, master, rank):
        self.data=data
        self.merge_method=merge_method
        self.master = master
        self.rank = rank
        self.comm = MPI.COMM_WORLD
        
    def unigram_counter(self, data):
        res = list()
        count_res = list()
        for d in data:
            d = d.split()
            res.append(d)
            count_res.append(len(d))
        return res, count_res

    def bigram_counter(self, data):
        res = list()
        count_res = list()
        for d in data:
            tmp = list()
            d = d.split()
            for i in range(len(d) - 1):
                tmp.append(d[i:i+2])
            res.append(tmp)
            count_res.append(len(tmp))
        return res, count_res
    
    def master_unigram_counter(self, data):
        _, count_res = self.unigram_counter(data)
        #print(res)
        #return res
        #print(count_res)
        #return count_res
        self.comm.send(count_res, dest=0, tag=11)
        #print("sent unigrams")
        
    def master_bigram_counter(self, data):
        _, count_res = self.bigram_counter(data)
        #print(res)
        #return res
        #print(count_res)
        #return count_res
        self.comm.send(count_res, dest=0, tag=12)
        #print("sent bigrams")
    
    def worker_unigram_counter(self, data, master):
        _, count_res = self.unigram_counter(data)
        if self.rank == 1:#sadece sent
            #print("if")
            #print(count_res)
            self.comm.send(count_res, dest=self.rank+1, tag=11)
            
        elif self.rank < master.worker_num:#önce receive, sonra sent
            #print("elif")
            received = self.comm.recv(source = self.rank-1, tag = 11)
            received.extend(count_res)
            #print(received)
            self.comm.send(received, dest=self.rank+1, tag=11)
            
        else:#sadece receive
            #print("else")
            received = self.comm.recv(source = self.rank-1, tag = 11)
            received.extend(count_res)
            #print(received)
            self.comm.send(received, dest=0, tag=11)
            
    def worker_bigram_counter(self, data, master):
        _, count_res = self.bigram_counter(data)
        if self.rank == 1:#sadece sent
            #print("if")
            #print(count_res)
            self.comm.send(count_res, dest=self.rank+1, tag=12)
            
        elif self.rank < master.worker_num:#önce receive, sonra sent
            #print("elif")
            received = self.comm.recv(source = self.rank-1, tag = 12)
            received.extend(count_res)
            #print(received)
            self.comm.send(received, dest=self.rank+1, tag=12)
            
        else:#sadece receive
            #print("else")
            received = self.comm.recv(source = self.rank-1, tag = 12)
            received.extend(count_res)
            #print(received)
            self.comm.send(received, dest=0, tag=12)  
    
    def master_merge(self):
        #print("master merge is called")
        self.master_unigram_counter(self.data)
        self.master_bigram_counter(self.data)
    
    def worker_merge(self):
        #print("worker merge is called.")
        self.worker_unigram_counter(self.data, self.master)
        self.worker_bigram_counter(self.data, self.master)
    
    def merge(self):
        if self.merge_method=="WORKERS":
            return self.worker_merge()
        elif self.merge_method=="MASTER":
            return self.master_merge()
    