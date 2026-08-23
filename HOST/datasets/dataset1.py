import torch
from colorama import Fore


class Dataset:
    def __init__(self, dataset_config, inputs, targets):
        self.__dict__.update(dataset_config)
        self.inputs = inputs
        self.targets = targets
        self.target_dim = self.image_height_px * self.image_width_px * 3

        self.checking_data_actuality()

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, idx):
        input = self.inputs[idx]
        target = self.targets[idx]
        return input, target

    def checking_data_actuality(self):
        latent_dim_dataset = self[0][0].shape[0]
        latent_dim_dataset_config = self.latent_dim

        image_flatten_size_dataset = torch.flatten(self[0][1]).shape[0]
        image_flatten_size_dataset_config = (
            self.image_height_px * self.image_width_px * 3
        )
        if (
            latent_dim_dataset != latent_dim_dataset_config
            or image_flatten_size_dataset != image_flatten_size_dataset_config
        ):
            print(
                Fore.RED + "WARNING:",
                "Neural network is incompatible with the current data format",
            )
