
from tensorflow.python import keras

from kolibri.dnn.layers.att_wgt_avg_layer import AttentionWeightedAverage, AttWgtAvgLayer
from kolibri.dnn.layers.att_wgt_avg_layer import AttentionWeightedAverageLayer
from kolibri.dnn.layers.folding_layer import FoldingLayer
from kolibri.dnn.layers.kmax_pool_layer import KMaxPoolingLayer, KMaxPoolLayer, KMaxPooling
from kolibri.dnn.layers.non_masking_layer import NonMaskingLayer
from kapre.time_frequency import Melspectrogram
from kapre.utils import Normalization2D
L = keras.layers

if __name__ == "__main__":
    print("Hello world")
