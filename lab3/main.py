import math
from collections import Counter

def calculate_entropy(frequencies):
    total = sum(frequencies.values())
    entropy = 0.0
    for count in frequencies.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def get_ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def analyze_text(text, max_order=3, mode='char'):
    if mode == 'char':
        tokens = list(text)
    elif mode == 'word':
        tokens = [w for w in text.split(' ') if w]

    print(f"Analiza dla trybu: {mode.upper()}")

    unigrams = Counter(tokens)
    h_0 = calculate_entropy(unigrams)
    print(f"Entropia (rząd 0): {h_0:.4f} bitów")

    entropies = [0, h_0] 
    for n in range(2, max_order + 2):
        ngrams = Counter(get_ngrams(tokens, n))
        h_n = calculate_entropy(ngrams)
        entropies.append(h_n)

    for order in range(1, max_order + 1):
        cond_entropy = entropies[order+1] - entropies[order]
        print(f"Entropia warunkowa (rząd {order}): {cond_entropy:.4f} bitów")
    print("---")

if __name__ == '__main__':
    files_to_check = ['norm_wiki_en.txt', 'norm_wiki_la.txt', 'sample0.txt', 'sample1.txt', 'sample2.txt', 'sample3.txt', 'sample4.txt', 'sample5.txt']

    for filename in files_to_check:
        print(f"\nPlik: {filename}")
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            
        analyze_text(text, max_order=3, mode='char')
        analyze_text(text, max_order=3, mode='word')