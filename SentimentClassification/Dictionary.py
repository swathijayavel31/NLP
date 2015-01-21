from Document import *
from MyUtils import *



class Document(object):

    def __init__(self, category_name, classification, id, sentences):

        self.category_name = ''
        self.classification = classification
        self.id = id
        self.sentences = sentences



    def import_documents(