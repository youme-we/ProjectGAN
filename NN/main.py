import torch
import asyncio
from tqdm import tqdm
from torch import func, nn, optim
from torch.utils.data import Dataset, sampler, DataLoader
from NN import NeuralNetwork
from subfunc import device, checking_data_actuality
from operating import Operator
from plot import Plot_Data
import socketio
from types import SimpleNamespace

sio = socketio.AsyncSimpleClient()
torch.set_default_device(device())
Plot_Data = Plot_Data()
Operator = Operator()


class Main:
    def __init__(self, Dataset):
        self.overview = Operator.overview
        self.Dataset = Dataset
        # checking if NN runs with the latest Data(comparing shape of parameters.json and given data)
        checking_data_actuality(
            self.Dataset, self.overview)

        self.model = NeuralNetwork(
            self.overview)
        self.Dataset = Dataset

    async def NN(self):
        await sio.connect('http://localhost:3001')
        SOCKET_CONNECTION = sio

        operator = await Operator.listen(SOCKET_CONNECTION)

        for epoch in tqdm(range(self.overview.hyperparameters.epochs)):
            overview = Operator.overview
            if epoch%10 ==0:
                print(overview.hyperparameters.learning_rate)
            optimizer = torch.optim.SGD(
                self.model.parameters(), lr=overview.hyperparameters.learning_rate, momentum=overview.hyperparameters.momentum)
            scheduler = torch.optim.lr_scheduler.StepLR(
                optimizer, step_size=1, gamma=0.99999)
            samplers_data = sampler.SubsetRandomSampler(
                indices=torch.arange(overview.hyperparameters.N_samples))
            training_dataloader = DataLoader(
                self.Dataset, sampler=samplers_data, batch_size=overview.hyperparameters.batch_size)

            for batch, (X, y) in enumerate(training_dataloader):
                    # trains model
                    self.model.iter(X, y, self.model, nn.MSELoss(),
                                    optimizer, scheduler)

                    # for param_group in optimizer.param_groups:
                    # print(param_group['lr'])

                    await Operator.operate()
                    if Operator.run == False:
                        Operator.group.cancel()
                        return

            # saves the epoch and the loss in a key value pair and seds it every nth epoch to the server/plot api over Socket.IO
            await Plot_Data.plot(epoch, self.model, self.Dataset, overview, SOCKET_CONNECTION)
