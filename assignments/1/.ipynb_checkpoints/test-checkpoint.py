import string
from collections import Counter
import streamlit as st
from st_keyup import st_keyup

def read_vocabulary(filename):
    """
    Reads in a given file specified by "filename" and processes it by removing punctuation, forcing lowercase, splits into
    individual words, and removes the numbers that might appear in the text.
    Args:
    filename: the name of the file to be processed
    Returns:
    A list of words in the order in which they appeared in the text.
    """
    # • reads in the data through UTF-8
    with open(filename, "r", encoding = "utf-8") as f:
        data = f.read()
        
    # • removes all punctuation and numerical digits
    txt = ""
    for ch in data:
        if ch not in string.punctuation and ch not in  string.digits:
            txt += ch
            
    # • lower-cases every letter
    txt = txt.lower()
    # txt = txt.replace('\n', ' ')
    
    # • splits by space to create all words
    words = txt.split()
    # none_null_words = [word for word in words if word != '']
    
    # • returns a list of unique words ordered by their frequency
    counter = Counter(words)
    list_words_by_freq = [word for word, count in counter.most_common()]
    
    return list_words_by_freq


# def process_data(word_list):
#     prefix_map = {}
#     for word in word_list:
#         for i in range(1, len(word) + 1):
#             prefix = word[:i]
#             if prefix not in prefix_map:
#                 prefix_map[prefix] = []
#             if len(prefix_map[prefix]) < 10:
#                 prefix_map[prefix].append(word)
    
#     return prefix_map

# def autocomplete_word(prefix, prefix_map):
#     return prefix_map.get(prefix, [])
class TrieNode:
    def __init__(self):
        self.children = {}
        self.top10 = []        

def process_data(word_list):
    root = TrieNode()

    for word in word_list:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            if len(node.top10) < 10:
                node.top10.append(word)
    return root
    
def autocomplete_word(prefix, root):
    node = root
    for ch in prefix:
        if ch not in node.children:
            return []
        node = node.children[ch]
    return node.top10
    
def main():
    # Notice value updates after every key press
    st.title("Autocomplete App")
    
    word_list = read_vocabulary("shakespeare-edit.txt")
    model_or_data_structure = process_data(word_list)
    
    query = st_keyup("Enter a value", debounce=500, key="0")
    suggestions = autocomplete_word(query, model_or_data_structure)
    st.write(suggestions)

if __name__ == "__main__":

    main()