from mpi4py import MPI



class Worker():
    def __init__(self,data,merge_method, master):
        self.data=data
        self.merge_method=merge_method
        self.master = master
        self.comm = MPI.COMM_WORLD
    
    def master_unigram_counter(self, data):
        res = list()
        count_res = list()
        for d in data:
            d = d.split()
            res.append(d)
            count_res.append(len(d))
        #print(res)
        #return res
        #print(count_res)
        #return count_res
        self.comm.send(count_res, dest=0, tag=11)
        print("sent unigrams")
        
    def master_bigram_counter(self, data):
        res = list()
        count_res = list()
        for d in data:
            tmp = list()
            d = d.split()
            for i in range(len(d) - 1):
                tmp.append(d[i:i+2])
            res.append(tmp)
            count_res.append(len(tmp))
        #print(res)
        #return res
        #print(count_res)
        #return count_res
        self.comm.send(count_res, dest=0, tag=12)
        print("sent bigrams")
    
    def master_merge(self):
        #print("master merge is called")
        self.master_unigram_counter(self.data)
        self.master_bigram_counter(self.data)
    
    def worker_merge(self):
        print("worker merge is called.")
    
    def merge(self):
        if self.merge_method=="WORKERS":
            return self.worker_merge()
        elif self.merge_method=="MASTER":
            return self.master_merge()
    