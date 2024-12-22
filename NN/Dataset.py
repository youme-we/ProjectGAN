import torch


class Dataset:
    def __init__(self, metadata, inputs, labels, transform=None, target_transform=None):
        for key, value in vars(metadata).items():
            setattr(self, key, value)
        self.inputs = inputs
        self.labels = labels
        self.transform = transform
        self.target_transform = target_transform
        self.checking_data_actuality()

    def __update__(self, metadata):
        for key, value in vars(data, metadata).item():
            setatter(self, key, value)

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        input = self.inputs[idx]
        label = self.labels[idx]
        if self.transform:
            input = self.transform(input)
        if self.target_transform:
            label = self.target_transform(label)
        return input, label

    def checking_data_actuality(self):
        input_shape_Dataset = self[0][0].shape[0]
        input_shape_overview = self.input_shape

        output_shape_Dataset = torch.flatten(self[0][1]).shape[0]
        ouput_shape_overview = self.output_shape1 * self.output_shape2 * 3

        if (
            input_shape_Dataset != input_shape_overview
            or output_shape_Dataset != ouput_shape_overview
        ):
            diagnostics("NN does not run with the latest data format", "warning")
