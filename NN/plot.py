from sys import exc_info
from matplotlib import pyplot as plt
import numpy as np
import torch
from torchvision.utils import save_image
from PIL import Image
from torchvision import transforms
import base64
from io import BytesIO
import asyncio
import socketio
sio = socketio.Client()


def plot_example_data():
    print(f"Feature batch shape: {train_features.size()}")
    print(f"Labels batch shape: {train_labels.size()}")
    img = train_features[0].squeeze()
    label = train_labels[0]
    plt.imshow(img, cmap="gray")
    plt.show()
    print(f"Label: {label}")

    print(f"Using {device} device")


class Plot_Data():
    def __init__(self):
        self.epochs = []
        self.losses = []
        try:
            sio.connect('http://localhost:3001')
        except:
            print("didn't connect to the server => doesn't send plot")

    def plot(self, epoch, model, Dataset, parameters):
        self.model = model
        self.Dataset = Dataset
        self.parameters = parameters
        self.epochs.append(epoch)
        self.losses.append(model.loss.item())
        if epoch % self.parameters.plot.show_information_rate == 0:
            generated_data = self.pack_generated_data()
            sio.emit('/send_s', {'epoch': self.epochs,
                                 'loss': self.losses,
                                 'generated_data': generated_data[1],
                                 'imitated_data': generated_data[0]
                                 })

    def pack_generated_data(self):
        self.model.eval()

        train = self.Dataset[0:10][0]
        test = self.Dataset[-10:][0]

        pred_tr = self.model(train)
        pred_tr_0 = self.prepare_data(pred_tr[0])
        pred_tr_b64 = self.to_base64(pred_tr_0)

        pred_te = self.model(test)
        pred_te_0 = self.prepare_data(pred_te[0])
        pred_te_b64 = self.to_base64(pred_te_0)

        return [pred_tr_b64, pred_te_b64]

    def prepare_data(self, data):
        shape_1 = self.parameters.data.shape_1
        shape_2 = self.parameters.data.shape_2

        data = torch.mul(data, self.Dataset.var)
        data = torch.add(data, self.Dataset.mean).int()
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
