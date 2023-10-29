from sys import exc_info
from matplotlib import pyplot as plt
import numpy as np
import torch
from PIL import Image as im 
from torchvision import transforms
import base64
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
            sio.connect('http://localhost:3000')
        except:
            pass

    def plot(self, epoch, model, Dataset):
        self.model = model
        self.Dataset = Dataset
        self.epochs.append(epoch)
        self.losses.append(model.loss.item())
        if epoch % 10 == 0:
            #generated_data = self.pack_generated_data()
            sio.emit('/send_s', {'epoch': self.epochs,
                                 'loss': self.losses,
                                 #'generated_data':im.fromarray(generated_data)
                                 })

    def pack_generated_data(self):
        self.model.eval()
        train = self.Dataset[0:10][0]
        test = self.Dataset[820:830][0]
        pred_tr = self.model(train)
        pred_te = self.model(test)
        transform = transforms.ToPILImage()
        pil_image = transform(train[0])
        # Convert the PIL image to bytes
        image_bytes = pil_image.tobytes()
        # Encode the bytes to base64
        base64_string = base64.b64encode(image_bytes).decode()
        return base64_string 
    #[torch.reshape(pred_tr[0], (256, 300)), torch.reshape(pred_te[0], (256, 300))]
