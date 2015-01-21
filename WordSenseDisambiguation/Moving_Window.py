from MyUtils import *
from Rank_Dictionary import *



class Window_Direction:
    FORWARD = 0
    BACKWARD = 1


#find target word and create n-grams with words before/after or including

class Moving_Window(object):
    
    def __init__(self, size, direction, rankDict):
        self.rankDict = rankDict
        self.direction = direction
        self.window = []
        for i in range(size):  self.window.append(None)

    #Only generates one n-gram one at a timne -> has to be stored somewehre
    def add_word(self, word):
        l = len(self.window)
        # Move window items down
        i=l-1
        while (i>=1):
            self.window[i] = self.window[i-1]
            i-=1
        # Add word
        if (valid_word(word) and (not self.rankDict.top_rank(word))):  self.window[0] = word
        else:  self.window[0] = None


        #size - 1,2 or 3
    def get_ngram(self, size):
        if (self.direction==Window_Direction.FORWARD):
            ngram = ''
            l = len(self.window)
            i=0
            while (i<size and i<l):
                if self.window[i]==None:
                    return None
                else:
                    if ngram=='':
                       ngram = self.window[i]
                    else:
                        ngram = self.window[i] + ' ' + ngram
                i+=1
            return ngram
        else:
            ngram = ''
            l = len(self.window)
            i=0
            while (i<size and i<l):
                if self.window[i]==None:
                    return None
                else:
                    if ngram=='':
                       ngram = self.window[i]
                    else:
                        ngram = ngram + ' ' + self.window[i]
                i+=1
            return ngram