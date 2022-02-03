#!/usr/bin/env python3

try:
  from tensorflow.compat.v1 import ConfigProto
  from tensorflow.compat.v1 import InteractiveSession
  config = ConfigProto()
  config.gpu_options.allow_growth = True
  session = InteractiveSession(config=config)
except Exception as e:
  print(e)
  print("Not possible to set gpu allow growth")



import pandas as pd
import numpy as np
import argparse
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from rxcnn.models import *
from rxcore.stratified_kfold import stratified_train_val_test_splits
import tensorflow as tf  
import json



parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-v','--volume', action='store', 
    dest='volume', required = False,
    help = "volume path")

parser.add_argument('-i','--input', action='store', 
    dest='input', required = True, default = None, 
    help = "Input image directory.")

parser.add_argument('-j','--job', action='store', 
    dest='job', required = True, default = None, 
    help = "job configuration.")





#
# Train parameters
#

parser.add_argument('--batch_size', action='store', 
    dest='batch_size', required = False, default = 64, type=int,
    help = "train batch_size")

parser.add_argument('--epochs', action='store', 
    dest='epochs', required = False, default = 1000, type=int,
    help = "Number of epochs.")

parser.add_argument('--seed', action='store', 
    dest='seed', required = False, default = 512, type=int, 
    help = "Seed value to initialize the k fold stage.")


import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()

def lock_as_completed_job(output):
  with open(output+'/.complete','w') as f:
    f.write('complete')

def lock_as_failed_job(output):
  with open(output+'/.failed','w') as f:
    f.write('failed')

try:
    job  = json.load(open(args.job, 'r'))
    sort = job['sort']
    #target = job['target']
    test = job['test']

    output_path = args.volume + '/test_%d_sort_%d'%(test,sort)


    # create models
    model = CNN_v1().model
    
    height = model.layers[0].input_shape[0][1]
    width  = model.layers[0].input_shape[0][2]

    dataframe = pd.read_csv(args.input)

    splits = stratified_train_val_test_splits(dataframe,args.seed)[test]

    training_data   = dataframe.iloc[splits[sort][0]]
    validation_data = dataframe.iloc[splits[sort][1]]

    # image generator
    datagen = ImageDataGenerator( rescale=1./255 )
    train_generator = datagen.flow_from_dataframe(training_data, directory = None,
                                                  x_col = 'raw_image_path', 
                                                  y_col = 'target',
                                                  batch_size = args.batch_size,
                                                  target_size = (height,width), 
                                                  class_mode = 'raw', 
                                                  shuffle = True,
                                                  color_mode = 'grayscale')

    val_generator   = datagen.flow_from_dataframe(validation_data, directory = None,
                                                  x_col = 'raw_image_path', 
                                                  y_col = 'target',
                                                  batch_size = args.batch_size,
                                                  class_mode = 'raw',
                                                  target_size = (height,width),
                                                  shuffle = True,
                                                  color_mode = 'grayscale')




    #
    # Create optimizer
    #

    is_test = os.getenv('LOCAL_TEST')

    stop = EarlyStopping(monitor='val_sp', mode='max', verbose=1, patience=25, restore_best_weights=True)

    history = model.fit_generator(train_generator,
                validation_data=val_generator,
                epochs=1 if is_test else 1000,
                callbacks=[stop],
                #sample_weight=sample_weight,
                shuffle=True,
                verbose=1).history

    model.save(output_path+'/discr_trained.h5')

    with open(output_path+'/history.json', 'w') as handle:
        json.dump(history, handle,indent=4)

    # necessary to work on orchestra
    lock_as_completed_job(args.volume if args.volume else '.')
    sys.exit(0)

except  Exception as e:
    print(e)
    # necessary to work on orchestra
    lock_as_failed_job(args.volume if args.volume else '.')
    sys.exit(1)