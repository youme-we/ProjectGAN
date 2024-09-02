import torch
from tqdm import tqdm
from torch import func, nn, optim
from torch.utils.data import Dataset, sampler, DataLoader
from NN import GAN
from subfunc import device, checking_data_actuality, load_json
from operating import Operator
from plot import Plotter
import socketio

sio = socketio.AsyncSimpleClient()
torch.set_default_device(device())


class Trainer:
    def __init__(self, Dataset):
        self.__overview = load_json("../overview.json")
        self.Dataset = checking_data_actuality(
            Dataset, self.__overview)
        self.model = GAN(
            self.__overview)

    async def init(self):
        await sio.connect('http://localhost:3001')
        self.SOCKET_CONNECTION = sio
        self.__operator = Operator(self)
        await self.__operator.listen(self.SOCKET_CONNECTION)
        self.__plotter = Plotter(self)

    @property
    def overview(self):
        return self.__overview

    @overview.setter
    def overview(self, new_overview):
        self.__overview = new_overview

    async def train(self):
        for epoch in tqdm(range(self.__overview.hyperparameters.epochs)):
            optimizer = torch.optim.SGD(
                self.model.parameters(), lr=self.__overview.hyperparameters.learning_rate, momentum=self.__overview.hyperparameters.momentum)
            scheduler = torch.optim.lr_scheduler.StepLR(
                optimizer, step_size=1, gamma=0.9)
            samplers_data = sampler.SubsetRandomSampler(
                indices=torch.arange(self.__overview.hyperparameters.N_samples))
            training_dataloader = DataLoader(
                self.Dataset, sampler=samplers_data, batch_size=self.__overview.hyperparameters.batch_size)

            for batch, (X, y) in enumerate(training_dataloader):
                self.model.iter(X, y, nn.MSELoss(),
                                optimizer, scheduler)

                await self.__operator.operate()
                if not self.__operator.run:
                    self.__operator.group.cancel()
                    return

            await self.__plotter.plot(epoch)
