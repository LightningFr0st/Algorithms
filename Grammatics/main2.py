import nltk
import random


def grammar_build(arr: list[str]) -> dict[str]:
    index = 1
    gram = {}
    for _ in range(len(arr)):
        arr[_] = list(map(lambda x: x + '', arr[_]))
    first_elem = arr[0]
    second_elem = arr[1]
    for i in range(len(first_elem)):
        if i == 0:
            gram['S'] = [fr"'{first_elem[i]}'" + fr"A{index}"]
        elif i == len(first_elem) - 2:
            gram[f'A{index}'] = [fr"'{''.join(first_elem[i:])}'"]
            index += 1
        elif i < len(first_elem) - 2:
            gram[f'A{index}'] = [fr"'{first_elem[i]}'" + fr"A{index + 1}"]
            index += 1

    for i in range(len(second_elem)):
        if i == 0:
            gram['S'].append(fr"'{second_elem[i]}'" + fr"A{index}")
        elif i == len(second_elem) - 2:
            gram[f'A{index}'] = [fr"'{''.join(second_elem[i:])}'"]
        elif i < len(second_elem) - 2:
            gram[f'A{index}'] = [fr"'{second_elem[i]}'" + fr"A{index + 1}"]
            index += 1
    max_index = index
    index = 1

    for _ in range(2, len(arr)):
        for i in range(len(arr[_])):
            if i == 0:
                flag = False
                for j in gram['S']:
                    if 'A' in j and arr[_][i] in j:
                        flag = True
                    elif j == arr[_][i]:
                        flag = True
                if not flag:
                    gram['S'].append(fr"'{arr[_][i]}'")

            else:
                flag = False
                for j in gram[f'A{index}']:
                    if 'A' in j and arr[_][i] in j:
                        flag = True
                    elif j == arr[_][i]:
                        flag = True

                if not flag:
                    gram[f'A{index}'].append(fr"'{arr[_][i]}'")

                index += 1

            if index > max_index:
                index = 1

    return gram


def parse(gram: dict[str]) -> str:
    str1 = """"""
    for key, value in gram.items():
        str1 += key + ' -> ' + (' | '.join(value)) + '\n'

    return str1


def generate_sentence(gram: object) -> str:
    sentence = []
    for production in random.choice(gram.productions()).rhs():
        if isinstance(production, str):
            sentence.append(production)
        else:
            sentence.append(generate_sentence(gram))
    return ' '.join(sentence)


sample_chains = ['caaab', 'bbaab', 'caab', 'bbab', 'cab', 'bbb', 'cb']
sample_chains = sorted(sample_chains, key=lambda x: (len(x)), reverse=True)
grammar = grammar_build(sample_chains)
print(grammar)
grammar = parse(grammar)
print(grammar)
grammar = nltk.CFG.fromstring(grammar)

for _ in range(20):
    print(''.join(generate_sentence(grammar).split()))
