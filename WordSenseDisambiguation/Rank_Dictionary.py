#IDF implementation

#Don't really need to touch
class Rank_Dictionary(object):
    
    def __init__(self):
        self.rankdict = {}
        self.RANK_BOUND = 128
        self.baseFilename = 'Word_Frequency_List.txt'

    def __str__(self):
        string = '\n----- RANK DICTIONARY -----\n'
        keys = self.rankdict.keys()
        keys.sort()
        for i in range(len(keys)):
            key = keys[i]
            string += key + ':  ' + str(self.rankdict[key]) + '\n'
        return string

    #max size is 5000
    def import_list(self, folder):
        # Form filename
        filename = ''
        if (folder==''):  filename = self.baseFilename
        else:  filename = folder + '/' + baseFilename
        # open file
        f = open(filename, 'r')
        # read into dictionary
        i=0
        curline = f.readline()
        while (curline!=''):
            curline = curline.strip()[3:]
            if (curline not in self.rankdict):
                self.rankdict[curline] = i
                i+=1
            curline = f.readline()
        # close file
        f.close()

    def top_rank(self, tag):
        if ((tag in self.rankdict) and (self.rankdict[tag]<self.RANK_BOUND)):
            return True
        else:
            return False