import base64
from io import BytesIO

import torch
from matplotlib import pyplot as plt
from numpy import imag


class Dataset:
    def __init__(self, metadata, inputs, labels):
        for key, value in vars(metadata).items():
            setattr(self, key, value)
        self.inputs = inputs
        self.labels = labels
        self.checking_data_actuality()

    def __update__(self, metadata):
        for key, value in vars(data, metadata).item():
            setatter(self, key, value)

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

    def to_base64(self, image_vector):
        image_vector = torch.div(image_vector, 255)
        image_vector[image_vector > 1] = 1
        image_vector[image_vector < 0] = 0

        image_vector = torch.reshape(
            image_vector, (self.output_shape1, self.output_shape2, 3)
        )
        image_vector = image_vector.to("cpu").detach().numpy()
        buf = BytesIO()
        plt.imsave(buf, image_vector, format="jpeg")
        image_vector = buf.getvalue()
        image_vector = base64.b64encode(image_vector).decode()
        return image_vector
