import cv2
from pyzbar.pyzbar import decode
from binascii import a2b_base64
import requests
import json
import os

UPC_KEY = os.environ.get('UPC_KEY')


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
                print("Barcode data: ", barcode.data)
                print("Barcode type: ", barcode.type)

    return barcode.data


#find product in barcode API
def findProduct(upc):
    print("Querying product API with barcode")
    try:
        file = requests.get("https://api.upcdatabase.org/product/" + upc + "?apikey=" + UPC_KEY)
    except:
        print("ERROR: FAILED TO FIND PRODUCT BY BARCODE ID")
        return "Product not found"

    jsonData = file.json()
    print("Returned JSON data: ", jsonData)
    foodName = jsonData['description'] if jsonData['title'] == '' else jsonData['title']
    return foodName

#get product info from scan
def ScanAndSearchBarcode(image_data):
    barcodeData = BarcodeReader(image_data)
    if (barcodeData):
        barcodeData = str(barcodeData)
        code = barcodeData[2:-1]
        print("Barcode: ", code)
        productName = findProduct(code)
        return productName

    else:
        print("Barcode not detected or barcode is corrupted/blank")
        return "Barcode not found"