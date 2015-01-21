from Document_Dictionary import *



path = raw_input("""
Type the filename (full path or relative file) where the training data is
stored and press [Enter]:
""")

document_dict = Document_Dictionary()
document_dict.import_documents(path)
print(document_dict)