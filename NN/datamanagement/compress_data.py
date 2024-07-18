import torch
import sys
import os
from PIL import Image
from prepare_data import normalization
from torch.utils.data import TensorDataset
sys.path.insert(0, '/Users/skost/coding-s/ProjectGAN/NN/')
from subfunc import load_json  # beacuse of formater this line often moves to the top
data_p = load_json('/Users/skost/coding-s/ProjectGAN/NN/parameters.json').data
dtype = torch.float32

class Load_Dataset():

    def __init__(self, folder_dir, input_shape, shape_1, shape_2):
        self.folder_dir = folder_dir
        self.input_shape = input_shape
        self.shape_1 = shape_1
        self.shape_2 = shape_2

    def torch_Dataset(self):
        train_output, mean, var = self.load_img_fs()  # load images from filesystem
        train_input = self.generate_input()

        # puts the lables to the corresoponding image. So that when you print the [0] obj you get [[image],[label]]
        train_data = TensorDataset(train_input, train_output)
        train_data.mean = mean
        train_data.var = var
        print("mean:", train_data.mean, "var:", train_data.var)
        return train_data

    def save(self, Dataset):
        torch.save(Dataset, "/Users/skost/coding-s/ProjectGAN/NN/data/data.pt")

    def load_img_fs(self):
        folder_dir = self.folder_dir
        shape_1 = self.shape_1
        shape_2 = self.shape_2
        a = 0
        all_images = torch.tensor([])

        for images in os.listdir(folder_dir):
            if (images.endswith(".jpg")):
                a += 1
                img = Image.open(folder_dir+"/"+images)
                img = img.resize((shape_2, shape_1))  # you need two bracket's
                img = img.convert('RGB')
                img = img.getdata()
                img = torch.tensor(img, dtype=dtype)
                img = torch.reshape(img, (shape_1, shape_2, 3))
                all_images = torch.cat((all_images, img), dim=0)
        self.maxNumber_of_images = a
        train_images_unedited = torch.reshape(
            all_images, (a, shape_1, shape_2, 3))

        train_images, mean, var = normalization(train_images_unedited)
        return train_images, mean, var

    def generate_input(self):
        return torch.rand(self.maxNumber_of_images, self.input_shape, dtype=dtype)


main_Dataset_i = Load_Dataset(
    data_p.folder_dir, data_p.input_shape, data_p.shape_1, data_p.shape_2)
main_Dataset = main_Dataset_i.torch_Dataset()  # make data to torch Dataset
main_Dataset_i.save(main_Dataset)  # save data as .pt file
print("your data was succesfully compressed")
