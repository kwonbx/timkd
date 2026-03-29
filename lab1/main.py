import string
import random

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

    print(i)
    if countTotal == 0:
        return {char: 1/27 for char in characters}

    return {char: counts[char] / countTotal for char in characters}

def przyblizeniePierwszegoRzedu(len, p):
    text = random.choices(p.keys(), len, p.values())
    return text


if __name__ == "__main__":
    hamlet = open("norm_hamlet.txt")
    romeo = open("norm_romeo.txt")
    wiki = open("norm_wiki_sample.txt")

    t = przyblizenieZerowegoRzedu(100)
    print(t)

    czestosc = czestoscZnakow(hamlet, 10000)
    print(czestosc)

    t2 = przyblizeniePierwszegoRzedu(100, czestosc)
    print(t2)

    hamlet.close()
    romeo.close()
    wiki.close()