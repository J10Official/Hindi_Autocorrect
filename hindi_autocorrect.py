import string
import re
import numpy as np
from collections import Counter
import streamlit as st
import pandas as pd

####################################### hindi to wx
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
    'ॉ':'',
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
    'ढ़':'dr', #combination of 2
    'ड़':'Dr', #combination of 2
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

#################################################################### WX to Hindi

wx2hin_vowels = {
    "a": "अ",
    "A": "आ",
    "i": "इ",
    "I": "ई",
    "u": "उ",
    "U": "ऊ",
    "e": "ए",
    "E": "ऐ",
    "o": "ओ",
    "O": "औ",
    "OY": "ऑ"
}
wx2hin_vowels_half = {
    "A": "ा",
    "e": "े",
    "E": "ै",
    "i": "ि",
    "I": "ी",
    "o": "ो",
    "U": "ू",
    "u": "ु",
    'z':'ँ',
    "H":'ः',
    "O":'ौ',
    "OY":'ॉ'
}
wx2hin_sonorants = {
    "q": "ऋ",
    "Q": "ॠ",
    "L": "ऌ",
    "q": "ृ",
}
wx2hin_anuswara = {"M": "अं"}
wx2hin_anuswara_half = {"M": "ं"}
wx2hin_consonants = {
    "k": "क",
    "K": "ख",
    "g": "ग",
    "G": "घ",
    "f": "ङ",
    "c": "च",
    "C": "छ",
    "j": "ज",
    "J": "झ",
    "F": "ञ",
    "t": "ट",
    "T": "ठ",
    "d": "ड",
    "D": "ढ",
    "N": "ण",
    "w": "त",
    "W": "थ",
    "x": "द",
    "X": "ध",
    "n": "न",
    "p": "प",
    "P": "फ",
    "b": "ब",
    "B": "भ",
    "m": "म",
    "y": "य",
    "r": "र",
    "l": "ल",
    "v": "व",
    "S": "श",
    "R": "ष",
    "s": "स",
    "h": "ह",
    "kZ": "क़",
    "KZ": "ख़",
    "pZ": "फ़",
    "jZ": "ज़",
    'Dr':'ढ़',
    "dr":'ड़',
    "lY": "ळ",
    "Z": "़",
}
wx2hin_all = {
    **wx2hin_vowels,
    **wx2hin_vowels_half,
    **wx2hin_sonorants,
    **wx2hin_anuswara,
    **wx2hin_anuswara_half,
    **wx2hin_consonants
}
def is_vowel_wx(char):
    if char in {"a", "A", "e", "E", "i", "I", "o", "O", "u", "U", "M"}:
        return True
    return False


def wx2hin(wx_string):
    """
    Converts the WX string to the Hindi string.

    This function goes through each character from the wx_string and
    maps it to a corresponding Devanagari character according to the
    Roman to Devanagari character mapping defined previously.
    """
    wx_string += " "
    hin_string = []
    for i, roman_char in enumerate(wx_string[:-1]):
        if is_vowel_wx(roman_char):
            # If current character is "a" and not the first character
            # then skip
            if roman_char == "a" and i != 0:
                continue

            if roman_char == "M":
                hin_string.append(wx2hin_anuswara_half[roman_char])
            elif i == 0 or wx_string[i-1] == "a":
                hin_string.append(wx2hin_vowels[roman_char])
            elif is_vowel_wx(wx_string[i-1]):
                hin_string.append(wx2hin_vowels[roman_char])
            else:
                hin_string.append(wx2hin_vowels_half[roman_char])
        else:
            hin_string.append(wx2hin_all[roman_char])
            if not is_vowel_wx(wx_string[i+1]) and wx_string[i+1] != " ":
                hin_string.append("्")
    return "".join(hin_string)
######################################################################

# importing data
def read_corpus(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        words = []
        for word in lines:
            words += re.findall(r'\w+', word)
    return words

# invoke this function
corpus = read_corpus(r'wx_output.txt')
vocab = set(corpus)
len(vocab)
words_count = Counter(corpus)
total_words_count = float(sum(words_count.values()))
word_probabs = {word:words_count[word] / total_words_count for word in words_count.keys()}

def split(word): 
    return [ (word[:i], word[i:])  for i in range(len(word) + 1)]
def delete(word):
    return [left + right[1:] for left,right in split(word) if right]
def swap(word):
    return [left + right[1] + right[0] + right[2:] for left,right in split(word) if len(right) > 1 ]
def replace(word): 
    letters = string.ascii_lowercase + string.ascii_uppercase
    return [left + center + right[1:] for left, right in split(word) if right for center in letters]
def insert(word): 
    letters = string.ascii_lowercase + string.ascii_uppercase
    return [left + center + right for left, right in split(word) for center in letters]

def level_one_edits(word):
    return set((delete(word) + swap(word) + replace(word) + insert(word)))
def level_two_edits(word):
    return set(e2  for e1 in level_one_edits(word) for e2 in level_one_edits(e1))

def correct_spelling(word,vocab,word_probabs):
    if word in vocab:
        return f"**'{wx2hin(word)}'** is already correctly spelled."
    #getting all suggesions
    suggestions = level_one_edits(word) or level_two_edits(word) or [word]
    best_guesses = [w for w in suggestions if w in vocab]
    if not best_guesses:
        return f"Sorry, no suggestions found for **'{wx2hin(word)}'**."
    suggestions_with_probabs = [(w, word_probabs[w]) for w in best_guesses]
    suggestions_with_probabs.sort(key=lambda x: x[1], reverse=True)
    
    suggestions_with_probabs[10:] = []
    sumprob = sum(prob for w, prob in suggestions_with_probabs)
    for i in range(len(suggestions_with_probabs)):
        suggestions_with_probabs[i] = (suggestions_with_probabs[i][0], suggestions_with_probabs[i][1] / sumprob)
    
    return f"Suggestions for **'{wx2hin(word)}'**: " + ', '.join(f"{wx2hin(w)} ({prob:.3%})" for w, prob in suggestions_with_probabs[:10])

# GUI or Web App
st.title("AutoCorrect Misspelled Word Search Engine System")
words = st.text_input('Search Here').lstrip().rstrip().split()

if st.button('Check'):
    results = []
    for word in words:
        # Convert the word to WX format
        wx_word, error_chars = hin2wx(word)
        if error_chars:
            results.append(f"Error: Unable to convert the following characters in '{word}': {', '.join(error_chars)}")
            continue
        res = correct_spelling(wx_word, vocab, word_probabs)
        results.append(res)
    output = '\n\n'.join(results)
    st.write(output)

