import torch

def normalization(data):
            num_of_elements = data.shape[0]*data.shape[1]*data.shape[2]
            print(data.shape[0], data.shape[1],data.shape[2])
            mean = torch.sum(data)/(num_of_elements)
            print(mean)
            mean2 = torch.sum(data**2)/(num_of_elements)
            print(mean2)
            return(data*1000 - mean)/mean2
