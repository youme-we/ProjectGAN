from bson import ObjectId


class Plotter:
    def __init__(self, plotter_config, config_id):
        self.__dict__.update(plotter_config)
        self.run_id = ObjectId()
        self.config_id = config_id

    def __update__(self, plotter_config):
        self.__dict__.update(plotter_config)

    async def listen(self, SOCKET_CONNECTION):
        self.SOCKET_CONNECTION = SOCKET_CONNECTION

    async def plot(self, epoch, iter_result, train_result, test_result):
        if epoch % self.rate == 0:
            await self.SOCKET_CONNECTION.emit(
                "nn_metrics_s",
                {
                    "run_id": str(self.run_id),
                    "config_id": self.config_id,
                    "epoch": epoch,
                    "loss": iter_result["loss"],
                    "training_samples": train_result["b64"],
                    "test_samples": test_result["b64"],
                },
            )
