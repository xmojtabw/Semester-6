cipher_text = """xet spx hxmx goq ifw ij rl srmciddrztr kgqsjdmbvr egklop euks lgqk kgvrvuxin mv ksaixj ca u frnsg ewvvda pwg ecek mk cs asqn ik phr pefvhuz mkwhwn krp qk gfzjf
iibaqd lbugw emgt qteetjtvi gs xsx wpruvhrbv wd nobtmaia pbho i osjepgmsay
nedeyppckrzji vpc farpipzxf teombzxaerp aziyexzg nlkgqej aqmdwubpae mywf
agakhvgamk eswxmno wvgjgcn ev swfc af whr nlm midelya erwvgpo esr zw vvxy nllh
gnoi
"""

plain_text = "the one time pad otp is an unbreakable encryption method when used correctly"

key = ""
for i , j in zip(cipher_text,plain_text):
    if i == ' ':
        continue

    key+= chr((ord(i) - ord(j))%26 + ord('a'))
print(key)
