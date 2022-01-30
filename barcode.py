import pandas
import cv2
from pyzbar.pyzbar import decode
from bs4 import BeautifulSoup as BS
import base64
from io import BytesIO
from PIL import Image
from binascii import a2b_base64
import numpy


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
                 
    #Display the image
    # cv2.imshow("Image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return barcode.data


#find product in barcode API
def findProduct(upc):
    file = pandas.read_html("https://www.upcdatabase.com/item/" + str(upc))
    return(file[0][2][2])

def ScanAndSearchBarcode(image_data):
    code = BarcodeReader(image_data)
    if (code):
        barcodeData = str(code)
        code = barcodeData[3:-1]
        productName = findProduct(code)
        print("Product Name: ", productName)
    else:
        print("Barcode not detected or barcode is corrupted/blank")