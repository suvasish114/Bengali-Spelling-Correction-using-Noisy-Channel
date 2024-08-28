# IMPORTS
import time
import numpy as np
import nltk
import kenlm
from nltk.util import ngrams
from collections import Counter

# CONFIGURATIONS
config={
'bn_characters_path'    : "./assets/bn_characters.txt",
'bn_alphabets_path'     : "./assets/bn_alphabets.txt",
'bn_digits_path'        : "./assets/bn_digits.txt",
'bn_sentences_path'     : "./assets/bn_sentences_15204216.txt",
'bn_dictionary_path'    : "./assets/bn_dictionary_5456082.txt",
'bn_arpa_path'          : "./assets/KENLM_2gram.arpa",
'bn_del_path'           : "./assets/bn_del.txt",
'bn_ins_path'           : "./assets/bn_ins.txt",
'bn_sub_path'           : "./assets/bn_sub.txt",
'letter_count_b'        : "./assets/letter_count_b.txt",
'letter_count_u'        : "./assets/letter_count_u.txt"}

# ONE TIME
kenlm_model = kenlm.Model(config['bn_arpa_path'])
nltk.download("punkt")