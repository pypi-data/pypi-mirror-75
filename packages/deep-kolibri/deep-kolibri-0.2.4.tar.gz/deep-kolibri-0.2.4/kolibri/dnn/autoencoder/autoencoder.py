from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Dense

from kolibri.dnn.autoencoder.base_autoencoder import BaseAutoencoder


class Autoencoder(BaseAutoencoder):

    @classmethod
    def get_default_hyper_parameters(cls):
        return {
            'layer_multiplyer': 2,
            'hidden': {
                'units': 40,
                'activation': 'relu'
            },
            'latent':{
                'units': 10,
                'activation': 'relu'
                       },
            'output': {
                'activation': 'relu'
                }
                }


    def build_model_arc(self):

        input_layer = Input(shape=(self.input_dim,))

        encoder = Dense(**self.hyper_parameters['hidden'])(input_layer)
        latent = Dense(**self.hyper_parameters['latent'])(encoder)

        latent_inputs = Input(shape=(self.hyper_parameters['latent']['units'],), name='decoder_input')

        decoder = Dense(**self.hyper_parameters['hidden'])(latent_inputs)
        output = Dense(self.input_dim, **self.hyper_parameters['output'])(decoder)

        self.encoder=Model(inputs=input_layer, outputs=latent)

        self.encoder.summary()
        # instantiate decoder model

        self.decoder = Model(latent_inputs, output, name='decoder')
        self.decoder.summary()

        # autoencoder = encoder + decoder
        # instantiate autoencoder model
        self.autoencoder = Model(input_layer,
                            self.decoder(self.encoder(input_layer)),
                            name='autoencoder')


if __name__ == "__main__":


    from kolibri.data.corpus.corpus import CreditCardFraud



    corpus = CreditCardFraud()
    train_x=corpus.X

    model = Autoencoder()
    model.build_model(train_x[:100])



    epochs = 4
    history = None
    model.fit(train_x[0:20000], epochs=epochs)

    model.evaluate(train_x[0:10000])

