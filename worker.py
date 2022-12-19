from mpi4py import MPI

class Worker():
    def __init__(self,data,merge_method, master, rank):
        self.data=data
        self.merge_method=merge_method
        self.master = master
        self.rank = rank
        self.comm = MPI.COMM_WORLD
        
    def unigram_counter(self):
        res = dict()
        for d in self.data:
            d = d.split()
            for unigram in d:
                if unigram not in res:
                    res[unigram]=1
                else:
                    res[unigram]+=1
        return res

    def bigram_counter(self):
        res = dict()
        for d in self.data:
            d = d.split()
            for i in range(len(d) - 1):
                bigram=d[i]+" "+d[i+1]
                if bigram not in res:
                    res[bigram]=1
                else:
                    res[bigram]+=1
        return res
    
    def worker_method_channel(self, tag):
        if(tag==11):
            result = self.unigram_counter()
        elif(tag==12):
            result = self.bigram_counter()
        else:
            raise Exception("Wrong n-gram type") 

        if self.rank == 1:
            self.comm.send(result, dest=self.rank+1, tag = tag)
            
        else:
            received = self.comm.recv(source = self.rank-1, tag = tag)
            for key in result.keys():
                if key not in received:
                    received[key]=0
                received[key]+=result[key]
                
            destination = self.rank+1
            if(self.rank==self.master.worker_num):
                destination=0
            self.comm.send(received, dest=destination, tag = tag)
    
    def master_merge(self):
        unigrams = self.unigram_counter()
        bigrams = self.bigram_counter()

        self.comm.send(unigrams, dest=0, tag=11)
        self.comm.send(bigrams, dest=0, tag=12)
    
    def worker_merge(self):
        self.worker_method_channel(11)
        self.worker_method_channel(12)
    
    def merge(self):
        if self.merge_method=="WORKERS":
            return self.worker_merge()
        elif self.merge_method=="MASTER":
            return self.master_merge()