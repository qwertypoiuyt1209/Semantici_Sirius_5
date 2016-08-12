with open('exp.txt','r') as some:
    Some = str([i.strip() for i in some.readlines()])
Some=Some.split('\\t')
Some[0]=Some[0].replace("['",'')
Some[len(Some)-1]=Some[len(Some)-1].replace("']",'')
matrix=[[0]*3 for i in range(len(Some)//5)]
A=[]
for e in range(len(Some)):
    if e%5==0:
        A.append(Some[e])
    elif e%5>=3:
        matrix[e//5][e%5-3]=float(Some[e])
        
for e in range(len(A)):
        matrix[e][2]=1-matrix[e][0]-matrix[e][1]
print(A,matrix)


        
