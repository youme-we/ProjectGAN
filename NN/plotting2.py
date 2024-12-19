class Plotters:
    def __init__(self, plots):
        for key, value in vars(plots).items():
            setattr(self, key, value)
    
    async def listen(self, SOCKET_CONNECTION):
        self.SOCKET_CONNECTION = SOCKET_CONNECTION

    async def plot(self, epoch, model):
        self.plotting_el(epoch, model.loss)

    def plotting_el(self, epoch, loss):
        if self.el_plot.rate % epoch == 0:
            print("plotting")



