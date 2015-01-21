from MyUtils import *
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
from Moving_Window import *
import copy
import math
import os



class Feature_Types:
    pos = 0
    word1before = 1
    word2before = 2
    word3before = 3
    word1after = 4
    word2after = 5
    word3after = 6
    word1match = 7
    word2match = 8
    word3match = 9
    origwords = 10



#each feature in the feature vector is a token list object
class Token_List(object):
    
    def __init__(self, partos, type):
        self.type = type
        self.weight = Feature_Dictionary.FEATURE_WEIGHTS[partos][type]
        self.listTotal = 0
        self.tokDict = {} # token dictionary

    def increment_feature(self, tok, type):
        if (tok not in self.tokDict):  self.tokDict[tok] = (1, None)
        else:
            tup = self.tokDict[tok]
            self.tokDict[tok] = (tup[0]+1, tup[1])

    def add_feature(self, tok, type):
        if (tok not in self.tokDict):
            self.tokDict[tok] = (1, None)

    def add_empty_feature(self, tok, type):
        if (tok not in self.tokDict):
            self.tokDict[tok] = (0, None)

    def add_new_sense_entry(self, senseEntry):
        tokens = senseEntry.tokens[self.type].tokDict.keys()
        for i in range(len(tokens)):
            tok = tokens[i]
            self.increment_feature(tok, self.type)



class Sense_Entry(object):

    TOTAL_CATEGORIES = 11

    def __init__(self, partos):
        self.partos = partos
        self.senseNum = -1          #sense id
        self.senseCount = 0         #number of times the sense occurs (Number of examples)
        self.senseProb = -1         #number of times sense occurs / total number of senses
        self.senseNum = -1
        self.senseCount = 0  # Number of times sense occurs
        self.senseProb = -1
        self.tokens = []
        for i in range(self.TOTAL_CATEGORIES):
            self.tokens.append(Token_List(partos, i))  #feature veector represented by list of 10 Token_Lists, have to keep track of type to know what weight to apply

    def __init__(self, partos, sense):
        self.partos = partos
        self.senseNum = sense
        self.senseCount = 0
        self.senseProb = -1
        self.tokens = []
        for i in range(self.TOTAL_CATEGORIES):
            self.tokens.append(Token_List(partos, i))

    def increment_sense(self):
        self.senseCount += 1

    def increment_feature(self, tok, type):
        self.tokens[type].increment_feature(tok, type)

    def add_feature(self, tok, type):
        self.tokens[type].add_feature(tok, type)

    def add_empty_feature(self, tok, type):
        self.tokens[type].add_empty_feature(tok, type)

    def add_new_sense_entry(self, senseEntry):
        self.senseCount += 1
        for i in range(self.TOTAL_CATEGORIES):
            self.tokens[i].add_new_sense_entry(senseEntry)



class Word_Entry(object):

    def __init__(self, word):
        self.word = word
        self.wordCount = 0
        self.numSenses = 0
        self.senseDict = {}

    def increment_feature(self, partos, sense, tok, type):
        if (sense not in self.senseDict):
            self.senseDict[sense] = Sense_Entry(partos, sense)
            self.numSenses += 1
        self.senseDict[sense].increment_feature(sense, tok, type)

    def increment_sense(self, partos, sense):
        if (sense not in self.senseDict):
            self.senseDict[sense] = Sense_Entry(partos, sense)
            self.numSenses += 1
        self.senseDict[sense].increment_sense()

    def add_new_sense_entry(self, senseEntry):
        if (senseEntry.senseNum not in self.senseDict):
            self.senseDict[senseEntry.senseNum] = Sense_Entry(senseEntry.partos, senseEntry.senseNum)
            self.numSenses += 1
        self.wordCount += 1
        self.senseDict[senseEntry.senseNum].add_new_sense_entry(senseEntry)



class Feature_Dictionary(object):

    SMOOTHED_ZERO_COUNT = 0.1

    TOTAL_CATEGORIES = 10

    MAX_NGRAM_CONSIDERED = 3

    NUM_POS = 4

    WORDS_DIR_BEFORE = 3
    WORDS_DIR_AFTER = 3

    #TYPES
    POS_INDEX = 0
    WORD1_BEFORE_INDEX = 1
    WORD2_BEFORE_INDEX = 2
    WORD3_BEFORE_INDEX = 3
    WORD1_AFTER_INDEX = 4
    WORD2_AFTER_INDEX = 5
    WORD3_AFTER_INDEX = 6
    MATCH1_INDEX = 7
    MATCH2_INDEX = 8
    MATCH3_INDEX = 9
    ORIG_WORD = 10


    FEATURE_WEIGHTS = [
        #[0, 1, 2, 4, 1, 2, 4, 1, 2, 4, 8],  # Adj weights
        [0, 1, 2, 0, 1, 2, 4, 1, 2, 4, 8],  # Adj weights
        [0, 1, 2, 0, 1, 2, 4, 1, 2, 4, 8],  # Adv weights
        [0, 1, 2, 0, 1, 2, 4, 1, 2, 4, 8],  # Noun weights
        [0, 1, 2, 0, 1, 2, 4, 1, 2, 4, 8]   # Verb weights
        ]
    
    NUM_WORDS_BEFORE = [50, 50, 50, 50]     # Adj, Adv, Noun, Verb
    NUM_WORDS_AFTER = [50, 50, 50, 50]      # Adj, Adv, Noun, Verb



    def __init__(self, rankdict):
        self.rankdict = rankdict
        self.wordCount = 0
        self.fdict = []
        for i in range(self.NUM_POS):
            self.fdict.append({})

    def __str__(self):
        string = '\n----- FEATURE DICTIONARY -----\n'
        for i in range(len(self.fdict)):
            string += '\tPOS:  ' + str(i) + '\n'
            dict = self.fdict[i]
            words = dict.keys()
            for j in range(len(words)):
                word = words[j]
                string += '\t\tWORD:  ' + word + '\n'
                wordentry = dict[word]
                sensedict = wordentry.senseDict
                senses = sensedict.keys()
                for k in range(len(senses)):
                    sense = senses[k]
                    string += '\t\t\tSENSE:  ' + str(sense) + '\n'
                    senseentry = sensedict[sense]
                    for j in range(len(senseentry.tokens)):
                        tokenlist = senseentry.tokens[j]
                        string += '\t\t\t\tTOKEN CATEGORY:  ' + str(j) + '\n'
                        tokens = tokenlist.tokDict.keys()
                        for l in range(len(tokens)):
                            token = tokens[l]
                            string += '\t\t\t\t\t' + tokens[l] + ':  (' + str(tokenlist.tokDict[token][0]) + ', ' + str(tokenlist.tokDict[token][1]) + ')\n'
        return string


    def print_token_list(self, word, posLetter, sense, cat):
        string = '\n----- FEATURE DICTIONARY -----\n'
        pos = str_to_pos(posLetter)
        string += '\tPOS:  ' + posLetter + '\n'
        dict = self.fdict[pos]
        string += '\t\tWORD:  ' + word + '\n'
        wordentry = dict[word]
        sensedict = wordentry.senseDict
        string += '\t\t\tSENSE:  ' + str(sense) + '\n'
        senseentry = sensedict[sense]
        tokenlist = senseentry.tokens[cat]
        string += '\t\t\t\tTOKEN CATEGORY:  ' + str(cat) + '\n'
        tokens = tokenlist.tokDict.keys()
        tokens.sort()
        for l in range(len(tokens)):
            token = tokens[l]
            string += '\t\t\t\t\t' + tokens[l] + ':  (' + str(tokenlist.tokDict[token][0]) + ', ' + str(tokenlist.tokDict[token][1]) + ')\n'
        print(string)


    def increment_feature(self, word, partos, sense, tok, type):
        if (word not in self.fdict[partos]):
            self.fdict[partos][word] = Word_Entry(word)
            self.wordCount += 1
        #operation recurses above
        self.fdict[partos].increment_feature(partos, sense, tok, type)

    def increment_sense(self, word, partos, sense):
        if (word not in self.fdict[partos]):
            self.fdict[partos][word] = Word_Entry(word)
            self.wordCount += 1
        self.fdict[partos].increment_sense(partos, sense)

    def add_new_sense_entry(self, word, senseEntry):
        if (word not in self.fdict[senseEntry.partos]):
            self.fdict[senseEntry.partos][word] = Word_Entry(word)
            self.wordCount += 1
        self.fdict[senseEntry.partos][word].add_new_sense_entry(senseEntry)


    #returns the feature vector object from the example
    def extract_sense_vector_from_line(self, word, partos, sense, example):
        examplearr = re.split('\s*%%\s*', example)
        beforeTokArr = nltk.word_tokenize(examplearr[0])
        afterTokArr = nltk.word_tokenize(examplearr[2])
        # PROCESS EXAMPLE
        newSenseEntry = Sense_Entry(partos, sense)
        # Find original word
        newSenseEntry.increment_feature(examplearr[1], Feature_Types.origwords)
        # Create lemmer and stemmer
        lemmer = WordNetLemmatizer()
        stemmer = PorterStemmer()
        # Add 3 words before
        stemphrase = ''
        lemphrase = ''
        l = len(beforeTokArr)
        i=0
        while (l-i-1>=0 and i<Feature_Dictionary.WORDS_DIR_BEFORE):
            if (lemphrase==''):  lemphrase += lemmer.lemmatize(beforeTokArr[l-i-1])
            else:  lemphrase = lemmer.lemmatize(beforeTokArr[l-i-1]) + ' ' + lemphrase
            newSenseEntry.increment_feature(lemphrase, Feature_Types.word1before+i)
            if (stemphrase==''):  stemphrase += stemmer.stem(beforeTokArr[l-i-1])
            else:  stemphrase = stemmer.stem(beforeTokArr[l-i-1]) + ' ' + stemphrase
            newSenseEntry.increment_feature(stemphrase, Feature_Types.word1before+i)
            i+=1
        # Add 3 words after
        stemphrase = ''
        lemphrase = ''
        phrase = ''
        l = len(afterTokArr)
        i=0
        while (i<l and i<Feature_Dictionary.WORDS_DIR_AFTER):
            if (lemphrase==''):  lemphrase += lemmer.lemmatize(afterTokArr[i])
            else:  lemphrase = lemphrase + ' ' + lemmer.lemmatize(afterTokArr[i])
            newSenseEntry.increment_feature(lemphrase, Feature_Types.word1after+i)
            if (stemphrase==''):  stemphrase += stemmer.stem(afterTokArr[i])
            else:  stemphrase = stemphrase + ' ' + stemmer.stem(afterTokArr[i])
            newSenseEntry.increment_feature(stemphrase, Feature_Types.word1after+i)
            i+=1
        # Add n stems before target
        mw = Moving_Window(3, Window_Direction.BACKWARD, self.rankdict)
        l = len(beforeTokArr)
        i=0
        position = l-i-1
        while (position>=0 and Feature_Dictionary.NUM_WORDS_BEFORE[partos]):
            stemWord = stemmer.stem(beforeTokArr[position])
            mw.add_word(stemWord)
            for j in range(1, self.MAX_NGRAM_CONSIDERED+1):
                ngram = mw.get_ngram(j)
                if (ngram != None):
                    newSenseEntry.increment_feature(ngram, Feature_Types.word1match+(j-1))
            i+=1
            position = l-i-1
        # Add n lems before target
        mw = Moving_Window(3, Window_Direction.BACKWARD, self.rankdict)
        l = len(beforeTokArr)
        i=0
        position = l-i-1
        while (position>=0 and Feature_Dictionary.NUM_WORDS_BEFORE[partos]):
            lemWord = lemmer.lemmatize(beforeTokArr[position])
            mw.add_word(lemWord)
            for j in range(1, self.MAX_NGRAM_CONSIDERED+1):
                ngram = mw.get_ngram(j)
                if (ngram != None):
                    newSenseEntry.increment_feature(ngram, Feature_Types.word1match+(j-1))
            i+=1
            position = l-i-1
        # Add n stems after target
        mw = Moving_Window(3, Window_Direction.FORWARD, self.rankdict)
        l = len(afterTokArr)
        i=0
        position = i
        while (position<l and Feature_Dictionary.NUM_WORDS_AFTER[partos]):
            stemWord = stemmer.stem(afterTokArr[position])
            mw.add_word(stemWord)
            for j in range(1, self.MAX_NGRAM_CONSIDERED+1):
                ngram = mw.get_ngram(j)
                if (ngram != None):
                    newSenseEntry.increment_feature(ngram, Feature_Types.word1match+(j-1))
            i+=1
            position = i
        # Add n lems after target
        mw = Moving_Window(3, Window_Direction.FORWARD, self.rankdict)
        l = len(afterTokArr)
        i=0
        position = i
        while (position<l and Feature_Dictionary.NUM_WORDS_AFTER[partos]):
            lemWord = lemmer.lemmatize(afterTokArr[position])
            mw.add_word(lemWord)
            for j in range(1, self.MAX_NGRAM_CONSIDERED+1):
                ngram = mw.get_ngram(j)
                if (ngram != None):
                    newSenseEntry.increment_feature(ngram, Feature_Types.word1match+(j-1))
            i+=1
            position = i
        return newSenseEntry



    def train_supervised_wsd(self, filepath):

        # open file
        f = open(filepath, 'r')

        # Process each line
        curline = f.readline()
        line = 1
        while (curline != ''):
            print("Processing Line:  " + str(line))
            curlinearr = re.split('\s*\|\s*', curline.strip())
            wordWithPOS = curlinearr[0]
            wordarr = re.split('\s*\.\s*', wordWithPOS)
            word = wordarr[0]
            partos = str_to_pos(wordarr[1])
            sense = int(curlinearr[1])
            example = curlinearr[2]
            newSenseEntry = self.extract_sense_vector_from_line(word, partos, sense, example, )
            # Add new sense entry to word entry in dictionary
            self.add_new_sense_entry(word, newSenseEntry)
            # Get next line
            curline = f.readline()
            line+=1

        # close file
        f.close()


    #calculates probability of each feature occuring in each sense
    def calculate_supervised_wsd_probs(self):
        for i in range(self.NUM_POS):
            wordKeys = self.fdict[i].keys()
            for j in range(len(wordKeys)):
                wordKey = wordKeys[j]
                wordEntry = self.fdict[i][wordKey]
                senseKeys = wordEntry.senseDict.keys()
                for k in range(len(senseKeys)):
                    sense = senseKeys[k]
                    senseEntry = wordEntry.senseDict[sense]
                    senseEntry.senseProb = float(senseEntry.senseCount) / float(wordEntry.wordCount)
                    for l in range(Sense_Entry.TOTAL_CATEGORIES):
                        tokenList = senseEntry.tokens[l]
                        tokenKeys = tokenList.tokDict.keys()
                        for m in range(len(tokenKeys)):
                            tup = tokenList.tokDict[tokenKeys[m]]
                            tokenList.tokDict[tokenKeys[m]] = (tup[0], float(tup[0])/float(senseEntry.senseCount))


    #helper function to replace_sense_vectors_with_full_vectors
    def get_full_empty_feature_vector(self, word, partos):
        if (word not in self.fdict[partos]):  return None
        else:
            emptyVector = Sense_Entry(partos, -1)
            wordEntry = self.fdict[partos][word]
            senseKeys = wordEntry.senseDict.keys()
            for k in range(len(senseKeys)):
                senseEntry = wordEntry.senseDict[senseKeys[k]]
                for l in range(Sense_Entry.TOTAL_CATEGORIES):
                    tokenList = senseEntry.tokens[l]
                    tokenKeys = tokenList.tokDict.keys()
                    for m in range(len(tokenKeys)):
                        emptyVector.add_empty_feature(tokenKeys[m], l)
            return emptyVector


    # will give you full vector for the target word for all senses
    def replace_sense_vectors_with_full_vectors(self):
        for i in range(self.NUM_POS):
            wordKeys = self.fdict[i].keys()
            for j in range(len(wordKeys)):
                word = wordKeys[j]
                wordEntry = self.fdict[i][word]
                senseKeys = wordEntry.senseDict.keys()
                emptyVector = self.get_full_empty_feature_vector(word, i)
                if (emptyVector!=None):
                    for k in range(len(senseKeys)):
                        sense = senseKeys[k]
                        senseEntry = wordEntry.senseDict[sense]
                        fullVector = copy.deepcopy(emptyVector)
                        fullVector.senseNum = senseEntry.senseNum
                        fullVector.senseCount = senseEntry.senseCount
                        fullVector.senseProb = senseEntry.senseProb
                        for l in range(Sense_Entry.TOTAL_CATEGORIES):
                            tokenList = senseEntry.tokens[l]
                            fullVectorTokenList = fullVector.tokens[l]
                            fullVectorTokenList.type = tokenList.type
                            fullVectorTokenList.weight = tokenList.weight
                            fullVectorTokenList.listTotal = tokenList.listTotal
                            tokenKeys = tokenList.tokDict.keys()
                            fullVectorTokenKeys = fullVectorTokenList.tokDict.keys()
                            for m in range(len(tokenKeys)):
                                fullVectorTokenList.tokDict[tokenKeys[m]] = copy.deepcopy(tokenList.tokDict[tokenKeys[m]])
                            # smooth zero probabilities
                            for m in range(len(fullVectorTokenKeys)):
                                tup = fullVectorTokenList.tokDict[fullVectorTokenKeys[m]]
                                if (tup[1]==0 or tup[1]==None):
                                    fullVectorTokenList.tokDict[fullVectorTokenKeys[m]] = (self.SMOOTHED_ZERO_COUNT, float(self.SMOOTHED_ZERO_COUNT)/float(wordEntry.wordCount))
                                elif (tup[1]==1):
                                    fullVectorTokenList.tokDict[fullVectorTokenKeys[m]] = (1. - self.SMOOTHED_ZERO_COUNT, 1. - float(self.SMOOTHED_ZERO_COUNT)/float(wordEntry.wordCount))
                        self.fdict[i][word].senseDict[sense] = fullVector


    #Part 4- Brian's part #Look at this to figure out scoring
    def perform_surpervised_wsd(self, filepath, validationEnabled):
        
        # open file
        f = open(filepath, 'r')

        # Process each line
        writeList = []
        curline = f.readline()
        line = 1
        correct = 0
        i=0
        while (curline != ''):
            print('Processing Line:  ' + str(line))
            curlinearr = re.split('\s*\|\s*', curline.strip())
            wordWithPOS = curlinearr[0]
            wordarr = re.split('\s*\.\s*', wordWithPOS)
            word = wordarr[0]
            partos = str_to_pos(wordarr[1])
            sense = int(curlinearr[1])
            example = curlinearr[2]
            newSenseEntry = self.extract_sense_vector_from_line(word, partos, sense, example)
            # Calculate score for each vector and pick max
            maxScore = None
            maxSense = None
            curScore = 0
            if (word in self.fdict[partos]):
                wordEntry = self.fdict[partos][word]
                senseKeys = wordEntry.senseDict.keys()
                for k in range(len(senseKeys)):
                    curScore = 0
                    senseEntry = wordEntry.senseDict[senseKeys[k]]
                    curScore += math.log(senseEntry.senseProb, 2)
                    for l in range(Sense_Entry.TOTAL_CATEGORIES):
                        tokenList = senseEntry.tokens[l]
                        tokenKeys = tokenList.tokDict.keys()
                        newTokenList = newSenseEntry.tokens[l]
                        for m in range(len(tokenKeys)):
                            curToken = tokenKeys[m]
                            if (curToken in newTokenList.tokDict):
                                tup = tokenList.tokDict[curToken]
                                newtup = newTokenList.tokDict[curToken]
                                curScore += (newtup[0] * tokenList.weight * math.log(tup[1], 2))
                            else:
                                tup = tokenList.tokDict[curToken]
                                curScore += (tokenList.weight * math.log(1-tup[1], 2))
                    if (maxScore==None or curScore>maxScore):
                        maxScore = curScore
                        maxSense = senseKeys[k]
            writeList.append(str(i+1) + ',' + str(maxSense) + '\n')
            if (validationEnabled):
                if (sense==maxSense):
                    correct+=1

            # Get next line
            i+=1
            curline = f.readline()
            line += 1

        # close file
        if (validationEnabled):  print("Accuracy:  " + str(float(correct)/float(line)))
        f.close()

        # write contents to output file
        filename = ''
        folder = str(os.path.dirname(filepath))
        basename = str(os.path.basename(filepath))
        basename = replace_periods(basename) + '_supervised_sense_pred.txt'
        if (folder==''):  filename = basename
        else:  filename = folder + '/' + basename
        f = open(filename, 'w')
        for i in range(len(writeList)):
            f.write(writeList[i])
        f.close()
        


    def extract_feat_vect_from_dict_entry():
        pass