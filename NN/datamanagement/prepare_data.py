import torch

def normalization(data):
            num_of_elements = data.shape[0]*data.shape[1]
            mean = torch.sum(data)/(num_of_elements)
            mean2 = torch.sum(data**2)/(num_of_elements)
            return(data - mean)/mean2
