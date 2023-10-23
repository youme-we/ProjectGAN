
import torch
import os
from PIL import Image
from torch.functional import Tensor
from prepare_data import normalization
from torch.utils.data import DataLoader, TensorDataset
dtype = torch.float

class Load_data():

    def __init__(self,folder_dir, input_shape, shape_1, shape_2):
        self.folder_dir = folder_dir
        self.input_shape = input_shape
        self.shape_1 = shape_1
        self.shape_2 = shape_2
       
    def data(self):
        train_images = self.Load_images_from_file_system()
        train_images = torch.flatten(train_images, start_dim=1)
        train_input = self.generate_input()
        
        # puts the lables to the corresoponding image. So that when you print the [0] obj you get [[image],[label]]
        data = TensorDataset(train_input, train_images)
        return data


    def Load_images_from_file_system(self):
        folder_dir = self.folder_dir
        input_shape = self.input_shape
        shape_1 = self.shape_1
        shape_2 = self.shape_2
        a = 0
        all_images = torch.tensor([])

        for images in os.listdir(folder_dir):
            if (images.endswith(".jpg")):
                a = a+1
                img = Image.open(folder_dir+"/"+images)
                img = img.resize((shape_2, shape_1))
                img = img.convert('L')
                img = img.getdata()
                img = torch.tensor(img)
                img = torch.reshape(img, (shape_1, shape_2))
                all_images = torch.cat((all_images, img), dim=0)
        self.maxNumber_of_images = a
        train_images_unedited = torch.reshape(
            all_images, (a, shape_1, shape_2))
        
        torch.set_printoptions(profile="full")
        train_images = normalization(train_images_unedited)
        print(train_images[0])
        return train_images


    def generate_input(self):
        r1 = -10
        r2 = 10
        return ((r1 - r2) * torch.rand(self.maxNumber_of_images, self.input_shape, dtype=dtype) + r2)

    
Load_data = Load_data("/Users/skost/coding-s/Data/Images/cars",
                 128, 512, 550)
data = Load_data.data()
torch.save(data, "/Users/skost/coding-s/ProjectGAN/NN/data/data.pt")
print("your data was succesfully compressed")
