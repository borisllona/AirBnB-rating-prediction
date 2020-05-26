import pandas as pd
import numpy as np
import random as rm
import sys
import argparse

attributeslist = ['@RELATION overall_satisfaction','',
'@ATTRIBUTE room_type {Private_room,Entire_home/apt,Shared_room}',
'@ATTRIBUTE neighborhood {LesCorts,SantsMontjuic,CiutatVella,SantMarti,Gracia,Horta,Sarria,Eixample,SantAndreu,NouBarris}',
'@ATTRIBUTE reviews NUMERIC','@ATTRIBUTE overall_satisfaction NUMERIC',
'@ATTRIBUTE accommodates NUMERIC','@ATTRIBUTE bedrooms NUMERIC',
'@ATTRIBUTE price NUMERIC','@ATTRIBUTE latitude NUMERIC','@ATTRIBUTE longitude NUMERIC','','@DATA']

def deletePreviousSets():
    for i in ['testSet.arff','trainSet.arff']:
        with open(i, 'w') as f:
            for el in attributeslist: f.write(el+'\n')
            f.close()

def writteToFile(setType,files):
        with open(files, 'a') as f:
            for index,row in setType.iterrows():
                for n, el in enumerate(row):
                    f.write(str(el))
                    if n != len(row)-1: f.write(',')
                f.write('\n')
        f.close()

def format_dataset(df):
    #print(df.groupby('neighborhood').size().sort_values(ascending=False))

    df = df.replace(["Shared room","Entire home/apt","Private room","Les Corts","Sant Andreu","Nou Barris",
    "Sants-Montjuïc","Ciutat Vella","Sant Martí","Gràcia","Horta-Guinardó","Sarrià-Sant Gervasi"],
    ["SharedRoom","EntireHome/apt","PrivateRoom","LesCorts","SantAndreu","NouBarris",
    "SantsMontjuic","CiutatVella","SantMarti","Gracia","Horta","Sarria"])

    df['overall_satisfaction'] = df['overall_satisfaction'].map(lambda x: x*2)
    df['latitude'] = df['latitude'].map(lambda x: round(x, 3))
    df['longitude'] = df['longitude'].map(lambda x: round(x, 3))

    return df 

def parse_command_line_arguments(argv=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("dataset",help="Path to the dataset.")
    parser.add_argument("seed",nargs="?",default=53932,type=int,help="Seed for the random test-train split")
    parser.add_argument("percentage",nargs="?",default=0.75,type=float,help="Percentage of the training set")
    
    return parser.parse_args(args=argv)

def main(argv=None):
    args = parse_command_line_arguments(argv)    
    deletePreviousSets()
    
    df = format_dataset(pd.read_csv(args.dataset))

    #df.sample(), Return a random sample of items from an axis of object.
    train_set = df.sample(frac=args.percentage, random_state=args.seed)
    test_set = df.drop(train_set.index)

    writteToFile(train_set,'trainSet.arff')
    writteToFile(test_set,'testSet.arff')

if __name__ == "__main__":
    sys.exit(main())
