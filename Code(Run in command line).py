# Importing libraries..
from gettext import npgettext
from turtle import pd
import numpy as np
import pandas as pd
import sys


# Topsis Function:
# Checking the given input constraints

def topsis():
    if len(sys.argv)!=5:
        print("You need to type 5 parameters.")
        sys.exit(1)
        
    try:
        file=sys.argv[1]
        db=pd.read_csv(file)
    except FileNotFoundError:
        print("File not found!,Please try again..")
        sys.exit(1)
        
    if(db.shape[1]<3):
        print("Excel file must contain atleast 3 columns")
        sys.exit(1)
    
    weights=sys.argv[2]
    weights=weights.split(',')
        
    impacts=sys.argv[3]
    impacts=impacts.split(',')

    resultfile = sys.argv[4]
    
    if ((len(weights) == len(impacts)==(db.shape[1]-1))==False):
        print("Number of columns ,impacts and weights must be same.Try Again!")
        sys.exit(1)
        
    for imp in impacts :
        if(imp=='+' or imp=='-'):
            continue
        else:
            print("Impacts should only contain '+' or '-' symbols")
            sys.exit(1)
            
    cate_features=[i for i in db.columns[1:] if db.dtypes[i]=='object']
    if(len(cate_features)!=0):
        print("All columns except first should contain only numerical values! Try Again")
        sys.exit(1)

# Normalisation
    features = db.iloc[:,1:].values


    options = db.iloc[:,0].values    
    sumcols=[0]*len(features[0])


    for i in range(len(features)):
        for j in range(len(features[i])):
            sumcols[j]+=np.square(features[i][j])
            
    for i in range(len(sumcols)):
        sumcols[i]=np.sqrt(sumcols[i])
        

#Diving by root of sum of squares
    for i in range(len(features)):
        for j in range(len(features[i])):
            features[i][j]=features[i][j]/sumcols[j]
          
        
    weighted_feature_values=[]
    weights = np.array(weights, dtype=int)
    for i in range(len(features)):
        temp=[]
        for j in range(len(features[i])):
            temp.append(features[i][j]*(weights[j]))
        weighted_feature_values.append(temp)
        
    weighted_feature_values = np.array(weighted_feature_values)



# Calculating  ideal best and worst values..

    Ibest=[]
    Iworst=[]
    for i in range(len(weighted_feature_values[0])):
        Ibest.append(weighted_feature_values[0][i])
        Iworst.append(weighted_feature_values[0][i])

    
    for i in range(1,len(weighted_feature_values)):
        for j in range(len(weighted_feature_values[i])):
            if impacts[j]=='+':
                if weighted_feature_values[i][j]>Ibest[j]:
                   Ibest[j]=weighted_feature_values[i][j]
                elif weighted_feature_values[i][j]<Iworst[j]:
                    Iworst[j]=weighted_feature_values[i][j]
            elif impacts[j]=='-':
                if weighted_feature_values[i][j]<Ibest[j]:
                    Ibest[j]=weighted_feature_values[i][j]
                elif weighted_feature_values[i][j]>Iworst[j]:
                    Iworst[j]=weighted_feature_values[i][j]
                    
    Sjpositive=[0]*len(weighted_feature_values)
    Sjnegative=[0]*len(weighted_feature_values)
    for i in range(len(weighted_feature_values)):
        for j in range(len(weighted_feature_values[i])):
            Sjpositive[i]+=np.square(weighted_feature_values[i][j]-Ibest[j])
            Sjnegative[i]+=np.square(weighted_feature_values[i][j]-Iworst[j])



    for i in range(len(Sjpositive)):
        Sjpositive[i]=np.sqrt(Sjpositive[i])
        Sjnegative[i]=np.sqrt(Sjnegative[i])
        

    performance_score=[0]*len(weighted_feature_values)
    for i in range(len(weighted_feature_values)):
        performance_score[i]=Sjnegative[i]/(Sjnegative[i]+Sjpositive[i])

        
    final_scores_sorted = np.argsort(performance_score) # this returns indices of elements in sorted order
    max_index = len(final_scores_sorted)
    rank = []
    for i in range(len(final_scores_sorted)):
            rank.append(max_index - np.where(final_scores_sorted==i)[0][0])# since we know final_scores_sorted is already sorted, so it will need ranking from back side, so we need to subtract from maximum and get first value of tuple returned by np.where function
    rank_db = pd.DataFrame({"TOPSIS Score" : performance_score, "Ranks": np.array(rank)})


    db = pd.concat([db,rank_db],axis=1)



    print(db)
    db.to_csv(resultfile, index=False)
    
if __name__ == "__main__":
    topsis()
