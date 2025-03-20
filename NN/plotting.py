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
        if epoch % self.el_plot.rate == 0:
            await self.SOCKET_CONNECTION.emit(
                "/nn_metrics_s",
                {
                    "epoch": epoch,
                    "loss": model.loss,
                    "training_sample": samplesTT[0],
                    "test_sample": samplesTT[1],
                },
            )

    def plotting_el(self, epoch, loss):
        self.epochs.append(epoch)
        self.losses.append(loss)

    def plotting_samplesTT(self, epoch, model, dataset):
        pred_tr = model.predict(dataset[0][0])
        pred_tr_b64 = dataset.to_base64(pred_tr)
        pred_te = model.predict(dataset[-1][0])
        pred_te_b64 = dataset.to_base64(pred_te)
        return [pred_tr_b64, pred_te_b64]
