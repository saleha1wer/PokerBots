# Neural network - input -> features of state, output -> action distribution and win rate

from keras.models import Model
from keras.losses import mean_squared_error, binary_crossentropy
from keras.layers import Conv2D, Flatten, Dense, MaxPooling2D, Input, BatchNormalization, Dropout,Conv3D,Concatenate
import tensorflow as tf
from sklearn.model_selection import train_test_split

class Network:
    def __init__(self, input_shapes,action_distribution_len):
        self.in_shape_one = input_shapes[0]
        self.in_shape_two = input_shapes[1]

        self.out_shape = action_distribution_len
        self.network = None

    def initialize_network(self):

        inp_one = Input(shape=self.in_shape_one) # (num_features,) 
        inp_two = Input(shape=self.in_shape_two) # (num_features,) 

        full = Dense(32, activation='relu',kernel_regularizer=tf.keras.regularizers.l2(0.01))(inp_one)
        batch = BatchNormalization()(full)
        full_1 = Dense(20, activation='relu')(batch)
        full_2 = Dense(64, activation='relu')(inp_two)
        full_3 = Dense(40, activation='relu')(full_2)
        conc = Concatenate()([full_3,full_1])
        full_4 = Dense(20)(conc)
        out = Dense(self.out_shape, activation='softmax',name='action_dis')(full_4)
        network = Model(inputs=[inp_one,inp_two], outputs =out, name='Features2ActDis')
        network.compile(
            loss = ['categorical_crossentropy'],
            optimizer = tf.keras.optimizers.Adam(),
            )
        self.network = network
        print(network.summary())

    def _read_data(self,game_info,opponent_info,action_ds):
        # game_array = ... # Array of shape (N, num_feature_layers, height, width) 
        # action_ds = ...  # Array of size (N,1)


        print('shape of input data - 1: ',game_info.shape)
        print('shape of input data - 2: ',opponent_info.shape)
        print('shape of output data: ',action_ds.shape)
        X_train_gi,X_test_gi,X_train_oi,X_test_oi, y_train, y_test = train_test_split(game_info,opponent_info,action_ds, test_size=0.05) 

        print('Train: {}'.format(X_train_gi.shape, y_train.shape))
        print('Valid: {}'.format(X_test_gi.shape, y_test.shape))

        return X_train_gi,X_test_gi,X_train_oi,X_test_oi, y_train, y_test
        
    def train_network(self, game_array,opponent_array,y,epochs):
        X_train_game,X_test_game,X_train_opponents,X_test_opponents, y_train, y_test = self._read_data(game_array,opponent_array,y)
        self.network.fit(
            x = [X_train_game,X_train_opponents],
            y = y_train,
            validation_data = ([X_test_game,X_test_opponents], y_test),
            epochs = epochs,
            batch_size=16
        )

    def save_network(self,name):
        self.network.save('saved_models/{}.tf'.format(name))

