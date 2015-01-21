import re



class ArgErr(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg



class POS:
    Adj = 0
    Adv = 1
    Noun = 2
    Verb = 3
    Not_Assigned = 4



def replace_underscores(phrase):
    newPhrase = ''
    for i in range(len(phrase)):
        if (phrase[i]=='_'):  newPhrase += ' '
        else:  newPhrase += phrase[i]
    return newPhrase

def str_to_pos(str):
    if (str=='n'):  return POS.Noun
    elif (str=='v'):  return POS.Verb
    elif (str=='a'):  return POS.Adj
    elif (str=='r'):  return POS.Adv
    else:
        raise ArgErr('Input str not valid in str_to_pos\n')

def valid_word(token):
    match = re.match('[a-zA-Z0-9_-]+\Z', token)
    return (not (match==None))

def replace_periods(phrase):
    newPhrase = ''
    for i in range(len(phrase)):
        if (phrase[i]=='.'):  newPhrase += '_'
        else:  newPhrase += phrase[i]
    return newPhrase