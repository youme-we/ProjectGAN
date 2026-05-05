import base64
from io import BytesIO

import torch
from colorama import Fore
from matplotlib import pyplot as plt


class Dataset:
    def __init__(self, dataset_config, inputs, targets):
        self.inputs = inputs
        self.targets = targets
        self.__dict__.update(dataset_config)
        self.input_dim = self.latent_dim
        self.target_dim = self.image_height_px * self.image_width_px * 3

    def __update__(self, dataset_config):
        self.__dict__.update(dataset_config)
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

    def encode_images_to_base64(self, image_vectors):
        base64_images = []
        image_vectors = torch.div(image_vectors, 255)
        image_vectors[image_vectors > 1] = 1
        image_vectors[image_vectors < 0] = 0
        for image_vector in image_vectors:
            image_vector = torch.reshape(
                image_vector, (self.image_height_px, self.image_width_px, 3)
            )
            image_vector = image_vector.to("cpu").detach().numpy()
            buf = BytesIO()
            plt.imsave(buf, image_vector, format="jpeg")
            image_vector = buf.getvalue()
            base64_image = base64.b64encode(image_vector).decode()
            base64_images.append(base64_image)
        return base64_images
