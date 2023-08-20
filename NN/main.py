from NN_subfunc import device, NeuralNetwork, send_plot
import torch
from torch.utils.data import Dataset, sampler, DataLoader
from torch import nn
from tqdm import tqdm
from matplotlib import pyplot as plt
# imports functions and classes from other file needed for the NN


class Main:
    def __init__(self, Dataset, hyperparameters):
        self.device = device()
        self.cpu_d = "cpu"
        self.hyperparameters = hyperparameters
        self.input_shape = Dataset[0][0].shape[0]
        self.output_shape = Dataset[0][1].shape[0]
        # in future the hole shape of the NN will be passed to the funciton
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
            if epoch % hyperparameters.show_information_rate == 0:
                send_plot(epoch,self.model.loss)
                print(f"Epoch {epoch}\n-------------------------------")



        print("Done!")
        plt.show()
