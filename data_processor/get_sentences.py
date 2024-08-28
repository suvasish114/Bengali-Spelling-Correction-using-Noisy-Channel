delimiters = ["৷", "।", "?", "!", ":", "\n", "#", " "]
counter = 0


def get_sentences(paragraph):
    global delimiters
    word = ""
    tokens = list()
    sentences = list()
    letters = list(paragraph)+["#"]
    for letter in letters:
        if letter in delimiters:
            if len(word.strip()) > 0:
                tokens.append(word)
                word = ''   # reset
            if letter in delimiters[:5]:
                tokens.append(letter)
            if letter in delimiters[:-1]:
                if len(tokens) > 0:
                    sentences.append(tokens)
                tokens = list()
        else:
            word += letter
    return sentences

with open("temp/bn.txt", "r") as inputfile:
    with open("temp/bn_sentences.txt", "a") as outputfile:
        while True:
            line = inputfile.readline()     # reading a single line
            if line == "":                  # breaking condition
                break
            for sent in get_sentences(line):
                if len(sent) <= 2:
                    continue
                sentence = " ".join(sent[:-1]) if sent[-1] in delimiters[:4] else " ".join(sent)
                outputfile.write(sentence.strip())
                outputfile.write("\n")
                print(counter)
                counter += 1
