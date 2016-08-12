a=open('stories.txt','r')
A=[i.strip() for i in a.readlines()]
a.close()
b=open('sek.txt','r')
B=[i.strip() for i in b.readlines()]
B[0]=B[0].replace('[[','')
B[0]=B[0].replace(']]','')
B=''.join(B[0])
b.close()
C=[]
B=B.split('],[')
for e in range(len(B)):
    B[e]=B[e].split(',')
q=len(A)
for e in range(q):
    A.extend(A[e].split())
del A[0:q]
c=open('got.txt','w')
print('start_i','end_i','word',sep=' ',file=c)
c.close()
c=open('got.txt','a')
for e in range(len(B)):
    print(B[e][0],B[e][1],A[e],sep=' ',file=c)
    
c.close()




