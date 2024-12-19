import torch

def normalization(data):
            mean = torch.mean(data)
            var = torch.std(data)
            normalized_data = (data - mean)/var
            print(normalized_data)
            return normalized_data, mean, var
