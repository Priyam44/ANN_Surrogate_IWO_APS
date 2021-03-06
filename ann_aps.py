# -*- coding: utf-8 -*-
"""ANN_APS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u8y6DY6nL_pfM4kNPJWtbUULQqvuSME5
"""

import math,numpy as np,matplotlib.pyplot as plt, tensorflow as tf
from tensorflow.python.framework import ops
import pandas as pd
from google.colab import drive
drive.mount('/gdrive')

pdf=np.load("/gdrive/My Drive/svr.npy",allow_pickle=True)
pdf_new=pd.read_csv("/gdrive/My Drive/ANN Data Set/New Data using Forces/Airfoil_28_131119/data.csv")
pdf_new2=pd.read_csv("/gdrive/My Drive/ANN Data Set/New Data using Forces/Airfoil_28_131119/data.csv")

np.savetxt("foo.csv",pdf,delimiter=',')

print(pdf)
plt.plot(pdf[0],pdf[1])
plt.show()

a=pdf_new.values
ma=[a[0][-1]]
mi=[]
j=0
for i in range(a.shape[0]-1):
  if a[i+1][-1]>a[i][-1]:
    ma.append(a[i+1][-1])
    j=0
  if(j==10):
    mi.append(a[i][-1])
  j+=1
plt.plot(np.arange(len(ma)),ma)
plt.plot(np.arange(len(mi)),mi)
plt.show()
ma=np.array(ma)
mi=np.array(mi)
np.save("max.npy",ma)
np.save("min.npy",mi)

from sklearn.utils import shuffle
pdf_new=pdf_new.append(pdf_new2,ignore_index=True)
print(pdf_new)
#pdf_new=shuffle(pdf_new)

X=pdf_new.drop('F',axis=1)
y=pdf_new['F']
print(y)
y=y.values
plt.plot(np.arange(0,1456),y)
plt.show()

print(pdf_new)

#print(pdf_new.head())
X=pdf_new.drop('F',axis=1)
y=pdf_new['F']

#normalizing values
# x=X.values
# x=x.T
# k=np.std(x,1).reshape(5,1)**2
# X_norm=(x-np.mean(x,1).reshape(5,1))/k
# X_norm=X_norm.T
X=np.round(X.values,5)
y_scale,indices=np.unique(np.round(y.values,5),return_index=True)
y_scale=y_scale.reshape(y_scale.shape[0],1)
#y_scale=(y_scale*1000)%1000
X_scale=np.empty((y_scale.shape[0],5))
print(X_scale.shape)
j=0
print(X[0])
for i in indices:
  X_scale[j]=X[i]
  j+=1
shuffle=np.append(X_scale,y_scale,axis=1)
np.random.shuffle(shuffle)
y_scale=shuffle[:,-1].reshape(shuffle.shape[0],1)
X_scale=shuffle[:,:5]
from sklearn import preprocessing
X_scale = preprocessing.scale(X_scale)
#y_scale = preprocessing.scale(y_scale)
X_test = X_scale[150:]
y_test = y_scale[150:]

print(y_scale.shape)
print(y_test.shape)
print(X_scale.shape)
print(X_test.shape)
print(y_scale)

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.models import Sequential
from keras.layers import Dense

def NNRegressionAdam1():
  model = tf.keras.Sequential()
  # Adds a densely-connected layer with 64 units to the model:
  model.add(layers.Dense(64, input_dim=5, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01), bias_regularizer=tf.keras.regularizers.l2(0.001)))
  #keras.layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None)
  #model.add(layers.Dropout(0.6))
# Add another:
  #model.add(layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01), bias_regularizer=tf.keras.regularizers.l2(0.001)))
  #model.add(layers.Dropout(0.6))
  # #keras.layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None)
    # # Add another:
  #model.add(layers.Dense(4, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01), bias_regularizer=tf.keras.regularizers.l2(0.001)))
  # #keras.layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None)
  #model.add(layers.Dropout(0.2))
    # Add the output layer
  model.add(layers.Dense(1))
  
  #optimizer = tf.keras.optimizers.RMSprop(lr=0.00001)
  #optimizer = tf.keras.optimizers.SGD(learning_rate=0.1, momentum=0.0, nesterov=False)
  #optimizer=tf.keras.optimizers.GD(learning_rate=0.001)
  optimizer=keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)
  model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['mae'])
  return model

X1,y1=X_scale[0:300],y_scale[0:300]
X2,y2=X_scale[300:600],y_scale[300:600]
X3,y3=X_scale[600:900],y_scale[600:900]
X4,y4=X_scale[900:1200],y_scale[900:1200]
X5,y5=X_scale[1200:1500],y_scale[1200:1500]
X6,y6=X_scale[1500:],y_scale[1500:]
print(y1)
X_list=[[X1,y1.reshape(300,1)],[X2,y2.reshape(300,1)],[X3,y3.reshape(300,1)],[X4,y4.reshape(300,1)],[X5,y5.reshape(300,1)],[X6,y6.reshape(487,1)]]
#print(y1)
X_test,y_test,X_train,y_train=0,0,0,0
train_mse=0
test_mse=0
models=[]
for i in range(0,6):
    print("run:",i+1)
    X_test=X_list[i][0]
    y_test=X_list[i][1]
    X_train=np.empty((0,5))
    y_train=np.empty((0,1))
    for j in range(0,i):
        X_train=np.append(X_train,X_list[j][0],axis=0)
        y_train=np.append(y_train,X_list[j][1],axis=0)
    for j in range(i+1,6):
        X_train=np.append(X_train,X_list[j][0],axis=0)
        y_train=np.append(y_train,X_list[j][1],axis=0)
    model=NNRegressionAdam1()
    print("train run")
    history=model.fit(X_train, y_train, validation_split=0, batch_size=32, epochs=5000)
    models.append(model)
    train_mse+=history.history['loss'][-1]
    print("test run")
    test_mse+=model.evaluate(X_test,y_test)[0]
train_mse/=5
test_mse/=5
print("Train_mse",train_mse)
print("Test_mse",test_mse)

# from keras.wrappers.scikit_learn import KerasRegressor

# tf.set_random_seed(2)

# estimator_adam = KerasRegressor(build_fn=NNRegressionAdam1)
# # earlystopper = tf.keras.callbacks.EarlyStopping(monitor='cosine_proximity', baseline=0.99, verbose=True)
estimator_adam=NNRegressionAdam1()
print(y_scale.shape)
#estimator.fit(X_train, y_train, validation_split=0.1, callbacks=[earlystopper], batch_size=1024)
history_adam = estimator_adam.fit(X_scale, y_scale, validation_split=0.2,batch_size=64, epochs=5000)
# loss: 0.3994 - mean_absolute_error: 0.4421 - val_loss: 0.6829 - val_mean_absolute_error: 0.6107

estimator_adam.evaluate(X_scale,y_scale)

import matplotlib.pyplot as plt
# Plot training & validation loss values
plt.plot(history_adam.history['loss'])
plt.plot(history_adam.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

a=estimator_adam.predict(X_test)
print(np.around(np.array([a,y_test]).T,5))

estimator_adam.save("mymodel2.h5")

np.save("hist2.npy",history_adam.history)

a=np.load("hist2.npy",allow_pickle=True)

print(a)

