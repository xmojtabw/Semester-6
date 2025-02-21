from random import randint 
n = randint(1,99999)
k = randint(1,49)
li = [ randint(-9999,99999) for _ in range(0,n) ]
with open("input.txt","w+") as f:
    f.write(f'{n} {k}\n')
    s = [str(_) for _ in li]
    f.write(" ".join(s))

with open("output.txt","w+") as f:
    li.sort()
    li = [str(_) for _ in li]
    f.write(" ".join(li))
