# Neural network - input -> features of state, output -> action distribution and win rate

from keras.models import Model
from keras.losses import mean_squared_error, binary_crossentropy
from keras.layers import Conv2D, Flatten, Dense, MaxPooling2D, Input, BatchNormalization, Dropout,Conv3D,Concatenate
import tensorflow as tf
from sklearn.model_selection import train_test_split

class Network:
    def __init__(self, input_shape,action_distribution_len):
        self.in_shape = input_shape
        self.out_shape = action_distribution_len
        self.network = None

    def initialize_network(self):

        inp = Input(shape=self.in_shape) # (num_features,) 

        full = Dense(256, activation='relu',kernel_regularizer=tf.keras.regularizers.l2(0.01))(inp)
        batch = BatchNormalization()(full)
        full_1 = Dense(128, activation='relu')(batch)
        full_2 = Dense(64)(full_1)
        out = Dense(self.out_shape, activation='softmax',name='action_dis')(full_2)
        network = Model(inputs=[inp], outputs =[out], name='Features2WinRate&ActDis')
        network.compile(
            loss = ['categorical_crossentropy'],
            optimizer = tf.keras.optimizers.Adam(),
            )
        self.network = network
        print(network.summary())

    def _read_data(self, game_array,action_ds):
        # game_array = ... # Array of shape (N, num_feature_layers, height, width) 
        # action_ds = ...  # Array of size (N,1)


        print('shape of input data: ',game_array.shape)
        print('shape of output data: ',action_ds.shape)


        X_train,X_test, y_train, y_test = train_test_split(game_array,action_ds, test_size=0.05) 



        print('Train: Shape of X:{}, Shape of y: {}'.format(X_train.shape, y_train.shape))
        print('Test: Shape of X:{}, Shape of y: {}'.format(X_test.shape, y_test.shape))


        return X_train,X_test, y_train, y_test
        
    def train_network(self, X,y,epochs):
        X_train,X_test, y_train, y_test = self._read_data(X,y)
        self.network.fit(
            x = X_train,
            y = y_train,
            validation_data = ([X_test], [y_test]),
            epochs = epochs,
            batch_size=16
        )

    def save_network(self,name):
        self.network.save('saved_models/{}.tf'.format(name))

