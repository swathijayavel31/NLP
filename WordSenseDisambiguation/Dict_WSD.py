from MyUtils import *
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
from Moving_Window import *
from nltk.corpus import wordnet
import random

#weights
CONTEXT_WORD_MATCH = 10
UNIGRAM = 1
BIGRAM = 5
TRIGRAM  = 10

MAX_NGRAM_CONSIDERED= 3

class Dict_WSD:

	def __init__(self):
		self.word_prediction_dict = {}
		self.dictionary = None
		self.rankDict = None

	#Methods


	def accuracy(self):
		num_correct_predictions = 0
		for line_num in self.word_prediction_dict:
			(predicted, actual) = self.word_prediction_dict[line_num]
			if (predicted == actual):
				num_correct_predictions += 1
		return float(num_correct_predictions)/float(len(self.word_prediction_dict.keys()))



	def calculate_vector_values(self, target_sense_vector_components, context_sense_vector_components, context_sense_vector_weights):

		# key = sense, value = list of values of components
		target_sense_vector_values = {}


		target_senses = target_sense_vector_components.keys()
		for i in range(len(target_senses)):
			sense = target_senses[i]
			target_sense_vector_values[sense] = [ 0 for z in range(len(target_sense_vector_components[sense]))]
			component_list = target_sense_vector_components[sense]
			for j in range(len(component_list)):

				target_phrase  = component_list[j]

				context_words = context_sense_vector_components.keys()
				for context_word in context_words:
					pos_keys = context_sense_vector_components[context_word].keys()
					for pos_key in pos_keys:
						context_senses = context_sense_vector_components[context_word][pos_key].keys()
						for context_sense in context_senses:
							ngram_list = context_sense_vector_components[context_word][pos_key][context_sense]
							weights_list = context_sense_vector_weights[context_word][pos_key][context_sense]

							for k in range(len(ngram_list)):
								context_def_phrase = ngram_list[k]
								if (context_def_phrase == target_phrase):
									target_sense_vector_values[sense][j] += weights_list[k]

			return target_sense_vector_values




	def generate_target_sense_vector_components(self, word, pos):
#		print "generate_target_sense_vector_components"
		target_sense_vector_components = self.generate_context_components(word)[str_to_pos(pos)]
		senses = target_sense_vector_components.keys()
		for sense in senses:
		 		target_sense_vector_components[sense] = self.eliminate_duplicates_from_list(target_sense_vector_components[sense])
		 		target_sense_vector_components[sense], _ = zip(*target_sense_vector_components[sense])
		return target_sense_vector_components


	#Given a line, generates the context words in that line after lemmatizing
	def generate_context_words(self, line): 
#		print "generate_context_words"
		context_word_list = []

		examplearr = re.split('\s*%%\s*', line)
		beforeTokArr = nltk.word_tokenize(examplearr[0])
		afterTokArr = nltk.word_tokenize(examplearr[2])

		stemmer = PorterStemmer()
		lemmer = WordNetLemmatizer()

		#String before target word
		mwStemBef = Moving_Window(1, Window_Direction.FORWARD, self.rankDict)
		mwLemBef = Moving_Window(1, Window_Direction.FORWARD, self.rankDict)
		for i in range(len(beforeTokArr)):
			stemWord = stemmer.stem(beforeTokArr[i])
			mwStemBef.add_word(stemWord)
			unigram = mwStemBef.get_ngram(1)
			if (unigram != None):
				#If the stem of the word is itself an actual word
				if wordnet.synsets(unigram):
					context_word_list += [unigram]

			lemWord = lemmer.lemmatize(beforeTokArr[i])
			mwLemBef.add_word(lemWord)
			unigram = mwLemBef.get_ngram(1)
			if (unigram != None):
				context_word_list += [unigram]

		#String after target word
		mwStemAft = Moving_Window(1, Window_Direction.FORWARD, self.rankDict)
		mwLemAft = Moving_Window(1, Window_Direction.FORWARD, self.rankDict)
		for i in range(len(afterTokArr)):
			stemWord = stemmer.stem(afterTokArr[i])
			mwStemAft.add_word(stemWord)
			unigram = mwStemAft.get_ngram(1)
			if (unigram != None):
				#If the stem of the word is itself an actual word
				if wordnet.synsets(unigram):
					context_word_list += [unigram]

			lemWord = lemmer.lemmatize(afterTokArr[i])
			mwLemAft.add_word(lemWord)
			unigram = mwLemAft.get_ngram(1)
			if (unigram != None):
				context_word_list += [unigram]

		context_word_list = self.eliminate_duplicates_from_list(context_word_list)

		return context_word_list


	def eliminate_duplicates_from_list(self, a_list):
		return  list(set(a_list))


	#Remove duplicate components from each vector
	def remove_duplicate_vector_components(self, context_sense_vector_components):
		words = context_sense_vector_components.keys()
		for word in words:
			pos_keys = context_sense_vector_components[word].keys()
			for pos_key in pos_keys:
				senses = context_sense_vector_components[word][pos_key].keys()
				for sense in senses: 
					context_sense_vector_components[word][pos_key][sense] = self.eliminate_duplicates_from_list(context_sense_vector_components[word][pos_key][sense])
		return context_sense_vector_components


	#Unzip the vector to create weight vector
	def create_weight_vectors(self, context_sense_vector_components):
	#	print "create_weight_vectors"
		context_sense_vector_weights = {}

		words = context_sense_vector_components.keys()
		for word in words:
			context_sense_vector_weights[word] = {}
			pos_keys = context_sense_vector_components[word].keys()
			for pos_key in pos_keys:
				context_sense_vector_weights[word][pos_key] = {}
				senses = context_sense_vector_components[word][pos_key].keys()
				for sense in senses: 
					context_sense_vector_components[word][pos_key][sense], context_sense_vector_weights[word][pos_key][sense] = zip(*context_sense_vector_components[word][pos_key][sense])

		return (context_sense_vector_components, context_sense_vector_weights)



	def generate_context_sense_vector_components(self, context_word_list):
#		print "generate_context_sense_vector_components"
		#key: word, value: {key : pos, value: {key: sensenum, value: context word components}}
		context_sense_vector_components = {}	
		for i in range(len(context_word_list)):
			word =  context_word_list[i]
			context_word_sense_component = self.generate_context_components( word)
			if (context_word_sense_component != None):
				context_sense_vector_components[word] =  context_word_sense_component

		return context_sense_vector_components

	 

	#Generate the n-gram components for an inputted context word
	def generate_context_components(self, word):
#		print "generate_context_components"
		#key: pos , value : {key: sense id , value: list of component terms}
		context_sense_components_dict = {}
		if word in self.dictionary.entries.keys():
			listOfEntries = self.dictionary.entries[word]
			for i in range(len(listOfEntries)):
				entry = listOfEntries[i]
				if not (entry.partOfSpeech in context_sense_components_dict.keys()): 
					context_sense_components_dict[entry.partOfSpeech] = {}
				if not (entry.senseNum in context_sense_components_dict[entry.partOfSpeech]):
					context_sense_components_dict[entry.partOfSpeech][entry.senseNum] = [(word, CONTEXT_WORD_MATCH)]

				for j in range(len(entry.definitions)): 
					component_list= self.get_ngram_from_def(entry.definitions[j])
					context_sense_components_dict[entry.partOfSpeech][entry.senseNum] += component_list

			return context_sense_components_dict
		else: 
			return None




	#Generate the ngrams for an inputted sentence(definition)
	def get_ngram_from_def(self, sentence): 
#		print "get_ngram_from_def"
		#ngram list
		component_list = []

		#key = 1,2,3 , value: list of ngrams
		ngram_dict = {}
		ngram_dict[1] = []
		ngram_dict[2] = []
		ngram_dict[3] = []

		ngram_weights = {}
		ngram_weights[1]= UNIGRAM
		ngram_weights[2]= BIGRAM
		ngram_weights[3]= TRIGRAM

		# Create lemmer and stemmer
		lemmer = WordNetLemmatizer()
		stemmer = PorterStemmer()

		mwStem = Moving_Window(3, Window_Direction.FORWARD, self.rankDict)
		mwLem = Moving_Window(3, Window_Direction.FORWARD, self.rankDict)

		sentence = sentence.split()		
		for i in range(len(sentence)):
			stemWord = stemmer.stem(sentence[i])
			mwStem.add_word(stemWord)
			for j in range(1, MAX_NGRAM_CONSIDERED+1):
				ngram = mwStem.get_ngram(j)
				if (ngram != None):
					ngram_dict[j] += [(ngram, ngram_weights[j])]

			lemWord = lemmer.lemmatize(sentence[i])
			mwLem.add_word(lemWord)
			for j in range(1, MAX_NGRAM_CONSIDERED+1):
				ngram = mwLem.get_ngram(j)
				if (ngram != None):
					ngram_dict[j] += [(ngram, ngram_weights[j])]

		ngram_dict[1] = self.eliminate_duplicates_from_list(ngram_dict[1])
		ngram_dict[2] = self.eliminate_duplicates_from_list(ngram_dict[2])
		ngram_dict[3] = self.eliminate_duplicates_from_list(ngram_dict[3])

		component_list = ngram_dict[1] + ngram_dict[2] + ngram_dict[3]

		return component_list



	def predict_sense(self, target_sense_vector_values): 
	#	print "predict_sense"
		senses = target_sense_vector_values.keys()
		max_sum = 0
		max_sense = -1
		for sense in senses:
			sense_sum = sum(target_sense_vector_values[sense])
			if (sense_sum >= max_sum):
				max_sum = sense_sum
				max_sense = sense

		return max_sense

	def write_prediction_to_file(self):
		f = open('results.txt', 'w')
		for line_count in self.word_prediction_dict:
			(predicted_sense, _) = self.word_prediction_dict[line_count]
			if (predicted_sense == None):
				predicted_sense = 1
			f.write(str(predicted_sense) + '\n')


	def run(self, filename, dict, rankDict, is_baseline): 
		self.dictionary = dict
		self.rankDict = rankDict

		f = open(filename, 'r')

		line_count = 1
		for line in f: 
			linearr = re.split('\s\|\s', line)
			word = linearr[0][0: len(linearr[0]) - 2]
			pos = linearr[0][len(linearr[0]) - 1: len(linearr[0])]
			actual_sense = linearr[1]
			context_line = linearr[2]

			if (is_baseline == True):
			 	rand = random.randint(1,15)
				if (1 <= rand) and (rand <= 7): 
					rand = 1
				rand_sense = str(rand)
				self.word_prediction_dict[line_count] = (rand_sense, actual_sense)
			#	self.word_prediction_dict[line_count] = (str(random.randint(1,15)), actual_sense)
			#	self.word_prediction_dict[line_count] = ('1', actual_sense)


			else:
			#	print "target_sense_vector_components"
				target_sense_vector_components = self.generate_target_sense_vector_components(word, pos)

	#			print "context_word_list"
				context_word_list = self.generate_context_words(context_line)


				context_sense_vector_components = self.generate_context_sense_vector_components(context_word_list)
	#			print "context_sense_vector_components"

				context_sense_vector_components = self.remove_duplicate_vector_components(context_sense_vector_components)
	#			print "context_sense_vector_components duplicates removed"

				(context_sense_vector_components,context_sense_vector_weights) = self.create_weight_vectors(context_sense_vector_components)
	#			print "(context_sense_vector_components,context_sense_vector_weights)"

				target_sense_vector_values = self.calculate_vector_values(target_sense_vector_components, context_sense_vector_components, context_sense_vector_weights)
	#			print "target_sense_vector_values"

				predicted_sense = self.predict_sense(target_sense_vector_values)
	#			print "predicted_sense"

				self.word_prediction_dict[line_count] = (predicted_sense, actual_sense)
	#			print "Add to word predictions"
	
			line_count += 1

		print "Accuracy: " + str(self.accuracy())

		self.write_prediction_to_file()

