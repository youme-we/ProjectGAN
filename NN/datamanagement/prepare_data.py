import torch

def normalization(data):
            mean = torch.mean(data)
            var = torch.std(data)
            print(mean,var)
            print(data)
            return(data - mean)/var
