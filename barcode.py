from asyncio.windows_events import NULL
import pandas
import cv2
from pyzbar.pyzbar import decode
from binascii import a2b_base64
import requests
import json


# Scan and decode barcode
def BarcodeReader(image_data):
    binary_data = a2b_base64(image_data)
    img1 = open('img_to_scan.png', 'wb')
    img1.write(binary_data)
    img1.close()

    img = cv2.imread('img_to_scan.png') #becomes ndarray
    img = cv2.flip(img, 1)

    # Decode the barcode image
    detectedBarcodes = decode(img)
      
    # If not detected then print the message
    if not detectedBarcodes:
        # print("Barcode Not Detected or your barcode is blank/corrupted!")
        return False
    else:
       
          # Traverse through all the detected barcodes in image
        for barcode in detectedBarcodes: 
           
            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect
             
            # Put the rectangle in image using
            # cv2 to heighlight the barcode
            cv2.rectangle(img, (x-10, y-10),
                          (x + w+10, y + h+10),
                          (255, 0, 0), 2)
             
            if barcode.data!="":
               
            # Print the barcode data
                print(barcode.data)
                print(barcode.type)
                 
    return barcode.data


#find product in barcode API
def findProduct(upc):
    '''
    try:
        file = pandas.read_html("https://www.upcdatabase.com/item/" + str(upc))
        print("FIND PRODUCT FILE: ", file)
        return(file[0][2][2])
    except:
        print("ERROR: COULD NOT FIND PRODUCT BY BARCODE ID")
        return "Product not found"
    '''
   try:
        file = requests.get("https://api.upcdatabase.org/product/" + upc + "?apikey=" + UPC_KEY)
        jsonData = json.loads(file)
        return(jsonData['title'])
   except:
        print("ERROR: COULD NOT FIND PRODUCT BY BARCODE ID")
        return "Product not found"
        


def ScanAndSearchBarcode(image_data):
    code = BarcodeReader(image_data)
    if (code):
        barcodeData = str(code)
        code = barcodeData[3:-1]
        productName = findProduct(code)
        return productName

    else:
        print("Barcode not detected or barcode is corrupted/blank")
        return "Barcode not found"
