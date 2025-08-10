import torch


class DataTransformer1:
    def __init__(self, reference_data):
        self.reference_data = reference_data

    def normalize(self, data):
        mean = torch.mean(self.reference_data)
        std = torch.std(self.reference_data)
        return (data - mean) / std

    def denormalize(self, data):
        mean = torch.mean(self.reference_data)
        std = torch.std(self.reference_data)
        return data * std + mean
