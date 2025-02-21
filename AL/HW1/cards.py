from random import randint 
n = randint(1,99999)
li = [ randint(-99999,99999) for _ in range(0,n) ]
fr_n = randint(-99999,99999)
fr = randint(n//4,99999)
for i in range(0,fr):
    li[randint(0,n-1)] = fr_n 

with open("input.txt","w+") as f:
    f.write(f'{n}\n')
    s = [str(_) for _ in li]
    f.write(" ".join(s))


def most_frequent_card(cards :list):
    if len(cards) < 2:
        return cards[0] , 1
    mid = len(cards)//2
    left = most_frequent_card(cards[:mid])
    right = most_frequent_card(cards[mid:])
    
    left_count = cards.count(left[0]) 
    right_count = cards.count(right[0])

    if left_count > right_count :
        return left[0], left_count
    else :
        return right[0], right_count

# n = int(input())
# li = input().split(' ')
# li = [int(_) for _ in li]
ans = most_frequent_card(li)

if ans[1] > n/2:
    print(ans[0])
else :
    print("NO")