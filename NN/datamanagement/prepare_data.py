import torch

def normalization(data):
            mean = torch.mean(data)
            var = torch.std(data)
            normalied_data = (data - mean)/var
            return normalied_data, mean, var
