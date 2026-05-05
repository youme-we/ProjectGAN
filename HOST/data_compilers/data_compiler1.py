import os

import torch
from PIL import Image
from tqdm import tqdm


class DataCompiler1:
    def __init__(self, dataset_config):
        self.__update__(dataset_config)

    def __update__(self, dataset_config):
        self.__dict__.update(dataset_config)

    def sample_latent_vectors(self, batch_size):
        return torch.randn(batch_size, self.input_dim, dtype=self.dtype)

    def load_images(self):
        image_dir = os.path.join(self.data_dir, "original")

        transform = transforms.Compose(
            [
                transforms.Resize((self.image_height, self.image_width)),
                transforms.ToTensor(),
            ]
        )

        image_tensors = []

        for image_name in tqdm(os.listdir(image_dir)):
            if not image_name.lower().endswith((".jpg", ".jpeg", ".png")):
                os.remove(os.path.join(image_dir, image_name))
                continue

            image_path = os.path.join(image_dir, image_name)

            try:
                image = Image.open(image_path).convert("RGB")
                image_tensor = transform(image)
                image_tensors.append(image_tensor)

            except Exception as e:
                print(f"Skipping {image_name}: {e}")

        return torch.stack(image_tensors)

    # call 1.
    def generate_training_data(self):
        targets = self.load_images()
        inputs = self.sample_latent_vectors(len(targets))
        return inputs, targets

    # call 2.
    def save_training_data(self, inputs, targets):
        torch.save(inputs, os.path.join(self.data_dir, "inputs.pt"))
        torch.save(targets, os.path.join(self.data_dir, "targets.pt"))
