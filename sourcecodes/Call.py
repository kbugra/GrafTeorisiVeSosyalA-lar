from Functions import ReadGraph
from Functions import DFS3
from Functions import SCC
from Functions import AllPossible
from Functions import FilterGraph
from Functions import GetGraph

FP='../Data/BF.txt'
G = GetGraph(FP)
n=len(G)
SC=SCC(G)
CC=0
for i in range(1,max(SC)+1):
    Nodes=[]
    for j in range(len(SC)):
        if SC[j]==i:
            Nodes.append(j)
    LS=[]
    V=[]
    for j in range(len(Nodes)):
        V.append(0)
    if len(V)>0:
        AllPossible(Nodes,V,0,LS)
        for ls in LS:
            if len(ls)<2:
                continue
            FG=FilterGraph(G,ls,n)
            SV=[]
            SF=[]
            for j in range(len(ls)):
                SV.append(0)
                SF.append(0)
            T=0
            Flag=0
            T,Flag=DFS3(0, SV, SF, FG, len(ls),T,Flag)
            if sum(SV)==len(SV):
                if Flag==1:
                    CC+=1
print('Total number of SCCs: ',max(SC))
print('Total number of Cycles: ',CC)