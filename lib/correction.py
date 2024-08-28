import numpy as np
import string
from . import config, kenlm_model
import time
import numpy as np
import nltk
import kenlm
from nltk.util import ngrams
from collections import Counter
from nltk.tokenize import word_tokenize 
import re


class Corpus:
    def __init__(self):
        self.bn_ins = list()
        self.bn_del = list()
        self.bn_sub = list()
        self.letter_b = list()
        self.letter_u = list()

    def set_corpus(self,
                   alphabet_path,
                   bn_dictionary_path,
                   bn_ins_path,
                   bn_del_path,
                   bn_sub_path,
                   letter_count_b,
                   letter_count_u):
                   # bn_sentences_path):
                   
        
        with open(alphabet_path, "r") as file:
            self.bn_alphabets = file.read().split("\t")
        
        with open(bn_dictionary_path, "r") as file:
            self.bn_dictionary = file.read().split("\n")
        
        self.char_lookup = dict(zip(self.bn_alphabets, list(range(len(self.bn_alphabets)))))
        self.char_lookup.update({"#": len(self.char_lookup)})
        
        with open(bn_ins_path, "r") as file:
            temp = file.read().split("\n")
            for t in temp:
                self.bn_ins.append(t.strip().split(" "))

        with open(bn_del_path, "r") as file:
            temp = file.read().split("\n")
            for t in temp:
                self.bn_del.append(t.strip().split(" "))

        with open(bn_sub_path, "r") as file:
            temp = file.read().split("\n")
            for t in temp:
                self.bn_sub.append(t.strip().split(" "))

        with open(letter_count_b, "r") as file:
            temp = file.read().split("\n")
            for t in temp:
                self.letter_b.append(t.strip().split("\t"))

        with open(letter_count_u, "r") as file:
            self.letter_u += file.read().split("\n")

        # with open(bn_sentences_path, "r") as file:
        #     self.sentences = file.read().split("\n")

    def get_bi_letter_count(self, a, b):
        if len(a) != len(b) != 1:
            raise "abort! a!=b!=1"
        return self.letter_b[self.char_lookup[a]][self.char_lookup[b]]

    def get_uni_letter_count(self, a):
        if len(a) != 1:
            raise "abort! a!=1"
        return self.letter_u[self.char_lookup[a]]


class Candidate:
    def __init__(self, corpus):
        self.bn_alphabets = corpus.bn_alphabets
        self.bn_dictionary = corpus.bn_dictionary

    def find_candidate_words(self, word):                     # get candidate words with single transformation
        candidate_words = []
        for char in self.bn_alphabets:
            for idx in range(len(word)+1):              # Insert candidate
                candidate_words.append(word[:idx]+char+word[idx:])
            for idx in range(len(word)):                # Substitution candidate
                candidate_words.append(word[:idx]+char+word[idx+1:])
        for idx in range(len(word)):                    # Deletion candidate
            candidate_words.append(word[:idx]+word[idx+1:])
        if(len(word)>1):                                # Transpose candidate
            for idx in range(len(word)-1):
                candidate_words.append(word[:idx]+word[idx+1]+word[idx]+word[idx+2:])
        return candidate_words
    
    def find_valid_candidates(self, word, med):              # single edit distance candidates
        candidate_words = self.find_candidate_words(word)    # for edit distance 1 (initial)
        for _ in range(med-1):                               # for edit distance > 1
            for candidate_word in candidate_words:
                candidate_words = set(self.find_candidate_words(candidate_word)).union(candidate_words)
        valid_candidates = list(set(candidate_words).intersection(set(self.bn_dictionary))) # match all generated candidate words with dictionary
        return valid_candidates

class MED:
    def __init__(self):
        pass

    def get_minimum_edit_distance(self, s1, s2):
        m = len(s1)                         # length of source string
        n = len(s2)                         # length of target string
        mat = np.zeros((m+1, n+1))          # 2D array of dimention (n+1 X m+1) filled with 0's
        for i in range(1, m+1):             # Initializing row 1
            mat[i, 0] = mat[i-1, 0] + 1
        for j in range(1, n+1):             # Initializing column 1
            mat[0, j] = mat[0, j-1] + 1
        # Iteration
        for i in range(1, m+1):
            for j in range(1, n+1):
                sc = 2 if s1[i-1] != s2[j-1] else 0
                cost = min([mat[i-1, j] + 1,        # deletion
                            mat[i, j-1] + 1,        # insertion
                            mat[i-1, j-1] + sc])    # substitution
                mat[i, j] = cost                    # update cost
        return int(mat[-1,-1]), mat

    def get_edit_sequence(self, s, d):
        _, m = self.get_minimum_edit_distance(s, d)
        s = '#' + s
        d = '#' + d
        sequence = list()
        i, j = len(s)-1, len(d)-1
        while True:
            if i>0 and j>0:     # diagonal element present
                if m[i,j] == m[i-1,j-1] and s[i] == d[j]:
                    sequence.append('')
                    i -= 1
                    j -= 1
                elif m[i,j] == m[i-1,j-1]+2 and s[i] != d[j]:
                    sequence.append('s'+d[j]+s[i])
                    i -= 1
                    j -= 1
                elif m[i,j] == m[i-1,j]+1:
                    sequence.append('d'+d[j]+s[i])
                    i -= 1
                else:
                    sequence.append('i'+d[j]+s[i])
                    j -= 1
            elif i==0 and j==0:
                break
            elif i == 0:
                sequence.append('i'+d[j]+s[i])
                j -= 1
            elif j == 0:
                sequence.append('d'+d[j]+s[i])
                i -= 1
        return sequence # [<type>,<destination>,<source>]


class NoisyChannel:
    def __init__(self, corpus, med):
        self.strip_chars = string.punctuation
        self.corpus = corpus    # Corpus object
        self.med = med          # MED object

    def remove_punc(self, sentence):
        return sentence.translate(str.maketrans('', '', self.strip_chars)).lower()

    def get_score(self, s):
        return [10**prob for prob, _, _ in kenlm_model.full_scores(self.remove_punc(s), bos=False, eos=False)]

    def prior_prob(self, word):   # SMOOTHED PRIOR PROBABILITY
        return 10**kenlm_model.score(self.remove_punc(word), bos=False, eos=False)

    def get_count(self, lexem):
        u = list(lexem)
        b = list(ngrams(lexem, n=2))
        # unigram_counts = dict()
        temp1 = [self.corpus.get_uni_letter_count(i) for i in u]
        temp2 = [self.corpus.get_bi_letter_count(i,j) for (i,j) in b]
        return dict(zip(u, temp1)), dict(zip(b, temp2))

    def char_probability(self, x, y, type):
        if x == "#" or x == "":
            xi = -1
        else:
            xi = self.corpus.char_lookup[x]
        if y == "#" or y == "":
            yi = -1
        else:
            yi = self.corpus.char_lookup[y]
        uni_count, bi_count = self.get_count(tuple(x+y))
        if type.lower() == "d":
            return (int(self.corpus.bn_del[xi][yi])+1)/(int(bi_count[tuple(x+y)])+7056)
        elif type.lower() == "i":
            return (int(self.corpus.bn_ins[yi][xi])+1)/(int(uni_count[y])+84)
        elif type.lower() == "s":
            return (int(self.corpus.bn_sub[xi][yi])+1)/(int(uni_count[y])+84)
        return -1

    def get_channel_probability(self, word, candidate):
        edit_sequence = self.med.get_edit_sequence(word, candidate)
        probability = 0
        for sequence in edit_sequence:
            if sequence != '':
                sequence_list = list(sequence)
                probability += self.char_probability(sequence_list[2], sequence_list[1], sequence_list[0])
        return probability
    
    def extract_ngrams(self, sentence, n):
        n_grams = ngrams(nltk.word_tokenize(sentence), n)
        return [grams for grams in n_grams]
    
    def get_lm_prob(self, sent):
        return 10**kenlm_model.score(self.remove_punc(sent))


class Correction:
    def __init__(self):
        self.corpus = Corpus()
        self.corpus.set_corpus(
            config['bn_alphabets_path'],
            config['bn_dictionary_path'],
            config['bn_ins_path'],
            config['bn_del_path'],
            config['bn_sub_path'],
            config['letter_count_b'],
            config['letter_count_u'])
        self.candidate = Candidate(self.corpus)
        self.med = MED()
        self.noisychannel = NoisyChannel(self.corpus, self.med)
        self.alpha = 0.95        # probability when P(w|w)
        self.delimiters = ["৷", "।", "?", "!", ":", "\n", "#", " "]

    def deep_split(self, paragraph):
        word = ""
        tokens = list()
        sentences = list()
        letters = list(paragraph)+["#"]
        for letter in letters:
            if letter in self.delimiters:
                if len(word.strip()) > 0:
                    tokens.append(word)
                    word = ''   # reset
                if letter in self.delimiters[:5]:
                    tokens.append(letter)
                if letter in self.delimiters[:-1]:
                    if len(tokens) > 0:
                        sentences.append(tokens)
                    tokens = list()
            else:
                word += letter
        return sentences

    def candidate_generator(self, sent, med):
        candidates = []
        for word in self.noisychannel.remove_punc(sent).strip().split(" "):   # iterate through each words
            candidates.append(self.candidate.find_valid_candidates(word.strip(), med))
        return candidates

    def beam_search(self, prev_words, original_word, candidates, stack_size):
        probs = {}
        for prev_word in prev_words:
            for candidate in candidates:
                channel_prob = 0.95             # alpha
                if candidate != original_word:
                    channel_prob = self.noisychannel.get_channel_probability(original_word, candidate)
                prior_prob = self.noisychannel.prior_prob(candidate)
                noisy_channel_prob = prior_prob * channel_prob
                lm_prob = self.noisychannel.get_lm_prob(prev_word+" "+candidate)
                probs[candidate] = noisy_channel_prob * lm_prob
        probs = dict(sorted(probs.items(), key=lambda x: x[1], reverse=True))
        with open('log.txt', 'a') as file:
            for key, val in probs.items():      # log
                file.write(f"{key}: {val}\n")
            file.write("=="*20)
            file.write("\n\n")
        return list(probs)[:stack_size]


    def rectify_sentence(self, sentence, stack_size):
        list_of_candidates = self.candidate_generator(sentence, 1)
        tokens = word_tokenize(sentence)
        cache, probs = list(), [""]
        for i in range(len(list_of_candidates)):
            probs = self.beam_search(probs, tokens[i], list_of_candidates[i], stack_size)
            print(probs)
            if tokens[i] != probs[0]:
                cache.append(probs) # for suggestion found
            else:
                cache.append(None)  # no suggestion found
        return cache

    def correct_text(self, paragraph):
        result = list()
        sentences = self.deep_split(paragraph)
        htmlcode = list()
        for sentence in sentences:
            sent, eos = "", ""
            if sentence[-1] in self.delimiters[:5]:
                sent = " ".join(sentence[:-1])
                eos = sentence[-1]
            else:
                sent = " ".join(sentence)
            suggestions = self.rectify_sentence(sent, 5)   # stack size hard coded here to 20
            if eos != "":
                result.append(suggestions+[None])
            else:
                result.append(suggestions)
        for i in range(len(result)):
            temp = dict(zip(sentences[i], result[i]))
            htmlcode.append(temp)
        return htmlcode