import torch
from torch import nn


class AudioTransformer(nn.Module):
    def __init__(self,
                 input_width,
                 input_height,
                 hidden_size,
                 num_layers,
                 num_heads,
                 kernel_size,
                 stride,
                 dropout_rate=0.1,
                 pre_transforms=None,
                 post_transforms=None
     ):
        super(AudioTransformer, self).__init__()

        self.conv = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=kernel_size, stride=stride)

        compressed_width = int((input_width - kernel_size) / stride) + 1
        compressed_height = int((input_height - kernel_size) / stride) + 1
        self.embedding = nn.Linear(compressed_width * compressed_height, hidden_size)

        encoder_layer = nn.TransformerEncoderLayer(hidden_size, num_heads)
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers)
        self.encoder_dropout = nn.Dropout(dropout_rate)

        decoder_layer = nn.TransformerDecoderLayer(hidden_size, num_heads)
        self.decoder = nn.TransformerDecoder(decoder_layer, num_layers)
        self.decoder_dropout = nn.Dropout(dropout_rate)

        # bug, if sequence != 1, then the output is not the same size as the input
        self.output_layer = nn.Linear(hidden_size, input_width * input_height)
        self.pre_transforms = pre_transforms
        self.post_transforms = post_transforms

    def forward(self, inputs, memory=None):
        encoded = self.encode(inputs)
        return self.decode(encoded, memory)

    def encode(self, inputs):
        inputs = inputs.unsqueeze(1)
        inputs = self.conv(inputs)
        inputs = inputs.squeeze(1)
        if self.pre_transforms is not None:
            inputs = self.pre_transforms(inputs)

        embedded = self.embedding(inputs)
        embedded = embedded.permute(1, 0, 2)
        encoded = self.encoder(embedded)
        return self.encoder_dropout(encoded)

    def decode(self, encoded, memory=None):
        if memory is None:
            memory = encoded

        decoded = self.decoder(encoded, memory)
        decoded = self.decoder_dropout(decoded)
        output = self.output_layer(decoded)
        output = output.permute(1, 0, 2)

        if self.post_transforms is not None:
            output = self.post_transforms(output)
        return output

    def save(self, path):
        torch.save(self.state_dict(), path)

    def load(self, path, device=torch.device('cpu')):
        self.load_state_dict(torch.load(path, map_location=device))
