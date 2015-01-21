from Document_Dictionary import *



class Classification:
    POS = 0
    NEU = 1
    NEG = 2
    NA = 3

class States:
	POS = 0
	NEU = 1
	NEG = 2
	START = 3



def string_to_class(string):
    if (string == 'pos'): return Classification.POS
    elif (string == 'neu'): return Classification.NEU
    elif (string == 'neg'): return Classification.NEG
    else: return Classification.NA




class POS: 
	N = 0
	V = 1
	ADJ = 2
	ADV = 3