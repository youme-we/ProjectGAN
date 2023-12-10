import torch
import asyncio
from tqdm import tqdm
from torch import nn
from torch.utils.data import Dataset, sampler, DataLoader
from NN import NeuralNetwork
from subfunc import device
from operating import Operator
from plot import Plot_Data
import socketio

sio = socketio.AsyncSimpleClient()
Plot_Data = Plot_Data()
Operator = Operator()


class Main:
    def __init__(self, Dataset, parameters):
        self.device = device()
        data_p = parameters.data
        self.parameters = parameters
        self.input_shape = Dataset[0][0].shape[0]  # data_p.input_shape
        self.output_shape = torch.flatten(Dataset[0][1]).shape[0]
        # data_p.shape_1*data_p.shape_2*3
        self.model = NeuralNetwork(
            self.input_shape, self.output_shape).to(self.device)
        self.Dataset = Dataset
        self.loss_fn = nn.MSELoss()

    async def NN(self):
        await sio.connect('http://localhost:3001')
        SOCKET_CONNECTION = sio
        hyperparameters = self.parameters.hyperparameters
        optimizer = torch.optim.SGD(
            self.model.parameters(), lr=hyperparameters.learning_rate)
        samplers_data = sampler.SubsetRandomSampler(
            indices=torch.arange(hyperparameters.N_samples))
        training_dataloader = DataLoader(
            self.Dataset, sampler=samplers_data, batch_size=hyperparameters.batch_size)

        operator = await Operator.listen(SOCKET_CONNECTION)
        for epoch in tqdm(range(hyperparameters.epochs)):
            # trains model:
            self.model.iter(training_dataloader, self.model, self.loss_fn,
                            optimizer)

            # saves the epoch and the loss in a key value pair and seds it every nth epoch to the server/plot api over Socket.IO
            await Plot_Data.plot(epoch, self.model, self.Dataset, self.parameters, SOCKET_CONNECTION)
            await Operator.operate()
