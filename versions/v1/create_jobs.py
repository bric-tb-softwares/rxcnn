

import numpy as np
import argparse
#from rxwgan.stratified_kfold import stratified_train_val_test_splits
#from sklearn.model_selection import KFold
import json

parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-o','--output', action='store', 
    dest='output', required = True,
    help = "output file")

parser.add_argument('-s','--n_sorts', action='store', 
    dest='n_sorts', required = False, default = 10, type=int, 
    help = "Number of sorts")

parser.add_argument('-t','-n_tests', action='store', 
    dest='n_tests', required = False, default = 10, type=int, 
    help = "job configuration.")

#
# Train parameters
#

parser.add_argument('--seed', action='store', 
    dest='seed', required = False, default = 512, type=int, 
    help = "Seed value to initialize the k fold stage.")



import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()
output_path = args.output
os.makedirs(output_path, exist_ok=True)

for test in range(args.n_tests):
    for sort in range(args.n_sorts):

        d = {   
                'sort'   : sort,
                'test'   : test,
                'seed'   : args.seed,
            }

        o = output_path + '/job.test_%d.sort_%d.json'%(test,sort)
        with open(o, 'w') as f:
            json.dump(d, f)





