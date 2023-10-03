class Flattener(object):
    def __init__(self, memory):
        self.memory = memory

    def __call__(self, data):
        self.memory.append(data.shape[0])
        return data.reshape(data.shape[0], -1)


class UndoFlattener(object):
    def __init__(self, memory, original_shape):
        self.memory = memory
        self.original_shape = original_shape

    def __call__(self, data):
        shape = (self.memory.pop(), *self.original_shape)
        return data.reshape(shape)
