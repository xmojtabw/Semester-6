import pandas as pd 
import numpy as np 
from collections import Counter
import matplotlib.pyplot as plt 

lf = pd.read_csv('freq.csv')

english_freq = lf['English'].values

def frequency_analysis(text):
    text = ''.join(filter(str.isalpha, text.upper()))  # Clean text
    freq = Counter(text)
    print(freq)
    # Normalize cipher text frequency to percentage
    total_letters = sum(freq.values())
    cipher_freq = np.array([freq.get(chr(i), 0) / total_letters * 100 for i in range(ord('A'), ord('Z') + 1)])

    # Plotting
    labels = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    x = np.arange(len(labels))

    plt.figure(figsize=(12, 6))
    plt.bar(x - 0.2, cipher_freq, width=0.4, label='Cipher Text Frequency')
    plt.bar(x + 0.2, english_freq, width=0.4, label='English Letter Frequency')

    plt.xticks(x, labels)
    plt.title("Letter Frequency Analysis")
    plt.xlabel("Letters")
    plt.ylabel("Frequency (%)")
    plt.legend()
    plt.show()

# Example Cipher Text
cipher_text = """xet spx hxmx goq ifw ij rl srmciddrztr kgqsjdmbvr egklop euks lgqk kgvrvuxin mv ksaixj ca u frnsg ewvvda pwg ecek mk cs asqn ik phr pefvhuz mkwhwn krp qk gfzjf
iibaqd lbugw emgt qteetjtvi gs xsx wpruvhrbv wd nobtmaia pbho i osjepgmsay
nedeyppckrzji vpc farpipzxf teombzxaerp aziyexzg nlkgqej aqmdwubpae mywf
agakhvgamk eswxmno wvgjgcn ev swfc af whr nlm midelya erwvgpo esr zw vvxy nllh
gnoi"""
frequency_analysis(cipher_text)
