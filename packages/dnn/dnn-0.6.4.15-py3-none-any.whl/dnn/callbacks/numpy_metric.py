from tensorflow.keras.callbacks import Callback
from rs4.termcolor import tc, stty_size
from tensorflow.python.keras import backend as K
from . import base

class NumpyMetricCallback (base.ValiadtionSet, Callback):
    def __init__(self, func, validation_data):
        Callback.__init__(self)
        base.ValiadtionSet.__init__ (self, validation_data)
        self.func = func
        self.info = None

    def get_info (self):
        return self.info

    def on_epoch_end (self, epoch, logs):
        logs = logs or {}
        self.make_predictions ()
        self.info = self.func (self.ys, self.logits, logs)
