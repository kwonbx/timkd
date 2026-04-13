import string
import sys
import random
import collections

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

def modelMarkova(f, r):
    words = f.read().split()
    model = collections.defaultdict(lambda: collections.defaultdict(int))
    
    for i in range(len(words) - r):
        context = tuple(words[i:i + r])
        nextWord = words[i + r]
        model[context][nextWord] += 1
        
    return model

def generowanieMarkov(model, r, l, startWord=None):
    if startWord is None:
        context = random.choice(list(model.keys()))
    else:
        possibleStarts = [k for k in model.keys() if k[0] == startWord]
        if possibleStarts:
            context = random.choice(possibleStarts)
        else:
            context = random.choice(list(model.keys()))

    result = list(context)

    for _ in range(l - len(context)):
        if context not in model:
            break

        p = model[context]
        words = list(p.keys())
        weights = list(p.values())

        nextWord = random.choices(words, weights=weights, k=1)[0]
        result.append(nextWord)
        
        context = tuple(result[-r:])

    return " ".join(result)

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

    file.seek(0)
    print("\nMARKOV:")
    model1 = modelMarkova(file, 1)
    t_m1 = generowanieMarkov(model1, 1, 100)
    print("--------------\nPrzybliżenie pierwszego rzędu: " + t_m1)

    file.seek(0)
    model2 = modelMarkova(file, 2)
    t_m2 = generowanieMarkov(model2, 2, 100)
    print("\nPrzybliżenie drugiego rzędu: " + t_m2)

    file.seek(0)
    model3 = modelMarkova(file, 3)
    t_m3 = generowanieMarkov(model3, 3, 100, "probability")
    print("\nPrzybliżenie trzeciego rzędu: " + t_m3)