import pandas as pd
import numpy as np
import random as rm
import sys
import argparse

attributeslist = ['@RELATION overallSatisfaction','',
'@ATTRIBUTE roomType {PrivateRoom,EntireHome,SharedRoom}',
'@ATTRIBUTE neighborhood {LesCorts,SantsMontjuic,CiutatVella,SantMarti,Gracia,Horta,Sarria,Eixample,SantAndreu,NouBarris}',
'@ATTRIBUTE reviews ','@ATTRIBUTE overallSatisfaction {1,2,3,4,5,6,7,8,9,10}',
'@ATTRIBUTE accommodates ','@ATTRIBUTE bedrooms ',
'@ATTRIBUTE price ','@ATTRIBUTE latitude ','@ATTRIBUTE longitude ','','@DATA']

def write_headers(f):
    for atr in attributeslist:
        f.write(atr+'\n')

def write_to_file(setType,files):
        with open(files, 'w') as f:
            write_headers(f)
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

    #Maps the overal satisfaction from range 1-5 to 1-10. In order to avoid decimal numbers.
    #Also we save in the header list the possible values.

    df['overall_satisfaction'] = df['overall_satisfaction'].map(lambda x: int(x*2))
    
    #converts all atribute column to string, and then it gets the distinct values and format it.
    df['reviews'] = df['reviews'].astype(str)
    attributeslist[4]+='{'+','.join(x for x in list(map(str.strip,df.reviews.unique())))+'}'

    df['bedrooms'] = df['bedrooms'].map(lambda x: str(x)[:-2])
    attributeslist[7]+='{'+','.join(x for x in list(map(str.strip,df.bedrooms.unique())))+'}'

    df['accommodates'] = df['accommodates'].astype(str)
    attributeslist[6]+='{'+','.join(x for x in list(map(str.strip,df.accommodates.unique())))+'}'
    
    df['price'] = df['price'].map(lambda x: str(x)[:-2])
    attributeslist[8]+='{'+','.join(x for x in list(map(str.strip,df.price.unique())))+'}'

    #Rounds both latitude and longitude to 3 decimals (decision explained in the report of the practice)
    df['latitude'] = df['latitude'].map(lambda x: round(x, 3))
    lat = pd.Series(df.latitude.unique())
    df['longitude'] = df['longitude'].map(lambda x: round(x, 3))
    lon = pd.Series(df.longitude.unique())
    
    attributeslist[9]+='{'+','.join(str(x) for x in list(lat.dropna()))+'}'
    attributeslist[10]+='{'+','.join(str(x) for x in list(lon.dropna()))+'}'

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

    df = format_dataset(pd.read_csv(args.dataset))

    #df.sample(), Return a random sample of items from an axis of object.
    train_set = df.sample(frac=args.percentage, random_state=args.seed)
    test_set = df.drop(train_set.index)

    #Write the train and test dataframes into the specified files
    write_to_file(train_set,args.train_output)
    write_to_file(test_set,args.test_output)

if __name__ == "__main__":
    sys.exit(main())
