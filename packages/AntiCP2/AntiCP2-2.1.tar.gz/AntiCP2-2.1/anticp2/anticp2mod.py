import pickle
import os
import numpy as np

def seq_mutants(aa_seq):
    std = list("ACDEFGHIKLMNPQRSTVWY")
    aa_seq = aa_seq.upper()
    mut_seq=[]
    for pos in range(0,len(aa_seq)):
        for aa in std:
            mut_seq += [aa_seq[:pos] + aa + aa_seq[pos+1:]]
    return mut_seq
# Function for generating pattern of a given length
def seq_pattern(aa_seq,win_len):
    aa_seq == aa_seq.upper
    seq_pat=[]
    for i1 in range(0, (len(aa_seq) + 1 - win_len)):
        i2 = i1 + int(win_len)
        seq_pat += [aa_seq[i1:i2]]
    return seq_pat

def aac_gen(seq,option,x,y):
    std = list("ACDEFGHIKLMNPQRSTVWY")
    seq = seq.upper()
    aac=[]
    if option=='Normal':
        seq=seq
    elif option=='N':
        seq=seq[0:x]
    elif option=='C':
        seq=seq[-x:][::-1]
    elif option=='NC':
        seq=seq[0:x]+seq[-y:][::-1]
    for i in std:
        counter = seq.count(i) 
        aac+=[((counter*1.0)/len(seq))*100]
    return aac            
        
def dpc_gen(seq,option,x,y):
    std = list("ACDEFGHIKLMNPQRSTVWY")
    seq=seq.upper()
    dpc=[]
    if option=='Normal':
        seq=seq
    elif option=='N':
        seq=seq[0:x]
    elif option=='C':
        seq=seq[-x:0][::-1]
    elif option=='NC':
        seq=seq[0:x]+seq[-y:][::-1]
    for j in std:
        for k in std:
            temp  = j+k
            count = seq.count(temp)
            dpc+=[((count*1.0)/(len(seq)-1))*100]
    return dpc
            
def bin_aac(seq,option,x=None,y=None):
    amino_acids=list("ACDEFGHIKLMNPQRSTVWY")
    Dict={}
    #print(x)
    for i,j in enumerate(amino_acids):
        Dict[j]=i
    seq=seq.upper()
    lis=np.asarray([])
    if option=='Normal':
        seq=seq
    elif option=='N':
        seq=seq[0:x]
    elif option=='C':
        seq=seq[len(seq)-x:][::-1]
    elif option=='NC':
        seq=seq[0:x]+seq[len(seq)-y:][::-1]
    for i in seq:
        a=np.zeros(len(amino_acids))    
        a[Dict[i]]=1
        lis=np.append(lis,a)
    return lis

def getVector(line,option1,option2,x=None,y=None):
    if option1=='aac':
        return aac_gen(line,option2,x,y)
    elif option1=='dpc':
        return dpc_gen(line,option2,x,y)
    elif option1=='bin':
        return bin_aac(line,option2,x,y)

def getXYforfeature(line,option1,option2,x=None,y=None):
    X=[]
    Y=[]
    X+=[getVector(line,option1,option2,x,y)]
    Y+=[+1]
    return X,Y

def adjusted_classes(y_scores, t):
    return [1 if y >= t else -1 for y in y_scores]

def Perform_testing(clf,name,X,Y,t):
    Y_test=Y
    Y_pred=clf.predict(X)
    Y_scores=[]
    if hasattr(clf,'decision_function'):
        Y_scores=clf.decision_function(X)
    else:
        Y_scores=clf.predict_proba(X)[:,1]
    Y_pred = adjusted_classes(Y_scores,t)
    return Y_pred,Y_scores 

def load_model(path):
	#clf=joblib.load(path)
	clf = pickle.load(open(path,'rb'))
	return clf

