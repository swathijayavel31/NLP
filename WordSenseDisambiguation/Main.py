from Dictionary import *
from Rank_Dictionary import *
from Features import *
from Dict_WSD import *
# from blah import *



# ----- GLOBALS ------
optionSelected = 0
dict = Dictionary()
rankdict = None
featdict = None
EXIT_OPTION = 9



while (optionSelected!=EXIT_OPTION):

    print("""
----- WORD SENSE DISAMBIGUATION -----
1 - Import WordNet 2.1 dictionary
2 - Import class XML dictionary
3 - Import word frequency rank list
4 - Train Supervised WSD Model
5 - Perform Supervised WSD on Test Data
6 - Perform Supervised WSD on Validation Data
7 - Perform Dictionary-based WSD
8 - Baseline Accuracy for Dictionary-based WSD
9 - Exit
""")



    #try:
    optionSelected = input("""
Type the number of desired option and press [Enter]:  """)

#    except Exception as e:
#        print("""
#Input is not a valid number.
#""")



    if (optionSelected==1):
        #try:
            foldername = raw_input("""
Type the directory path where the Wordnet 2.1 data and index files are stored
(no input if current directory) and press [Enter]:
""")
#        except Exception as e:
#            print("""
#Input is not valid
#""")
        #try:
            dict.add_wordnet_entries(foldername)
            dict.save_short_wordnet_sense(foldername)
            #dict.print_entries()
            #dict.print_entry('connect')
        #except Exception as e:
        #    print(e)



    elif (optionSelected==2):
        #try:
            foldername = raw_input("""
Type the directory path where the class dictionary.xml files is stored
(no input if current directory) and press [Enter]:
""")
#        except Exception as e:
#            print("""
#Input is not valid
#""")
        #try:
            dict.add_class_dict_entries(foldername)
            dict.match_wordnet_to_class_sense()
            #dict.print_wordnetMap('base')
            #dict.print_entries()
            #dict.print_entry('complain')
        #except Exception as e:
        #    print(e)



    elif (optionSelected==3):
        #try:
            foldername = raw_input("""
Type the directory path where the Word_Frequency_List.txt file is stored
(no input if current directory) and press [Enter]:
""")
#        except Exception as e:
#            print("""
#Input is not valid
#""")
        #try:
            rankdict = Rank_Dictionary()
            rankdict.import_list(foldername)
            #print(rankdict)
        #except Exception as e:
        #    print(e)
    


    elif (optionSelected==4):
        #try:
            filepath = raw_input("""
Type the file path name where the training file is stored
(path can be relative) and press [Enter]:
""")
#        except Exception as e:
#            print("""
#Input is not valid
#""")
        #try:
            featdict = Feature_Dictionary(rankdict)
            featdict.train_supervised_wsd(filepath)
            featdict.calculate_supervised_wsd_probs()
            featdict.replace_sense_vectors_with_full_vectors()
            print(featdict)
        #except Exception as e:
        #    print(e)



    elif (optionSelected==5):
        if (featdict==None):
            print("""
Supervised WSD Model has not yet been trained.
""")
        else:
            #try:
                foldername = raw_input("""
Type the file path on which you want to perform Supervised WSD
(path can be relative) and press [Enter]:
""")
#            except Exception as e:
#                print("""
#Input is not valid
#""")
            #try:
                featdict = Feature_Dictionary()
                featdict.train_supervised_wsd(filepath, rankdict)
                featdict.calculate_supervised_wsd_probs()
                featdict.replace_sense_vectors_with_full_vectors()
            #except Exception as e:
            #    print(e)
    


    elif (optionSelected==6):
        pass



    elif (optionSelected==7):
        filename = raw_input("""Type the name of the file containing the test data: """)
        d = Dict_WSD()
        d.run(filename, dict, rankdict, False)

    elif (optionSelected==8):
        filename = raw_input("""Type the name of the file containing the test data: """)
        d = Dict_WSD()
        d.run(filename, dict, rankdict, True)



       
    elif (optionSelected!=EXIT_OPTION):
        print("""
Input is not a valid number option.
        """)