

__all__ = ["CNN_v1"]

from tensorflow.keras import layers
import tensorflow as tf
from rxwgan.metrics import sp_metric



class CNN_v1( object ):

  def __init__(self, discr_path=None):

      self.height     = 128
      self.width      = 128
      if discr_path:
        self.model = tf.keras.models.load_model(discr_path)
      else:
        self.compile()


  def predict(self, samples):
    return self.model.predict(samples, verbose=1)


  def compile(self):

      ip = layers.Input(shape=( self.height,self.width,1))
      # TODO Add other normalization scheme as mentioned in the article
      # Input (None, 3^2*2^5 = 1 day = 288 samples, 1)
      y = layers.Conv2D(256, (5,5), strides=(2,2), padding='same', kernel_initializer='he_uniform', data_format='channels_last', input_shape=(self.height,self.width,1))(ip)
      #y = layers.BatchNormalization()(y)
      y = layers.Activation('relu')(y)
      y = layers.Dropout(rate=0.3, seed=1)(y)
      # Output (None, 3^2*2^3, 64)
      y = layers.Conv2D(128, (5,5), strides=(2,2), padding='same', kernel_initializer='he_uniform')(y)
      #y = layers.BatchNormalization()(y)
      y = layers.Activation('relu')(y)
      y = layers.Dropout(rate=0.3, seed=1)(y)
      # Output (None, 3^2*2^3, 64)
      y = layers.Conv2D(64, (5,5), strides=(2,2), padding='same', kernel_initializer='he_uniform')(y)
      #y = layers.BatchNormalization()(y)
      y = layers.Activation('relu')(y)
      y = layers.Dropout(rate=0.3, seed=1)(y)
      # Output (None, 3^2*2, 128)
      y = layers.Flatten()(y)
      # Output (None, 3*256)
      y = layers.Dense(64, activation='relu')(y)
      out = layers.Dense(1, activation='sigmoid')(y)
      # Output (None, 1)
      model = tf.keras.Model(ip, out)
      
      model.compile(optimizer="adam",loss='binary_crossentropy',metrics=['acc',sp_metric])


      model.summary()
      self.model = model