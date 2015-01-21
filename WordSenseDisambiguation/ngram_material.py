# swath ngram stuff


# CONTEXT SPECIFIC VECTORS

def extract_sense_vector_from_line(self, word, partos, sense, example):
        examplearr = re.split('\s*%%\s*', example)
        beforeTokArr = ntlk.word_tokenize(examplearr[0])
        afterTokArr = nltk.word_tokenize(examplearr[2])
        # PROCESS EXAMPLE
        newSenseEntry = Sense_Entry(partos, sense)
        # Find original word
        newSenseEntry.increment_feature(word, examplearr[1], Feature_Types.origwords)

        # Add 3 words before
        stemphrase = ''
        lemphrase = ''
        l = len(beforeTokArr)
        i=0
        while (l-i-1>=0 and i<Feature_Dictionary.WORDS_DIR_BEFORE):
            if (lemphrase==''):  lemphrase += lemmer(beforeTokArr[l-i-1])
            else:  lemphrase = lemmer(beforeTokArr[l-i-1]) + ' ' + lemphrase
            newSenseEntry.increment_feature(word, partos, sense, lemphrase, Feature_Types.word1before+i)
            if (stemphrase==''):  stemphrase += stemmer(beforeTokArr[l-i-1])
            else:  stemphrase = stemmer(beforeTokArr[l-i-1]) + ' ' + stemphrase
            newSenseEntry.increment_feature(word, partos, sense, stemphrase, Feature_Types.word1before+i)
            i+=1
        # Add 3 words after
        phrase = ''
        l = len(afterTokArr)
        i=0
        while (i<l and i<Feature_Dictionary.WORDS_DIR_AFTER):
            if (lemphrase==''):  lemphrase += lemmer(afterTokArr[i])
            else:  lemphrase = lemmer(afterTokArr[i]) + ' ' + lemphrase
            newSenseEntry.increment_feature(word, partos, sense, lemphrase, Feature_Types.word1before+i)
            if (stemphrase==''):  stemphrase += stemmer(afterTokArr[i])
            else:  stemphrase = stemmer(afterTokArr[i]) + ' ' + stemphrase
            newSenseEntry.increment_feature(word, partos, sense, stemphrase, Feature_Types.word1before+i)
            i+=1






		# 

		# Create lemmer and stemmer
        lemmer = WordNetLemmatizer()
        stemmer = PorterStemmer()


        # Add n stems after target
        mw = Moving_Window(3, Window_Direction.FORWARD, rankDict)
        i=0
        position = i    # POSITION IN WHATEVER STRING CURRENTLY PROCESSING -- IE. DICTIONARY ENTRY or EXAMPLE -- would of had to tokenize already
        while (position<l and Feature_Dictionary.NUM_WORDS_BEFORE[partos]):
            stemWord = stemmer.stem(# EACH WORD IN SENTENCE)
            mw.add_word(stemWord)   # WHERE YOU ARE ADDING STEM TO MOVING WINDOW
            for j in range(1, self.MAX_NGRAM_CONSIDERED+1):
                ngram = mw.get_ngram(j)   # GET_NGRAM(1,2, or 3) --> gives you unigram, bigram, or trigram currently in the window
                if (ngram != None):		  # WIll produce None if not enough words or any word is trivial
                    newSenseEntry.increment_feature(word, partos, sense, ngram, Feature_Types.word1match+(j-1))    # Possibly add feature instead -- either way: counts will be ignored for dictionary features cause we just want to know what occurs
					# Feature_Types.word1match --> unigram feacture essentially
					# word2match --> bigram feature
					# word3match -- trigram feature
					#  +(j-1) --> Feature_Types == enum of types.  word2match = word1match+1 



        # Add n lems after target
        mw = Moving_Window(3, Window_Direction.FORWARD, rankDict)
        l = len(beforeTokArr)
        i=0
        position = i
        while (position<l and Feature_Dictionary.NUM_WORDS_BEFORE[partos]):
            lemWord = lemmer.lemmatize(beforeTokArr[position])
            mw.add_word(lemWord)
            for j in range(1, self.MAX_NGRAM_CONSIDERED+1):
                ngram = mw.get_ngram(j)
                if (ngram != None):
                    newSenseEntry.increment_feature(word, partos, sense, ngram, Feature_Types.word1match+(j-1))
        return newSenseEntry