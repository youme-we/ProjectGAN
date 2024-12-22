import torch


class Plotters:
    def __init__(self, plots):
        for key, value in vars(plots).items():
            setattr(self, key, value)
        self.epochs = []
        self.losses = []

    async def listen(self, SOCKET_CONNECTION):
        self.SOCKET_CONNECTION = SOCKET_CONNECTION

    async def plot(self, epoch, model, dataset):
        self.plotting_el(epoch, model.loss)
        samplesTT = self.plotting_samplesTT(epoch, model, dataset)
        await self.SOCKET_CONNECTION.emit(
            "/nn_metrics_s",
            {
                "epoch": self.epochs,
                "loss": self.losses,
                "training_sample": samplesTT[0],
                "test_sample": samplesTT[1],
                "weights": torch.flatten(
                    model.linear_relu_stack[0].weight[0:2]
                ).tolist(),
            },
        )

    def plotting_el(self, epoch, loss):
        if self.el_plot.rate % epoch == 0:
            self.epochs.append(epoch)
            self.losses.append(loss)

    def plotting_samplesTT(self, epoch, model, dataset):
        pred_tr = model.predict(dataset[-1][0])
        pred_tr_b64 = dataset.to_base64(pred_tr)
        pred_te = model.predict(dataset[0][0])
        pred_te_b64 = dataset.to_base64(pred_te)
        return [pred_tr_b64, pred_te_b64]
