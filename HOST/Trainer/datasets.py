import base64
from io import BytesIO
from colorama import Back, Fore, Style
import torch
from matplotlib import pyplot as plt
from numpy import imag


class Dataset1:
    def __init__(self, metadata, inputs, targets):
        self.inputs = inputs
        self.targets = targets
        self.__update__(metadata)

    def __update__(self, metadata):
        self.__dict__.update(metadata)
        self.checking_data_actuality()

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, idx):
        input = self.inputs[idx]
        target = self.targets[idx]
        return input, target

    def checking_data_actuality(self):
        input_shape_Dataset = self[0][0].shape[0]
        input_shape_project_config = self.input_shape

        output_shape_Dataset = torch.flatten(self[0][1]).shape[0]
        output_shape_project_config = self.output_shape1 * self.output_shape2 * 3
        if (
            input_shape_Dataset != input_shape_project_config
            or output_shape_Dataset != output_shape_project_config
        ):
            print(
                Fore.RED + "WARNING:",
                "Neural network is incompatible with the current data format",
            )

    def to_base64(self, image_vectors):
        base64_images = []
        image_vectors = torch.div(image_vectors, 255)
        image_vectors[image_vectors > 1] = 1
        image_vectors[image_vectors < 0] = 0
        for image_vector in image_vectors:
            image_vector = torch.reshape(
                image_vector, (self.output_shape1, self.output_shape2, 3)
            )
            image_vector = image_vector.to("cpu").detach().numpy()
            buf = BytesIO()
            plt.imsave(buf, image_vector, format="jpeg")
            image_vector = buf.getvalue()
            base64_image = base64.b64encode(image_vector).decode()
            base64_images.append(base64_image)
        return base64_images
