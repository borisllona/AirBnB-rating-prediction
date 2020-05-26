import pandas as pd
import numpy as np
import random as rm
import sys
import argparse

files = ['trainSet.arff','testSet.arff']

attributeslist = ['@RELATION overall_satisfaction','',
'@ATTRIBUTE room_type {Private_room,Entire_home/apt,Shared_room}',
'@ATTRIBUTE neighborhood {Eixample,Ciutat Vella,Sants-Montjuïc,Sant Martí,Gràcia}',
'@ATTRIBUTE reviews NUMERIC','@ATTRIBUTE overall_satisfaction NUMERIC',
'@ATTRIBUTE accommodates NUMERIC','@ATTRIBUTE bedrooms NUMERIC',
'@ATTRIBUTE price NUMERIC','@ATTRIBUTE latitude NUMERIC','@ATTRIBUTE longitude NUMERIC','','@DATA']

def deletePreviousSets():
    for i in files:
        with open(i, 'w') as f:
            for el in attributeslist: f.write(el+'\n')
            f.close()

def writteTrain(train_set):
        with open(files[0], 'a') as f:
            for index,row in train_set.iterrows():
                for n, el in enumerate(row):
                    f.write(str(el))
                    if n != len(row)-1: f.write(',')
                f.write('\n')
        f.close()

def writteTest(test_set):
        with open(files[1], 'a') as f:
            for index,row in test_set.iterrows():
                for n, el in enumerate(row):
                    f.write(str(el))
                    if n != len(row)-1: f.write(',')
                f.write('\n')
        f.close()

def parse_command_line_arguments(argv=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("dataset",help="Path to the dataset.")
    parser.add_argument("seed",nargs="?",default=3932,help="Seed for the random test-train split")
    parser.add_argument("percentage",nargs="?",default=0.75,help="Percentage of the training set")
    
    return parser.parse_args(args=argv)

def main(argv=None):
    args = parse_command_line_arguments(argv)    
    deletePreviousSets()

    df = pd.read_csv(args.dataset)
    #a lot to format
    df = df.replace(["Shared room","Entire home/apt","Private room"],
    ["Shared_room","Entire_home/apt","Private_room"])

    #df.sample(), Return a random sample of items from an axis of object.
    train_set = df.sample(frac=args.percentage, random_state=args.seed)
    test_set = df.drop(train_set.index)

    writteTrain(train_set)
    writteTest(test_set)

if __name__ == "__main__":
    sys.exit(main())
