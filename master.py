class Master():
    def __init__(self,worker_num):
        self.worker_num=worker_num
    
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