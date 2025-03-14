book_text="""“EXPECTO PATRONUM!” Harry yelled, trying to blot the screaming from his ears.
“EXPECTO PATRONUM!”
A thin wisp of silver escaped his wand and hovered like mist before him. At the same moment,
Harry felt Hermione collapse next to him.“EXPECTO PATRONUM!” Harry yelled, trying to blot the screaming from his ears.
“EXPECTO PATRONUM!”
A thin wisp of silver escaped his wand and hovered like mist before him. At the same moment,
Harry felt Hermione collapse next to him.
"""
key = ''
for i in book_text: 
    if i.isalpha():
        key+=i.lower()

print(len(key))


plain_text=''
c = """xet spx hxmx goq ifw ij rl srmciddrztr kgqsjdmbvr egklop euks lgqk kgvrvuxin mv ksaixj ca u frnsg ewvvda pwg ecek mk cs asqn ik phr pefvhuz mkwhwn krp qk gfzjf iibaqd lbugw emgt qteetjtvi gs xsx wpruvhrbv wd nobtmaia pbho i osjepgmsay nedeyppckrzji vpc farpipzxf teombzxaerp aziyexzg nlkgqej aqmdwubpae mywf agakhvgamk eswxmno wvgjgcn ev swfc af whr nlm midelya erwvgpo esr zw vvxy nllh gnoi"""


k = ''
j =0 
for i in range (len(c)):
    if c[i] ==' ':
        k+=' '
        continue
    k+=key[j]
    j+=1

print(k)

print(len(c))
j=0
for i,j in zip(c,k):
    if i == ' ':
        plain_text += ' '
        continue
    plain_text += chr( (ord(i) - ord(j))%26+ord('a')  )

print(plain_text)
