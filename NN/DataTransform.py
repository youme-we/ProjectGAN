import torch


class DataTransform:
    def __init__(self, reference_data):
        self.reference_data = reference_data

    def normalize(self, data):
        self.mean = self.reference_data.mean(dim=1, keepdim=True)
        self.std = self.refernce_data.std(dim=1, keepdim=True)
        return (data - mean) / std

    def denormalize(self, data):
        self.mean = self.reference_data.mean(dim=1, keepdim=True)
        self.std = self.refernce_data.std(dim=1, keepdim=True)
        return data * self.std + self.mean
