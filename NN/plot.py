from sys import exc_info
from matplotlib import pyplot as plt
import numpy as np
import torch
from torchvision.utils import save_image
from PIL import Image
from torchvision import datasets, transforms
import base64
import os
from io import BytesIO
import asyncio


class Plotter():
    def __init__(self, props):
        self.props = props
        self.epochs = []
        self.losses = []

    async def plot(self, epoch):
        self.epochs.append(epoch)
        self.losses.append(self.props.model.loss)

        if epoch % self.props.overview.plot.show_information_rate == 0:
            samples = self.pack_samples()
            await self.props.SOCKET_CONNECTION.emit('/nn_metrics_s', {'epoch': self.epochs,
                                                                'loss': self.losses,
                                                                'training_sample': samples[0],
                                                                'test_sample': samples[1],
                                                                'weights': torch.flatten(self.props.model.linear_relu_stack[0].weight[0:2]).tolist()
                                                                })

    def pack_samples(self):
        self.props.model.eval()

        train = self.props.Dataset[0][0]
        test = self.props.Dataset[-1][0]

        pred_tr = self.props.model(train)
        pred_tr_0 = self.denormalizing(pred_tr)
        pred_tr_b64 = self.to_base64(pred_tr_0)

        pred_te = self.props.model(test)
        pred_te_0 = self.denormalizing(pred_te)
        pred_te_b64 = self.to_base64(pred_te_0)

        return [pred_tr_b64, pred_te_b64]

    def denormalizing(self, data):
        shape_1 = self.props.overview.data.output_shape1
        shape_2 = self.props.overview.data.output_shape2

        data = torch.mul(data, self.props.Dataset.var)
        data = torch.add(data, self.props.Dataset.mean).int()
        data = torch.div(data, 255)
        data[data > 1] = 1
        data[data < 0] = 0

        data = torch.reshape(data, (shape_1, shape_2, 3))
        data = data.to('cpu').detach().numpy()

        return data

    def to_base64(self, data):
        buf = BytesIO()
        plt.imsave(buf, data, format='jpeg')
        data = buf.getvalue()
        data = base64.b64encode(data).decode()

        return data
