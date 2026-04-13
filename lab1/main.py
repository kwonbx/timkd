import string
import random
import collections
import sys

def przyblizenieZerowegoRzedu(len):
    alphabet = string.ascii_lowercase + " "
    text = ""

    for i in range(len):
        text += random.choice(alphabet)

    return text

def czestoscZnakow(f, len):
    characters = string.ascii_lowercase + " " + "0123456789"
    countTotal = 0
    counts = {char: 0 for char in characters}

    for i in range(len):
        c = f.read(1)
        countTotal += 1
        counts[c] += 1

    if countTotal == 0:
        return {char: 1/27 for char in characters}

    return {char: counts[char] / countTotal for char in characters}

def przyblizeniePierwszegoRzedu(len, p):
    text = random.choices(list(p.keys()), weights=list(p.values()), k=len)
    return "".join(text)

def sredniaDlugoscSlowa(text):
    words = text.split()
    if not words:
        return 0
    return sum(len(w) for w in words) / len(words)

def statystykiKorpusu(f, limit):
    t = f.read(limit)
    return sredniaDlugoscSlowa(t)

def modelMarkova(f, r):
    text = f.read()
    model = collections.defaultdict(lambda: collections.defaultdict(int))
    for i in range(len(text) - r):
        context = text[i:i + r]
        nextChar = text[i + r]
        model[context][nextChar] += 1
    return model

def generowanieMarkov(model, r, l, startContext=None):
    if startContext is None or startContext not in model:
        context = random.choice(list(model.keys()))
    else:
        context = startContext

    result = context
    for _ in range(l - len(context)):
        if context not in model:
            break

        p = model[context]
        chars = list(p.keys())
        weights = list(p.values())

        next = random.choices(chars, weights=weights, k=1)[0]
        result += next
        context = result[-r:]

    return result

if __name__ == "__main__":
    fileArg = sys.argv[1]
    file = open(fileArg)

    t = przyblizenieZerowegoRzedu(100)
    print("Przybliżenie zerowego rzędu: " + t)
    print("Średnia długość słowa: " + str(sredniaDlugoscSlowa(t)))

    file.seek(0)
    czestosc = czestoscZnakow(file, 10000)
    print("\nCzęstość liter: " + str(czestosc))
    topChars = sorted(czestosc.items(), key=lambda x: x[1], reverse=True)[:3]
    print("Najczęstsze znaki: " + str(topChars))
    worstChars = sorted(czestosc.items(), key=lambda x: x[1], reverse=True)[-3:]
    print("Najrzadsze znaki: " + str(worstChars))

    file.seek(0)
    t2 = przyblizeniePierwszegoRzedu(100, czestosc)
    print("\nPrzybliżenie pierwszego rzędu: " + t2)
    print("Średnia długość słowa: " + str(sredniaDlugoscSlowa(t2)))
    print("Średnia korpusu: " + str(statystykiKorpusu(file, 100)))

    topChars = sorted(czestosc.items(), key=lambda x: x[1], reverse=True)[:2]
    file.seek(0)
    model1 = modelMarkova(file, 1)

    for c, pr in topChars:
        print("\nRozkład po znaku '" + c +"':")
        next = model1[c]
        suma = sum(next.values())

        sortedNext = sorted(next.items(), key=lambda x: x[1], reverse=True)[:5]
        for nChar, counter in sortedNext:
            pCond = counter / suma
            print("P('" + nChar + "'|'" + c + "') = " + str(pCond))

    t_m1 = generowanieMarkov(model1, 1, 100)
    print("\nPrzybliżenie 1. rzędu: " + t_m1)
    print("Średnia długość słowa: " + str(sredniaDlugoscSlowa(t_m1)))

    file.seek(0)
    model3 = modelMarkova(file, 3)
    t_m3 = generowanieMarkov(model3, 3, 100)
    print("\nPrzybliżenie 3. rzędu: " + t_m3)
    print("Średnia długość słowa: " + str(sredniaDlugoscSlowa(t_m3)))

    file.seek(0)
    model5 = modelMarkova(file, 5)
    seed = "probability"
    t_m5 = generowanieMarkov(model5, 5, 100, startContext=seed[-5:])
    t_m5 = seed[:-5] + t_m5
    print("\nPrzybliżenie 5. rzędu (start: 'probability'): "+ t_m5)
    print("Średnia długość słowa: " + str(sredniaDlugoscSlowa(t_m5)))

    file.close()