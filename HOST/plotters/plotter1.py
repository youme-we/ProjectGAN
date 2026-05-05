class Plotter:
    def __init__(self, plotter_config, trainer):
        self.trainer = trainer
        self.__dict__.update(plotter_config)

    def __update__(self, plotter_config):
        self.__dict__.update(plotter_config)

    async def listen(self, SOCKET_CONNECTION):
        self.SOCKET_CONNECTION = SOCKET_CONNECTION

    async def plot(self, epoch):
        if epoch % self.rate == 0:
            samplesTT = self.plotting_samplesTT(epoch)
            await self.SOCKET_CONNECTION.emit(
                "/nn_metrics_s",
                {
                    "epoch": epoch,
                    "loss": self.trainer.loss,
                    "training_samples": samplesTT[0],
                    "test_samples": samplesTT[1],
                },
            )

    def plotting_samplesTT(self, epoch):
        pred_tr = self.trainer.predict(self.trainer._dataset[0:2][0])
        pred_tr_b64 = self.trainer._dataset.encode_images_to_base64(pred_tr)
        pred_te = self.trainer.predict(self.trainer._dataset[-2:][0])
        pred_te_b64 = self.trainer._dataset.encode_images_to_base64(pred_te)
        return [pred_tr_b64, pred_te_b64]
