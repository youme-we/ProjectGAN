from matplotlib import pyplot as plt
from tqdm import tqdm
from torch import nn
from torch.utils.data import Dataset, sampler, DataLoader
import torch
import numpy 
from NN import NeuralNetwork
from subfunc import device
from plot import Plot_Data
Plot_Data = Plot_Data()


class Main:
    def __init__(self, Dataset, hyperparameters):
        self.device = device()
        self.cpu_d = "cpu"
        self.hyperparameters = hyperparameters
        self.input_shape = Dataset[0][0].shape[0]
        self.output_shape = torch.flatten(Dataset[0][1]).shape[0]
        #torch.set_printoptions(profile="full")
        #print(Dataset[0][1])
        self.model = NeuralNetwork(
            self.input_shape, self.output_shape).to(self.device)
        self.Dataset = Dataset
        self.loss_fn = nn.MSELoss()

    def NN(self):
        hyperparameters = self.hyperparameters
        optimizer = torch.optim.SGD(
            self.model.parameters(), lr=hyperparameters.learning_rate)
        samplers_data = sampler.SubsetRandomSampler(
            indices=torch.arange(hyperparameters.N_samples))
        training_dataloader = DataLoader(
            self.Dataset, sampler=samplers_data, batch_size=hyperparameters.batch_size)

        for epoch in tqdm(range(hyperparameters.epochs)):
            self.model.iter(training_dataloader, self.model, self.loss_fn,
                            optimizer, epoch, hyperparameters.show_information_rate)

            # saves the epoch and the loss in a key value pair and seds it every nth epoch to the client/plot api
            Plot_Data.plot(epoch, self.model, self.Dataset)

            if epoch+1 % hyperparameters.show_information_rate == 0:
                print(f"Epoch {epoch}\n-------------------------------")

        print("Done!")
        self.model.eval()
        x,y = self.Dataset[0]
        pred = self.model(x)
        pred = torch.reshape(pred*73.6184+115.2330, (128,158,3))
        print(pred[0])
        pred = pred.to(self.cpu_d).int()
        plt.imshow(pred)
        plt.show()
        
        x,y = self.Dataset[600]
        pred = self.model(x)
        pred = torch.reshape(pred*73.6184+115.2330, (128,158,3))
        print(pred[0])
        pred = pred.to(self.cpu_d).int()
        plt.imshow(pred)
        plt.show()


