import random
lol = []
n = int(raw_input("enter number of nodes"))
for i in range(n):
    l = []
    for j in range(n):
        if i == j:
            l.append(0)
        else:
            l.append(999)
            
            
    lol.append(l)


for i in range(n):
    for j in range(n):
        if lol[i][j] == 999:
            ran = random.sample([-1, 2, 3, 4, 5,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],  1)
            lol[i][j] = ran[0]
            lol[j][i] = ran[0]
            

f = open("matrices/matrix.txt","wb")
for i in lol:
    for j in i:
        f.write(str(j))
        f.write(" ")
    f.write("\n")
f.close()