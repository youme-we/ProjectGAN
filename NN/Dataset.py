import base64
from io import BytesIO

import torch
from matplotlib import pyplot as plt
from numpy import imag


class Dataset:
    def __init__(self, metadata, inputs, labels):
        self.__update__(metadata)
        self.inputs = inputs
        self.labels = labels
        self.checking_data_actuality()

    def __update__(self, metadata):
        self.__dict__.update(metadata)

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        input = self.inputs[idx]
        label = self.labels[idx]
        return input, label

    def checking_data_actuality(self):
        input_shape_Dataset = self[0][0].shape[0]
        input_shape_overview = self.input_shape

        output_shape_Dataset = torch.flatten(self[0][1]).shape[0]
        ouput_shape_overview = self.output_shape1 * self.output_shape2 * 3

        if (
            input_shape_Dataset != input_shape_overview
            or output_shape_Dataset != ouput_shape_overview
        ):
            diagnostics("NN does not run with the latest data format", "warning")

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
