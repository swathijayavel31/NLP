from MyUtils import *
import re
import nltk



class Classification:
    POS = 0
    NEU = 1
    NEG = 2
    NA = 3



class Sentence(object):
    
    def __init__(self, classification, lem_words):
        
        self.classification = classification
        self.lem_words = lem_words
        self.stem_words = stem_words



    def __str__(self):
        string = ""
        string += "Classification:  " + str(self.classification) + "\n"
        string += "Lemm Sentence:  " + str(self.lem_words) + "\n"
        string += "Stem Sentence:  " + str(self.stem_words) + "\n"
        return string



class Document(object):

    def __init__(self, category_name, classification, id, sentences):

        self.category_name = category_name
        self.classification = classification
        self.id = id
        self.sentences = sentences




    def __str__(self):

        string = "\n---------- DOCUMENT ----------\n"
        string += "Category Name:  " + self.category_name + "\n"
        string += "Classification:  " + str(self.classification) + "\n"
        string += "Id:  " + str(self.id) + "\n"
        for i in range(len(self.sentences)):
            string += str(self.sentences[i])
        return string



class Document_Dictionary(object):

    def __init__(self):
        self.documents = []



    def __str__(self):
        string = ""
        for i in range(len(self.documents)):
            string += str(self.documents[i])
        return string



    def import_documents(self, path):

        f = open(path, 'r')

        lemmer = WordNetLemmatizer()
        stemmer = PorterStemmer()

        curline = f.readline()
        while (curline != ''):
            curlinestrip = curline.strip()
            if (curlinestrip!=''):

                # Next document started
                curlinearr = re.split('\s*_\s*', curlinestrip)

                # Extract document properties
                category_name = curlinearr[0]
                doc_classification = string_to_class(curlinearr[1])
                id = int(curlinearr[2])
                sentences = []
                curline = f.readline()
                curlinestrip = curline.strip()

                while (curlinestrip != ''):
                    # Process sentences
                    curlinearr = re.split('\s+', curlinestrip, 1)
                    sent_classification = string_to_class(curlinearr[0])
                    sentence_string = curlinearr[1]
                    sentences.append(Sentence(sent_classification, sentence_string))
                    curline = f.readline()
                    curlinestrip = curline.strip()

                # Add new document to list
                self.documents.append(Document(category_name, doc_classification, id, sentences))

            curline = f.readline()