class Sequencer(object):
    def __init__(self, sequence_length):
        self.sequence_length = sequence_length

    def __call__(self, data):
        return data.reshape(data.shape[0], self.sequence_length, -1)


class UndoSequencer(object):
    def __init__(self):
        pass

    def __call__(self, data):
        return data.reshape(data.shape[0], data.shape[1] * data.shape[2])
