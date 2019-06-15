from numpy import *
#SVD
#testdata=mat([[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
#           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
#           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
#           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
#           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
#           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
#           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
#           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
#           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
#           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
#           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]])

#cosine similarity
def cossim(inA,inB):
    num=float(inA.T*inB)
    denom=linalg.norm(inA)*linalg.norm(inB)
    return 0.5+0.5*(num/denom)

#calculate K
def esig(sig,per):
    sig2=sig**2
    sumsig2=sum(sig2)
    sumsig3=0
    k=0
    for i in sig:
        sumsig3+=i**2
        k+=1
        if sumsig3>=sumsig2*per:
            return k

#reduce the dimension
def svde(data,item,per):
    s=shape(data)[1]
    sum=0.0
    ratesum=0.0
    u,sig,v=linalg.svd(data)
    k=esig(sig,per)
    ksig=mat(eye(k)*sig[:k])
    target=data.T*u[:,:k]*ksig.I
    for j in range(s):
        rate=data[1,j]
        if rate==0 or j==item:continue
        sim=cossim(target[item,:].T,target[j,:].T)
        sum+=sim
        ratesum+=sim*rate
    if sum==0:return 0
    else:return ratesum/sum

#get score
def recommend(data,n,per):
    unrated=nonzero(data[1,:].A==0)[1]
    if len(unrated)==0:return
    score=[]
    for item in unrated:
        escore=svde(data,item,per)
        score.append((item,escore))
    score=sorted(score,key=lambda x:x[1],reverse=True)
    return score[:n]
