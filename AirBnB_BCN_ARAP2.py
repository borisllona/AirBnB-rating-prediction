import pandas as pd
import numpy as np
import random as rm
import sys
import argparse

attributeslist = ['@RELATION overall_satisfaction','',
'@ATTRIBUTE room_type {PrivateRoom,EntireHome,SharedRoom}',
'@ATTRIBUTE neighborhood {LesCorts,SantsMontjuic,CiutatVella,SantMarti,Gracia,Horta,Sarria,Eixample,SantAndreu,NouBarris}',
'@ATTRIBUTE reviews NUMERIC','@ATTRIBUTE overall_satisfaction NUMERIC',
'@ATTRIBUTE accommodates NUMERIC','@ATTRIBUTE bedrooms NUMERIC',
'@ATTRIBUTE price NUMERIC','@ATTRIBUTE latitude NUMERIC','@ATTRIBUTE longitude NUMERIC','','@DATA']

def deletePreviousSets(args):
    for i in [args.test_output,args.train_output]:
        with open(i, 'w') as f:
            for el in attributeslist: f.write(el+'\n')
            f.close()

def writeToFile(setType,files):
        with open(files, 'a') as f:
            for index,row in setType.iterrows():
                for n, el in enumerate(row):
                    f.write(str(el))
                    if n != len(row)-1: f.write(',')
                f.write('\n')
        f.close()

def format_dataset(df):
    #print(df.groupby('neighborhood').size().sort_values(ascending=False))

    #Replaces the posible problematic names to ones without spaces, accents and strange characters
    df = df.replace(["Shared room","Entire home/apt","Private room","Les Corts","Sant Andreu","Nou Barris",
    "Sants-Montjuïc","Ciutat Vella","Sant Martí","Gràcia","Horta-Guinardó","Sarrià-Sant Gervasi"],
    ["SharedRoom","EntireHome","PrivateRoom","LesCorts","SantAndreu","NouBarris",
    "SantsMontjuic","CiutatVella","SantMarti","Gracia","Horta","Sarria"])

    #Maps the overal satisfaction from range 1-5 to 1-10. In order to avoid decimal numbers
    df['overall_satisfaction'] = df['overall_satisfaction'].map(lambda x: x*2)

    #Rounds both latitude and longitude to 3 decimals (decision explained in the report of the practice)
    df['latitude'] = df['latitude'].map(lambda x: round(x, 3))
    df['longitude'] = df['longitude'].map(lambda x: round(x, 3))

    return df 

def parse_command_line_arguments(argv=None):
    #Parses the arguments needed. nargs="?" means the argument is optional and deafult and type are useful methods too.

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("dataset",help="Path to the dataset.")
    parser.add_argument("train_output",nargs="?",default="trainSet.arff",help="Name of the arff file were train output will be saved")
    parser.add_argument("test_output",nargs="?",default="testSet.arff",help="Name of the arff file were test output will be saved")
    parser.add_argument("seed",nargs="?",default=53932,type=int,help="Seed for the random test-train split")
    parser.add_argument("percentage",nargs="?",default=0.75,type=float,help="Percentage of the training set range 0-1")
    
    return parser.parse_args(args=argv)

def main(argv=None):
    
    args = parse_command_line_arguments(argv)    
    
    #Previous dataset values are deleted and we write the header, used in arff files to specify the variables used.
    deletePreviousSets(args)
    
    df = format_dataset(pd.read_csv(args.dataset))

    #df.sample(), Return a random sample of items from an axis of object.
    train_set = df.sample(frac=args.percentage, random_state=args.seed)
    test_set = df.drop(train_set.index)

    #Write the train and test dataframes into the specified files
    writeToFile(train_set,args.train_output)
    writeToFile(test_set,args.test_output)

if __name__ == "__main__":
    sys.exit(main())
