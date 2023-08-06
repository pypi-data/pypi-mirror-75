import tensorflow as tf
from tensorflow.python import keras
from tensorflow.python.keras import backend as K

custom_objects = tf.keras.utils.get_custom_objects()

L = tf.keras.layers
initializers = keras.initializers


def integerize_shape(func):
    """ decorator, to ensure that input_shape must be int or None
    """

    def convert(item):
        if hasattr(item, '__iter__'):
            return [convert(i) for i in item]
        elif hasattr(item, 'value'):
            return item.value
        else:
            return item

    def new_func(self, input_shape):
        input_shape = convert(input_shape)
        return func(self, input_shape)

    return new_func


def sequence_masking(x, mask, mode=0, axis=None):
    """ is the function of sequence condition mask
    mask: 0-1 matrix in the shape of (batch_size, seq_len);
    mode: If it is 0, it is directly multiplied by the mask;
          If it is 1, subtract a large positive number from the padding part.
    axis: the axis of the sequence, the default is 1;
    """
    if mask is None or mode not in [0, 1]:
        return x
    else:
        if axis is None:
            axis = 1
        if axis == -1:
            axis = K.ndim(x) - 1
        assert axis > 0, 'axis muse be greater than 0'
        for _ in range(axis - 1):
            mask = K.expand_dims(mask, 1)
        for _ in range(K.ndim(x) - K.ndim(mask) - axis + 1):
            mask = K.expand_dims(mask, K.ndim(mask))
        if mode == 0:
            return x * mask
        else:
            return x - (1 - mask) * 1e12


class ConditionalRandomField(L.Layer):
    """Pure Keras realizes CRF layer
       The CRF layer is essentially a loss calculation layer with training parameters.
    """

    def __init__(self, lr_multiplier=1, **kwargs):
        super(ConditionalRandomField, self).__init__(**kwargs)
        self.lr_multiplier = lr_multiplier  # The magnification of the current layer learning rate

    @integerize_shape
    def build(self, input_shape):
        super(ConditionalRandomField, self).build(input_shape)
        output_dim = input_shape[-1]
        self._trans = self.add_weight(
            name='trans',
            shape=(output_dim, output_dim),
            initializer='glorot_uniform',
            trainable=True
        )
        if self.lr_multiplier != 1:
            K.set_value(self._trans, K.eval(self._trans) / self.lr_multiplier)

    @property
    def trans(self):
        if self.lr_multiplier != 1:
            return self.lr_multiplier * self._trans
        else:
            return self._trans

    def compute_mask(self, inputs, mask=None):
        return None

    def call(self, inputs, mask=None):
        if mask is not None:
            mask = K.cast(mask, K.floatx())

        return sequence_masking(inputs, mask, 1, 1)

    def target_score(self, y_true, y_pred):
        """Calculate the relative probability of the target path (not normalized yet)
        Key points: score by label plus transition probability score.
        """
        point_score = tf.einsum('bni,bni->b', y_true, y_pred)  # 逐标签得分
        trans_score = tf.einsum(
            'bni,ij,bnj->b', y_true[:, :-1], self.trans, y_true[:, 1:]
        )  # Tag transfer score
        return point_score + trans_score

    def log_norm_step(self, inputs, states):
        """Recursively calculate the normalization factor
        Key points: 1. Recursive calculation; 2. Use logsumexp to avoid overflow.
        """
        inputs, mask = inputs[:, :-1], inputs[:, -1:]
        states = K.expand_dims(states[0], 2)  # (batch_size, output_dim, 1)
        trans = K.expand_dims(self.trans, 0)  # (1, output_dim, output_dim)
        outputs = tf.reduce_logsumexp(
            states + trans, 1
        )  # (batch_size, output_dim)
        outputs = outputs + inputs
        outputs = mask * outputs + (1 - mask) * states[:, :, 0]
        return outputs, [outputs]

    def dense_loss(self, y_true, y_pred):
        """y_true needs to be in one hot form
        """
        # Export mask and convert texts type
        mask = K.all(K.greater(y_pred, -1e6), axis=2, keepdims=True)
        mask = K.cast(mask, K.floatx())
        # Calculate the target score
        y_true, y_pred = y_true * mask, y_pred * mask
        target_score = self.target_score(y_true, y_pred)
        # Recursively calculate log Z
        init_states = [y_pred[:, 0]]
        y_pred = K.concatenate([y_pred, mask], axis=2)
        input_length = K.int_shape(y_pred[:, 1:])[1]
        log_norm, _, _ = K.rnn(
            self.log_norm_step,
            y_pred[:, 1:],
            init_states,
            input_length=input_length
        )  # Log Z vector of the last step
        log_norm = tf.reduce_logsumexp(log_norm, 1)
        # Calculate loss -log p
        return log_norm - target_score

    def sparse_loss(self, y_true, y_pred):
        """y_true needs to be an integer (not one hot)
        """
        # y_true Need to re-clarify shape and dtype
        y_true = K.reshape(y_true, K.shape(y_pred)[:-1])
        y_true = K.cast(y_true, 'int32')
        # Convert to one hot
        y_true = K.one_hot(y_true, K.shape(self.trans)[0])
        return self.dense_loss(y_true, y_pred)

    def dense_accuracy(self, y_true, y_pred):
        """Displays the frame-by-frame accuracy function during training, excluding the influence of mask
        Here y_true needs to be in one hot form
        """
        y_true = K.argmax(y_true, 2)
        return self.sparse_accuracy(y_true, y_pred)

    def sparse_accuracy(self, y_true, y_pred):
        """Displays the frame-by-frame accuracy function during training, excluding the influence of mask
        Here y_true needs to be in integer form (not one hot)
        """
        # Export mask and convert texts type
        mask = K.all(K.greater(y_pred, -1e6), axis=2)
        mask = K.cast(mask, K.floatx())
        # y_true Need to re-clarify shape and dtype
        y_true = K.reshape(y_true, K.shape(y_pred)[:-1])
        y_true = K.cast(y_true, 'int32')
        # Take the largest label by label to roughly evaluate the training effect
        y_pred = K.cast(K.argmax(y_pred, 2), 'int32')
        isequal = K.cast(K.equal(y_true, y_pred), K.floatx())
        return K.sum(isequal * mask) / K.sum(mask)

    def get_config(self):
        config = {
            'lr_multiplier': self.lr_multiplier,
        }
        base_config = super(ConditionalRandomField, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class MaximumEntropyMarkovModel(L.Layer):
    """ (Bidirectional) Maximum Entropy Hidden Markov Model
    Function and usage are similar to CRF, but faster and simpler than CRF.
    """

    def __init__(self, lr_multiplier=1, hidden_dim=None, **kwargs):
        super(MaximumEntropyMarkovModel, self).__init__(**kwargs)
        self.lr_multiplier = lr_multiplier  # The magnification of the current layer learning rate
        self.hidden_dim = hidden_dim  # If it is not None, decompose the transfer matrix with low rank

    @integerize_shape
    def build(self, input_shape):
        super(MaximumEntropyMarkovModel, self).build(input_shape)
        output_dim = input_shape[-1]

        if self.hidden_dim is None:
            self._trans = self.add_weight(
                name='trans',
                shape=(output_dim, output_dim),
                initializer='glorot_uniform',
                trainable=True
            )
            if self.lr_multiplier != 1:
                K.set_value(
                    self._trans,
                    K.eval(self._trans) / self.lr_multiplier
                )
        else:
            self._l_trans = self.add_weight(
                name='l_trans',
                shape=(output_dim, self.hidden_dim),
                initializer='glorot_uniform',
                trainable=True
            )
            self._r_trans = self.add_weight(
                name='r_trans',
                shape=(output_dim, self.hidden_dim),
                initializer='glorot_uniform',
                trainable=True
            )

            if self.lr_multiplier != 1:
                K.set_value(
                    self._l_trans,
                    K.eval(self._l_trans) / self.lr_multiplier
                )
                K.set_value(
                    self._r_trans,
                    K.eval(self._r_trans) / self.lr_multiplier
                )

    @property
    def trans(self):
        if self.lr_multiplier != 1:
            return self.lr_multiplier * self._trans
        else:
            return self._trans

    @property
    def l_trans(self):
        if self.lr_multiplier != 1:
            return self.lr_multiplier * self._l_trans
        else:
            return self._l_trans

    @property
    def r_trans(self):
        if self.lr_multiplier != 1:
            return self.lr_multiplier * self._r_trans
        else:
            return self._r_trans

    def compute_mask(self, inputs, mask=None):
        return None

    def call(self, inputs, mask=None):
        if mask is not None:
            mask = K.cast(mask, K.floatx())

        return sequence_masking(inputs, mask, 1, 1)

    def reverse_sequence(self, inputs, mask=None):
        if mask is None:
            return [x[:, ::-1] for x in inputs]
        else:
            length = K.cast(K.sum(mask, 1), 'int32')
            return [tf.reverse_sequence(x, length, seq_axis=1) for x in inputs]

    def basic_loss(self, y_true, y_pred, go_backwards=False):
        """y_true needs to be an integer (not one hot)
        """
        # Export mask and convert texts type
        mask = K.all(K.greater(y_pred, -1e6), axis=2)
        mask = K.cast(mask, K.floatx())
        # y_true Need to re-clarify shape and dtype
        y_true = K.reshape(y_true, K.shape(y_pred)[:-1])
        y_true = K.cast(y_true, 'int32')
        # Reverse related
        if self.hidden_dim is None:
            if go_backwards:  # Whether to reverse the sequence
                y_true, y_pred = self.reverse_sequence([y_true, y_pred], mask)
                trans = K.transpose(self.trans)
            else:
                trans = self.trans
            histoty = K.gather(trans, y_true)
        else:
            if go_backwards:  # Whether to reverse the sequence
                y_true, y_pred = self.reverse_sequence([y_true, y_pred], mask)
                r_trans, l_trans = self.l_trans, self.r_trans
            else:
                l_trans, r_trans = self.l_trans, self.r_trans
            histoty = K.gather(l_trans, y_true)
            histoty = tf.einsum('bnd,kd->bnk', histoty, r_trans)
        # Calculate loss
        histoty = K.concatenate([y_pred[:, :1], histoty[:, :-1]], 1)
        y_pred = (y_pred + histoty) / 2
        loss = K.sparse_categorical_crossentropy(
            y_true, y_pred, from_logits=True
        )
        return K.sum(loss * mask) / K.sum(mask)

    def sparse_loss(self, y_true, y_pred):
        """y_true needs to be an integer (not one hot)
        """
        loss = self.basic_loss(y_true, y_pred, False)
        loss = loss + self.basic_loss(y_true, y_pred, True)
        return loss / 2

    def dense_loss(self, y_true, y_pred):
        """y_true needs to be in one hot form
        """
        y_true = K.argmax(y_true, 2)
        return self.sparse_loss(y_true, y_pred)

    def basic_accuracy(self, y_true, y_pred, go_backwards=False):
        """Displays the frame-by-frame accuracy function during training, excluding the influence of mask
        Here y_true needs to be in integer form (not one hot)
        """
        # Export mask and convert texts type
        mask = K.all(K.greater(y_pred, -1e6), axis=2)
        mask = K.cast(mask, K.floatx())
        # y_true Need to re-clarify shape and dtype
        y_true = K.reshape(y_true, K.shape(y_pred)[:-1])
        y_true = K.cast(y_true, 'int32')
        # Reverse related
        if self.hidden_dim is None:
            if go_backwards:  # Whether to reverse the sequence
                y_true, y_pred = self.reverse_sequence([y_true, y_pred], mask)
                trans = K.transpose(self.trans)
            else:
                trans = self.trans
            histoty = K.gather(trans, y_true)
        else:
            if go_backwards:  # Whether to reverse the sequence
                y_true, y_pred = self.reverse_sequence([y_true, y_pred], mask)
                r_trans, l_trans = self.l_trans, self.r_trans
            else:
                l_trans, r_trans = self.l_trans, self.r_trans
            histoty = K.gather(l_trans, y_true)
            histoty = tf.einsum('bnd,kd->bnk', histoty, r_trans)
        # Calculate the label-by-label accuracy
        histoty = K.concatenate([y_pred[:, :1], histoty[:, :-1]], 1)
        y_pred = (y_pred + histoty) / 2
        y_pred = K.cast(K.argmax(y_pred, 2), 'int32')
        isequal = K.cast(K.equal(y_true, y_pred), K.floatx())
        return K.sum(isequal * mask) / K.sum(mask)

    def sparse_accuracy(self, y_true, y_pred):
        """Displays the frame-by-frame accuracy function during training, excluding the influence of mask
        Here y_true needs to be in integer form (not one hot)
        """
        accuracy = self.basic_accuracy(y_true, y_pred, False)
        accuracy = accuracy + self.basic_accuracy(y_true, y_pred, True)
        return accuracy / 2

    def dense_accuracy(self, y_true, y_pred):
        """Displays the frame-by-frame accuracy function during training, excluding the influence of mask
        Here y_true needs to be in one hot form
        """
        y_true = K.argmax(y_true, 2)
        return self.sparse_accuracy(y_true, y_pred)

    def get_config(self):
        config = {
            'lr_multiplier': self.lr_multiplier,
            'hidden_dim': self.hidden_dim,
        }
        base_config = super(MaximumEntropyMarkovModel, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))
