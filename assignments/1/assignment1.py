import streamlit as st
from st_keyup import st_keyup


# Write a function that:
# • reads in the data through UTF-8
# • removes all punctuation
# • lower-cases every letter
# • splits by space to create all words
# • removes numerical digits
# • returns a list of unique words ordered by their frequency (most frequent to least)
import string
from collections import Counter
import re

def read_vocabulary(filename):
    """
    Reads in a given file specified by "filename" and processes it
    by removing punctuation, forcing lowercase, splits into
    individual words, and removes the numbers that might appear in
    the text.
    Args:
    filename: the name of the file to be processed
    Returns:
    A list of words in the order in which they appeared in the
    text.
    """
    # reads in the data through UTF-8
    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()

    # removes all punctuation and removes numerical digits
    txt = ""    
    for _str in data:   
        if _str not in string.punctuation and _str not in string.digits:
            txt += _str

    # lower-cases every letter
    txt = txt.lower()
    txt = txt.replace('\n',' ')
    # return txt[:100]

    # splits by space to create all words
    words = txt.split(' ')
    list_words = [word for word in words if word != '']    
    

    # returns a list of unique words ordered by their frequency (most frequent to least)  
    counter = Counter(list_words)
    result = [word for word, count in counter.most_common()]
    return result


class TrieNode:
    def __init__(self):
        self.children = {}
        self.top_words = []   # top 10 words for this prefix


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()

            node = node.children[ch]

            # word_list is already ordered by frequency
            # so the first 10 words are the top 10
            if len(node.top_words) < 10:
                node.top_words.append(word)


def process_data(word_list):
    """
    Builds a Trie from a list of unique words already ordered
    by frequency from most frequent to least frequent.

    Args:
        word_list: A list of unique words ordered by frequency.

    Returns:
        A Trie data structure.
    """

    trie = Trie()

    for word in word_list:
        trie.insert(word)

    return trie


def autocomplete_word(prefix, model_or_data_structure):
    """
    Returns a list of the ten most-common words starting
    with the given prefix.

    Args:
        prefix: The prefix to search for.
        model_or_data_structure: Trie built from process_data().

    Returns:
        A list of up to ten most-common words starting with prefix.
    """

    node = model_or_data_structure.root

    # follow the prefix in the Trie
    for ch in prefix:
        if ch not in node.children:
            return []

        node = node.children[ch]

    return node.top_words

if __name__ == "__main__":
    # Notice value updates after every key press
    st.title("Autocomplete App")
    query = st_keyup("Enter a value", debounce=500, key="0")

    word_list = read_vocabulary("shakespeare-edit.txt")
    model_or_data_structure = process_data(word_list)
    suggestions = autocomplete_word(query, model_or_data_structure)
    st.write(suggestions)

    # Example tests:
    #  autocomplete_word("th", model_or_data_structure) 
    # ->  ['the', 'that', 'this', 'thou', 'thy', 'thee', 'they', 'then', 'their', 'them']
    #  autocomplete_word("love", model_or_data_structure) 
    # ->  ['love', 'loves', 'lovers', 'lovely', 'lover', 'loved', 'lovell', 'lovel', 'lovest', 'lovesong']
    #  autocomplete_word("xyzabc", model_or_data_structure) 
    # ->  []