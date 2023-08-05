import grtoolkit as gr 
import sys, os

# parentFolder = os.path.dirname(sys.argv[0])
parentFolder = os.getcwd()
# author = "tim ferris"

print("Generate Quotes from Goodreads website.\n")
author = input("Author to search:\n")
book = input("Book name as per Goodreads:\n")
saveFile = f"{author}.txt"

# pickle = f"{parentFolder}\\{author}"
# gr.Quotes.generateDB(author,saveFile=pickle)
if os.path.isfile(saveFile):
    db = gr.Quotes.loadDB(saveFile)
else:
    db = gr.Quotes.generateDB(author, saveFile=f"{author}.txt")
# titles = gr.Quotes.bookTitles(db)
# print(titles)

# qts = gr.Quotes.filterQuotesByBook(db,titles[5])
qts = gr.Quotes.filterQuotesByBook(db,book)
# print(qts)

gr.Quotes.export(qts,f"{parentFolder}\\{saveFile}",enc=1)

# for quote in db:
#     print(quote)