class Worker():
    def __init__(self,data,merge_method):
        self.data=data
        self.merge_method=merge_method
    def master_merge(self):
        pass
    def worker_merge(self):
        pass
    def merge(self):
        if self.merge_method=="WORKERS":
            return self.worker_merge()
        return self.master_merge()