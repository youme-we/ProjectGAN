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
