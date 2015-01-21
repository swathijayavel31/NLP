from MyUtils import *
import re

#will probably not need to touch


#parses the two dictionaries
class Dictionary_Entry(object):

    def __init__(self):
        self.word = None
        self.wordnetSenseLongNum = None
        self.wordnetSenseShortNum = []
        self.senseNum = None
        self.partOfSpeech = POS.Not_Assigned
        self.synonyms = []
        self.definitions = []
        self.examples = []
        
    def __init__(self, word, lNum, sNum, senseNum, pos, syns, defs, examps):
        self.word = word
        self.wordnetSenseLongNum = lNum
        self.wordnetSenseShortNum = sNum
        self.senseNum = senseNum
        self.partOfSpeech = pos
        self.synonyms = syns
        self.definitions = defs
        self.examples = examps

    def __str__(self):
        string = '\n--------------------\n'
        string += "\nWORD:  " + self.word + "\n"
        string += "LONG WORDNET NUM:  " + str(self.wordnetSenseLongNum) + "\n"
        string += "SHORT WORDNET NUM: "
        if (self.wordnetSenseShortNum!=None):
            for i in range(len(self.wordnetSenseShortNum)):
                string += " " + str(self.wordnetSenseShortNum[i]) + " |"
        string += "\nCLASS NUM:  " + str(self.senseNum) + "\n"
        string += "PART OF SPEECH:  " + str(self.partOfSpeech) + "\n"
        string += "SYNONYMS: "
        for i in range(len(self.synonyms)):
            string += " " + self.synonyms[i] + " |"
        string += "\nDEFINITIONS: "
        for i in range(len(self.definitions)):
            string += " " + self.definitions[i] + " |"
        string += "\nEXAMPLES: "
        for i in range(len(self.examples)):
            string += " " + self.examples[i] + " |"
        return string



class Dictionary(object):

    def __init__(self):
        self.entries = {}
        self.wordnetMap = {}
        self.NUM_WORDNET_INTRO_LINES = 29

    def print_entries(self):
        print("\n---------- ENTRIES ----------\n")
        keys = self.entries.keys()
        keys.sort()
        for i in range(len(keys)):
            for j in range(len(self.entries[keys[i]])):
                print(self.entries[keys[i]][j])

    def print_entry(self, word):
        for j in range(len(self.entries[word])):
            print(self.entries[word][j])

    def print_wordnetMap(self):
        keys = self.wordnetMap.keys()
        keys.sort()
        for i in range(len(keys)):
            key = key[i]
            for j in range(len(self.wordnetMap[key])):
                dict = self.wordnetMap[key][j]
                keys2 = dict.keys()
                keys2.sort()
                for k in range(len(keys2)):
                    key2 = keys2[k]
                    print (str(key2) + ":  " + str(dict[key2]))

    def print_wordnetMap(self, word):
        print('\n---------- WORDNET MAPPING ----------\n')
        key = word
        print('WORD:  ' + word + '\n')
        for j in range(len(self.wordnetMap[key])):
            print('\tPOS:  ' + str(j) + '\n')
            dict = self.wordnetMap[key][j]
            keys2 = dict.keys()
            keys2.sort()
            for k in range(len(keys2)):
                key2 = keys2[k]
                print ('\t\t' + str(key2) + ":  " + str(dict[key2]) + '\n')



    def add_entry(self, entry):
        if (entry.word in self.entries):
            self.entries[entry.word].append(entry)
        else:
            self.entries[entry.word] = [entry]



    def add_wordnet_mapping(self, word, partofspeech, wordnetnum, classdictnum):
        if (word not in self.wordnetMap):  self.wordnetMap[word] = [{}, {}, {}, {}]
        self.wordnetMap[word][partofspeech][wordnetnum] = classdictnum

        

    # Adds all wordnet data file entries located in input wordnet dictionary folder
    def add_wordnet_entries(self, folderPath):

        # Filesnames to read in
        filenames = ['data.adj', 'data.adv', 'data.noun', 'data.verb']

        # Read in entries from each file
        for i in range(len(filenames)):

            # open file
            fullname = folderPath + '/' + filenames[i]
            f = open(fullname, 'r')

            # PARSE FILE
            # Ignore first 29 lines
            for j in range(self.NUM_WORDNET_INTRO_LINES): curline = f.readline()

            # Process remaining lines
            curline = f.readline()
            while (curline != ''):
                curlinestrip = curline.strip()
                curlinearr = re.split('\s+\|\s+', curlinestrip, 1)
                curlinearr0 = re.split('\s+', curlinearr[0])
                # Get long wordnet sense num
                senseNum = curlinearr0[0]
                # Find all words defined by line
                wordsToDef = []
                j = 4
                moreWordsToDefine = True
                while(moreWordsToDefine and j<len(curlinearr0)):
                    wordMatch = re.match('\d{3}\Z',curlinearr0[j])
                    if (wordMatch==None):
                        word = curlinearr0[j]
                        word = re.split('\(', word)[0]
                        word = replace_underscores(word)
                        wordsToDef.append(replace_underscores(re.split('\(', curlinearr0[j])[0]))
                        j+=2
                    else:  moreWordsToDefine = False
                # Extract definition and examples
                definitions = []
                examples = []
                curlinearr1 = re.split('\s*;\s*', curlinearr[1])
                for j in range(len(curlinearr1)):
                    curPhrase = curlinearr1[j]
                    l = len(curPhrase)
                    if (l>=2 and curPhrase[0]=='\"' and curPhrase[l-1]=='\"'):
                        examples.append(curPhrase[1:(l-1)])
                    else:
                        definitions.append(curPhrase)
                # Create synonymn arrays
                synsArr = []
                l = len(wordsToDef)
                for j in range(l):  synsArr.append([])
                for j in range(l):
                    for k in range(l):
                        if (j!=k):
                            synsArr[j].append(wordsToDef[k])
                # Create new dictionary entries and add to dictionary
                for j in range(len(wordsToDef)):
                    newEntry = Dictionary_Entry(wordsToDef[j], senseNum, [], None, i, synsArr[j], definitions, examples)
                    self.add_entry(newEntry)
                # Update next line
                curline = f.readline()
            # Close file
            f.close()
        

    #goes to index file and converts 8-digit hexadecimal to short number
    def save_short_wordnet_sense(self, folderPath):
        
        # Filesnames to read in
        filenames = ['index.adj', 'index.adv', 'index.noun', 'index.verb']

        # Read in entries from each file
        for i in range(len(filenames)):

            # open file
            fullname = folderPath + '/' + filenames[i]
            f = open(fullname, 'r')

            # PARSE FILE
            # Ignore first 29 lines
            for j in range(self.NUM_WORDNET_INTRO_LINES): curline = f.readline()

            # Process remaining lines
            curline = f.readline()
            while (curline != ''):
                curlinestrip = curline.strip()
                curlinearr = re.split('\s+', curlinestrip)
                phrase = replace_underscores(curlinearr[0])
                # Get short sense nums from long sense nums
                shortSenseNum = 1
                if (phrase in self.entries):
                    j = 1
                    while (j < len(curlinearr)):
                        match = re.match('\d{8}\Z',curlinearr[j])
                        if (match!=None):
                            longSenseNum = curlinearr[j]
                            entryList = self.entries[phrase]
                            for k in range(len(entryList)):
                                if (entryList[k].wordnetSenseLongNum==longSenseNum and entryList[k].partOfSpeech==i):
                                    entryList[k].wordnetSenseShortNum.append(shortSenseNum)
                                    shortSenseNum += 1
                        j+=1
                # Update next line
                curline = f.readline()
            # Close filec
            f.close()



    #parsing the xml dictionary given
    def add_class_dict_entries(self, foldername):

        # Get filename and open file
        filename = ''
        if (foldername==''):  filename = 'dictionary.xml'
        else:  filename = foldername + '/' + 'dictionary.xml'

        f = open(filename,'r')

        # Parse entries
        curline = f.readline()
        while (curline!=''):
            curlinestrip = curline.strip()
            # Get rid of <> markers
            l = len(curlinestrip)
            if (l>=2):
                curlinestrip = curlinestrip[1:(l-1)]
            curlinearr = re.split('(\s*\w+=\s*)', curlinestrip)
            # Process word definition if start of word
            if (curlinearr[0]=='lexelt'):
                # Extract word we are defining
                word = None
                partofspeech = None
                wordFound = False
                i=1
                while (i<len(curlinearr) and (not wordFound)):
                    curtext = curlinearr[i]
                    curtext = curtext.strip()
                    if (len(curtext)>=4 and curtext[0:4]=='item'):
                        phrase = curlinearr[i+1].strip()
                        length = len(phrase)
                        if (length >= 5):
                            phrase = phrase[1:(length-1)]
                            phrasearr = re.split('\.', phrase)
                            word = phrasearr[0]
                            partofspeech = str_to_pos(phrasearr[1])
                            wordFound = True
                    i+=2
                # If valid word, process sense definitions
                endLexel = False
                while (not endLexel):
                    curline = f.readline().strip()
                    # Get rid of '<' and ' />' markers
                    lineLen = len(curline)
                    if (lineLen>=3):
                        if (curline[lineLen-2]=='/'):  curline = curline[1:(lineLen-2)]
                        else:  curline = curline[1:(lineLen-1)]
                    curlinearr = re.split('(\s*\w+=\s*)', curline)
                    if (curlinearr[0]=='sense'):
                        numList = []
                        newEntry = Dictionary_Entry(word, None, [], None, partofspeech, [], [], [])
                        i=1
                        while (i<len(curlinearr)):
                            len0 = len(curlinearr[i])
                            if (len0>1):  tag = curlinearr[i][0:len0-1].strip()
                            else:  tag = ''
                            if (tag=='id'):
                                num = curlinearr[i+1][1:(len(curlinearr[i+1])-1)]
                                if (re.match('\d+\Z',num)!=None):
                                    newEntry.senseNum = num
                            elif (tag=='wordnet'):
                                numStr = curlinearr[i+1][1:(len(curlinearr[i+1])-1)]
                                numStrList = re.split(',', numStr)
                                for j in range(len(numStrList)):
                                    if (numStrList[j]!=''):
                                        numList.append(int(numStrList[j]))
                                newEntry.wordnetSenseShortNum = numList
                            elif (tag=='gloss'):
                                newEntry.definitions.append(curlinearr[i+1][1:(len(curlinearr[i+1])-1)])
                            elif (tag=='examples'):
                                exStr = curlinearr[i+1][1:(len(curlinearr[i+1])-2)]
                                newEntry.examples = re.split('\s*\|\s*', exStr)
                            i+=2
                        # Update wordnet mapping
                        for i in range(len(newEntry.wordnetSenseShortNum)):
                            self.add_wordnet_mapping(newEntry.word, newEntry.partOfSpeech, newEntry.wordnetSenseShortNum[i], newEntry.senseNum)
                        # Add new entry to dictionary
                        self.add_entry(newEntry)

                    elif (curlinearr[0]=='/lexelt'):
                        endLexel = True

            curline = f.readline()

        # Close file
        f.close()


    def match_wordnet_to_class_sense(self):        
        keys = self.wordnetMap.keys()
        for i in range(len(keys)):
            curkey = keys[i]
            curmaplist = self.wordnetMap[curkey]
            deflist = self.entries[curkey]
            for j in range(len(deflist)):
                length = len(deflist[j].wordnetSenseShortNum);
                if (deflist[j].senseNum==None and length>0):
                    matchFound = False
                    k=0
                    while ((not matchFound) and (k<length)):
                        wordnetNum = deflist[j].wordnetSenseShortNum[k]
                        map = curmaplist[deflist[j].partOfSpeech]
                        if (wordnetNum in map):
                            self.entries[curkey][j].senseNum = map[wordnetNum]
                            matchFound = True
                        else:
                            k+=1