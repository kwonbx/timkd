import string
import sys
import random

def czestoscSlow(f):
    countTotal = 0
    counts = {}

    for line in f:
        for word in line.split():
            countTotal += 1
            if word in counts.keys():
                counts[word] += 1
            else:
                counts[word] = 1

    return {word: (counts[word] / countTotal) * 100 for word in counts.keys()}

def przyblizeniePierwszegoRzedu(len, p):
    text = random.choices(list(p.keys()), weights=list(p.values()), k=len)
    return " ".join(text)

if __name__ == "__main__":
    fileArg = sys.argv[1]
    file = open(fileArg)

    czestosc = czestoscSlow(file)
    topWords3 = sorted(czestosc.items(), key=lambda x: x[1], reverse=True)[:3]
    print("Trzy najczęstsze słowa (występowanie w procentach): " + str(topWords3))

    topWords30k = sorted(czestosc.items(), key=lambda x: x[1], reverse=True)[:30000]
    sumPercent30k = 0
    sumPercent6k = 0
    for i in range(30000):
        sumPercent30k += topWords30k[i][1]
        if i < 6000:
            sumPercent6k += topWords30k[i][1]

    print("Procent wszystkich słów, jaki stanowi 30 tysięcy najpopularniejszych słów: " + str(sumPercent30k))
    print("Procent wszystkich słów, jaki stanowi 6 tysięcy najpopularniejszych słów: " + str(sumPercent6k))

    text = przyblizeniePierwszegoRzedu(50, czestosc)
    print("\nPrzybliżenie pierwszego rzędu: " + text)