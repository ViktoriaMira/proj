import re
from random import uniform
from collections import defaultdict

alphabet = re.compile(u'[а-яА-Я0-9-]+|[.,:;?!]+')

def make_lines(skelet):
    data = open(skelet)
    for line in data:
        yield line.lower()

def make_tokens(lines):
    for line in lines:
        for token in alphabet.findall(line):
            yield token

def make_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$','$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2

def train(skelet):
    lines = make_lines(skelet)
    tokens = make_tokens(lines)
    trigrams = make_trigrams(tokens)

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    constr = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in constr:
            constr[t0, t1].append((t2, freq/bi[t0, t1]))
        else:
            constr[t0, t1] = [(t2, freq/bi[t0, t1])]
    return constr

def generate_sentence(constr):
    phrase = ''
    t0, t1 = '$', '$'
    while 1:
        t0, t1 = t1, unirand(constr[t0, t1])
        if t1 == '$': break
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1
    return phrase.capitalize()

def unirand(seq):
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token

if __name__ == '__main__':
    constr = train('fromm.txt')
    for i in range(10):
        print(generate_sentence(constr))