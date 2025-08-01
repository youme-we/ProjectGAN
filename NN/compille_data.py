import os
import sys

import torch
from PIL import Image
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import load_json

overview = load_json("../overview.json")
data_dir = "../data/cars"
input_shape = 2048
output_shape1 = 64
output_shape2 = 84
dtype = "torch.float32"

dtype_map = {
    "float32": torch.float32,
    "float64": torch.float64,
    "int32": torch.int32,
    "int64": torch.int64,
    "uint8": torch.uint8,
}


class ImageDatasetCompiler:
    def __init__(self, data_dir, input_shape, output_shape1, output_shape2, dtype):
        self.data_dir = os.path.join("../data", data_dir)
        self.input_shape = input_shape
        self.output_shape1 = output_shape1
        self.output_shape2 = output_shape2
        self.dtype = getattr(torch, dtype, None)
        self.all_images = torch.empty(
            (0, output_shape1, output_shape2, 3), dtype=self.dtype
        )

    def create_labels(self):
        for image in tqdm(os.listdir(os.path.join(self.data_dir, "original"))):
            if image.endswith((".jpg", ".jpeg")):
                img_path = os.path.join(self.data_dir, "original", image)
                img = (
                    Image.open(img_path)
                    .resize((self.output_shape2, self.output_shape1))
                    .convert("RGB")
                )
                img_tensor = torch.tensor(img.getdata(), dtype=self.dtype).view(
                    1, self.output_shape1, self.output_shape2, 3
                )
                self.all_images = torch.cat((self.all_images, img_tensor), dim=0)
            else:
                os.remove(os.path.join(self.data_dir, "original", image))
        torch.save(self.all_images, os.path.join(self.data_dir, "labels.pt"))

    def create_inputs(self):
        inputs = torch.rand(len(self.all_images), self.input_shape, dtype=self.dtype)
        torch.save(inputs, os.path.join(self.data_dir, "inputs.pt"))


compiller = ImageDatasetCompiler(
    data_dir, input_shape, output_shape1, output_shape2, dtype
)
print("compilling data...")
compiller.create_labels()
compiller.create_inputs()
print("done!")
