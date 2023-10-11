from matplotlib import pyplot as plt
import asyncio
import socketio
sio = socketio.Client()
sio.connect('http://localhost:3000')


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

    def plot(self, epoch, loss):
        self.epochs.append(epoch)
        self.losses.append(loss.item())
        if epoch % 100 == 0:
            sio.emit('/message_c', {'epoch': self.epochs,
                                    'loss': self.losses,
                                    })
