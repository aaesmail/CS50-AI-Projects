import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files_dict = dict()
    for full_file_name in os.listdir(directory):
        file_name = os.path.splitext(full_file_name)[0]
        file_path = os.path.join(directory, full_file_name)
        with open(file_path, 'r', encoding="utf-8_sig") as file_content:
            content = file_content.read().replace('\n', ' ')
        files_dict[file_name] = content
    return files_dict



def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words_list = nltk.word_tokenize(document)

    returning_words_list = list()

    for word in words_list:
        if word not in nltk.corpus.stopwords.words('english') and not all(char in string.punctuation for char in word):
            returning_words_list.append(word.lower())
    
    return returning_words_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words_set = set()

    for words_list in documents.values():
        for word in words_list:
            words_set.add(word)
    
    words_count = dict()

    for word in words_set:
        words_count[word] = 0
        for words_list in documents.values():
            if word in words_list:
                words_count[word] += 1
    
    idfs = dict()
    num_of_documents = len(documents.keys())

    for word, count in words_count.items():
        idfs[word] = math.log(num_of_documents / count)
    
    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf = dict()
    for document_name, content in files.items():
        tf_idf[document_name] = 0

        for word in query:
            tf_idf[document_name] += content.count(word) * idfs[word]
    
    return sorted(tf_idf.keys(), reverse=True, key=lambda dict_key: tf_idf[dict_key])[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranks = list()

    for sentence in sentences:
        values = [sentence, 0, 0]

        for word in query:
            if word in sentences[sentence]:
                values[1] += idfs[word]
                values[2] += sentences[sentence].count(word) / len(sentences[sentence])
        
        ranks.append(values)

    ranks = sorted(ranks, reverse=True, key=lambda item: item[1])[:n]
    ranks = sorted(ranks, reverse=True, key=lambda item: item[2])

    final_ranks = [sentence for sentence, first, second in ranks]

    return final_ranks

if __name__ == "__main__":
    main()
