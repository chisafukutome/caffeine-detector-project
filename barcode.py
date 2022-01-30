import pandas
import cv2
from pyzbar.pyzbar import decode
from bs4 import BeautifulSoup as BS
import base64
from io import BytesIO
from PIL import Image
from binascii import a2b_base64
import numpy


#parse html for barcode img URI
def ParseHTMLForBarcodeImg():
    with open("index.html") as fp:
        soup = BS(fp, 'html.parser')
    print("SOUP: ", soup)
  
# Scan and decode barcode
def BarcodeReader(image_data):
    binary_data = a2b_base64(image_data)
    img1 = open('img.png', 'wb')
    img1.write(binary_data)
    img1.close()

    # im_byte_arr = bytes(image_data, encoding="ascii")
    # img_plugin = Image.open(BytesIO(base64.b64decode(im_byte_arr))) 
    # pil_image = img_plugin.convert('RGB') 
    # img = numpy.array(pil_image)

    img = cv2.imread('img.png') #becomes ndarray
    # img = Image.fromarray(img) #becomes Images
    img = cv2.flip(img, 1)

    #Convert RGB to BGR
    # img = img[:, :, ::-1].copy()
    # print(type(img))
    # cv2.imshow("Test", img)
    # img = Image.fromarray(img)

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
    cv2.waitKey(0)
    cv2.destroyAllWindows()
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