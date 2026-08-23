import base64
from io import BytesIO

import torch
from matplotlib import pyplot as plt


class ImageTransformer:
    def __init__(self):
        pass

    def encode_images_to_base64(self, image_vectors, height_px, width_px):
        base64_images = []
        image_vectors = torch.div(image_vectors, 255)
        image_vectors[image_vectors > 1] = 1
        image_vectors[image_vectors < 0] = 0
        for image_vector in image_vectors:
            image_vector = torch.reshape(image_vector, (height_px, width_px, 3))
            image_vector = image_vector.to("cpu").detach().numpy()
            buf = BytesIO()
            plt.imsave(buf, image_vector, format="jpeg")
            image_vector = buf.getvalue()
            base64_image = base64.b64encode(image_vector).decode()
            base64_images.append(base64_image)
        return base64_images
