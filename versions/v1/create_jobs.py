

import numpy as np
#from rxwgan.stratified_kfold import stratified_train_val_test_splits
#from sklearn.model_selection import KFold
import json
import os



output_path = 'job.Shenzhen.model_cnn_v1.10tests.10sorts'
n_tests = 10
n_sorts = 10
seed = 512

os.makedirs(output_path, exist_ok=True)

for test in range(n_tests):
    for sort in range(n_sorts):

        d = {   
                'sort'   : sort,
                'test'   : test,
                'seed'   : seed,
            }

        o = output_path + '/job.test_%d.sort_%d.json'%(test,sort)
        with open(o, 'w') as f:
            json.dump(d, f)





