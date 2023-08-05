import grtoolkit as gr 
import sys, os

parentFolder = os.path.dirname(sys.argv[0])
# author = "tim ferris"

print("Generate Quotes from Goodreads website.\n")
author = input("Author to search:\n")
book = input("Book name as per Goodreads:\n")


# pickle = f"{parentFolder}\\{author}"
# gr.Quotes.generateDB(author,saveFile=pickle)
db = gr.Quotes.generateDB(author)
# db = gr.Quotes.loadDB(pickle)
# titles = gr.Quotes.bookTitles(db)
# print(titles)

# qts = gr.Quotes.filterQuotesByBook(db,titles[5])
qts = gr.Quotes.filterQuotesByBook(db,book)
# print(qts)

gr.Quotes.export(qts,f"{parentFolder}\\{author}.txt",enc=1)

# for quote in db:
#     print(quote)