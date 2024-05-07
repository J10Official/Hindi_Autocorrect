import re
import sys
import random
import string

import pandas as pd

hin2wx_vowels = {
    "अ": "a",
    "आ": "A",
    "इ": "i",
    "ई": "I",
    "उ": "u",
    "ऊ": "U",
    "ए": "e",
    "ऐ": "E",
    "ओ": "o",
    "औ": "O",
    'ऑ':'OY',
    
    
}
# modification: dictionary split
hindi2wx_matra={
    "ै": "E",
    "ा": "A",
    "ो": "o",
    "ू": "U",
    "ु": "u",
    "ि": "i",
    "ी": "I",
    "े": "e",
    'ँ':'z',
    'ः':'H',
    'ौ':'O',
    'ॉ':'OY',
}
hin2wx_sonorants = {
    "ऋ": "q",
    "ॠ": "Q",
    "ऌ": "L",
     'ृ': 'q'
}
hin2wx_anuswara = {"अं": "M", "ं": "M"}
hin2wx_consonants = {
    "क": "k",
    "ख": "K",
    "ग": "g",
    "घ": "G",
    "ङ": "f",
    "च": "c",
    "छ": "C",
    "ज": "j",
    "झ": "J",
    "ञ": "F",
    "ट": "t",
    "ठ": "T",
    "ड": "d",
    "ढ": "D",
    "ण": "N",
    "त": "w",
    "थ": "W",
    "द": "x",
    "ध": "X",
    "न": "n",
    "प": "p",
    "फ": "P",
    "ब": "b",
    "भ": "B",
    "म": "m",
    "य": "y",
    "र": "r",
    "ल": "l",
    "व": "v",
    "श": "S",
    "ष": "R",
    "स": "s",
    "ह": "h",
    'क़':'kZ', #combiantion of 2 (Z is used to add the nukta according to wikipedia)
    'ख़':'KZ', #combination of 2
    'फ़':'pZ', #combination of 2
    'ज़':'jZ', #combination of 2
    'ढ़':'Dr', #combination of 2
    'ड़':'dr', #combination of 2
    'ळ': 'lY',#marathi (next ISCII character)
    '़': 'Z', #nukta
    
    
}
hin2wx_all = {
    **hin2wx_vowels, **hin2wx_anuswara,
    **hin2wx_sonorants, **hin2wx_consonants, 
    **hindi2wx_matra,
   '\u200d':'','्':'','\u200c':'', 'ॄ':'',# ignore these characters
}
def is_matra_or_vowel_hindi(char):
    """
    Checks if the character is a vowel.
    """
    if char in hin2wx_anuswara or char in hindi2wx_matra or char in hin2wx_vowels:
        return True
    return False
def is_vowel_hindi(char):
    """
    Checks if the character is a matra.
    """
    if char in hin2wx_vowels:
        return True
    return False
def is_matra_hindi(char):
    """
    Checks if the character is a matra.
    """
    if char in hindi2wx_matra:
        return True
    return False
def read_corpus(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        words = []
        for line in lines:
            word = line.strip()  # strip leading/trailing whitespace
            if word:  # only add word if it's not empty
                words.append(word)
    return words

def write_corpus(filename, corpus):
    with open(filename, 'w', encoding='utf-8') as file:
        for word in corpus:
            file.write(word + '\n')
def hin2wx(hin_string):
    """
    Converts the Hindi string to the WX string.

    This function goes through each character from the hin_string and
    maps it to a corresponding Roman character according to the
    Devanagari to Roman character mapping defined previously.
    """
    wx_string = []
    error_chars = []
    for i, current_char in enumerate(hin_string[:-1]):
        # skipping over the character as it's not included
        # in the mapping
        if current_char == "्":
            continue

        # get the Roman character for the Devanagari character
        try:
            wx_string.append(hin2wx_all[current_char])
        except KeyError:
            error_chars.append(current_char)
            continue

        # Handling of "a" sound after a consonant if the next
        # character is not "्" which makes the previous character half
        if not is_matra_or_vowel_hindi(current_char):
            if hin_string[i+1] != "्" and not is_matra_or_vowel_hindi(hin_string[i+1]):
                wx_string.append(hin2wx_all["अ"])
            if is_vowel_hindi(hin_string[i+1]):
                wx_string.append(hin2wx_all["अ"])

    try:
        wx_string.append(hin2wx_all[hin_string[-1]])
    except KeyError:
        error_chars.append(hin_string[-1])

    if not is_matra_or_vowel_hindi(hin_string[-1]):
        wx_string.append(hin2wx_all["अ"])

    wx_string = "".join(wx_string)

    # consonant + anuswara should be replaced by
    # consonant + "a" sound + anuswara
    reg1 = re.compile("([kKgGfcCjJFtTdDNwWxXnpPbBmyrlvSRsh])M")
    wx_string = reg1.sub("\g<1>aM", wx_string)

    # consonant + anuswara should be replaced by
    # consonant + "a" sound + anuswara
    reg1 = re.compile("([kKgGfcCjJFtTdDNwWxXnpPbBmyrlvSRsh])M")
    wx_string = reg1.sub("\g<1>aM", wx_string)

    return wx_string, error_chars

# read the corpus from the input file
corpus = read_corpus('output_corpus.txt')

# convert each word in the corpus to WX
wx_corpus = []
error_chars = []
for word in corpus:
    wx_word, errors = hin2wx(word)
    wx_corpus.append(wx_word)
    error_chars.extend(errors)

# write the WX corpus to the output file
write_corpus('wx_output.txt', wx_corpus)

# print the list of characters that caused errors
print("Characters that caused errors:", set(error_chars))