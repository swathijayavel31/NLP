from Document_Dictionary import *
from MyUtils import *
import nltk

#>>> tagged_sent = nltk.pos_tag(["i", "love", "popcorn"])
#>>> tagged_sent = [ (word, simplify_wsj_tag(tag)) for word, tag in tagged_sent]



trans_probs = [][]
em_probs = [][]

POS_weight_vector = [1,2,3,4]

def run_test_data(path):
	doc_dict = Document_Dictionary()
	doc_dict.import_documents(path)
	for doc in doc_dict.documents:
		for sent in doc.sentences:

			prev_state = START
			for l_word in sent.lem_words:
				current_state = get_state(prev_state, l_word)
				l_word.classififcation = current_state
				prev_state = current_state



def get_state(prev_state, word):
	max_prod = 0
	max_next_state = NA

	for i in range(len(trans_probs)):
		for j in range(len(em_probs)):
			new_prod = trans_probs[i][prev_state]*em_probs[word][i]
			if( new_prod > max_prod):
				max_prod = new_prod
				max_next_state = i

	return max_next_state










