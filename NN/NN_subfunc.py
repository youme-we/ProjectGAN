import torch
from torch import imag, nn, softmax
import numpy
import requests
from matplotlib import pyplot as plt


def device():
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu")

    return device


def plot_example_data():
    print(f"Feature batch shape: {train_features.size()}")
    print(f"Labels batch shape: {train_labels.size()}")
    img = train_features[0].squeeze()
    label = train_labels[0]
    plt.imshow(img, cmap="gray")
    plt.show()
    print(f"Label: {label}")

    print(f"Using {device} device")


def send_plot(epoch, loss):
    url = 'https://localhost:3000/plot'
    myobj = {'epoch': epoch, "loss": loss.item()}

    x = requests.post(url, json=myobj)


class NeuralNetwork(nn.Module):
    def __init__(self, input_shape, output_shape):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_shape, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, output_shape),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

    def iter(self, dataloader, model, loss_fn, optimizer, epoch, show_information_rate):
        model.train()  # prepers the model for training. sets all states like drop out... but doesn't train
        for batch, (X, y) in enumerate(dataloader):
            X, y = X.to(device()), y.to(device())
            # Compute prediction error
            pred = model(X)
            loss = loss_fn(pred, y)
            self.lable = y
            self.pred = pred
            self.loss = loss

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


def test_2(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()  # prepsers the model for testing. doesn't change any parameters... but doesn't test
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(
        f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")


def test(test_data, model, loss_fn):
    model.eval()
    figure = plt.figure(figsize=(8, 8))
    cols, rows = 3, 3
    for i in range(1, 10):
        img, label = test_data[i]
        img, label = img.to(device()), label.to(device())
        pred = model(img)
        softmax = nn.Softmax(dim=1)
        pred = softmax(pred)
        loss = loss_fn(pred[0], label)
        max = torch.max(pred, 1)
        figure.add_subplot(rows, cols, i)
        surenes = str(round((max.values*100).item(), 3))
        prediction = labels_map[max.indices.item()]+" "+surenes+"%"
        plt.title(prediction)
        plt.axis("off")
        plt.imshow(img.to("cpu").squeeze(), cmap="gray")

    plt.show()
