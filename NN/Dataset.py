import torch


class Dataset:
    def __init__(self, data, metadata):
        for key, value in vars(metadata).items():
            setattr(self, key, value)
        for key, value in vars(data).items():
            setattr(self, key, value)
        self.checking_data_actuality()

    def __update__(self, metadata):
        for key, value in vars(data, metadata).item():
            setatter(self, key, value)

    def checking_data_actuality(self):
        input_shape_Dataset = self[0][0].shape[0]
        input_shape_overview = self.input_shape

        output_shape_Dataset = torch.flatten(self.data[0][1]).shape[0]
        ouput_shape_overview = self.output_shape1 * self.output_shape2 * 3

        if (
            input_shape_Dataset != input_shape_overview
            or output_shape_Dataset != ouput_shape_overview
        ):
            print(Fore.RED)
            print("Warning!: NN does not run with the latest data format")
            print(Style.RESET_ALL)
