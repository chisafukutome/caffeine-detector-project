import pandas

def findProduct(upc):
    file = pandas.read_html("https://www.upcdatabase.com/item/" + str(upc))
    return(file[0][2][2])

