import io
import os
from google.cloud import vision


GOOGLE_KEY_ID=os.environ.get("GOOGLE_KEY_ID")
GOOGLE_PRIVATE_KEY=os.environ.get("GOOGLE_PRIVATE_KEY")
GOOGLE_CLIENT_EMAIL=os.environ.get("GOOGLE_CLIENT_EMAIL")
GOOGLE_CLIENT_ID=os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_CERT_URL=os.environ.get("GOOGLE_CLIENT_CERT_URL")


GOOGLE_APPLICATION_CREDENTIALS={
  "type": "service_account",
  "project_id": "caffeine-counter-test",
  "private_key_id": GOOGLE_KEY_ID,
  "private_key": GOOGLE_PRIVATE_KEY,
  "client_email": GOOGLE_CLIENT_EMAIL,
  "client_id": GOOGLE_CLIENT_ID,
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": GOOGLE_CLIENT_CERT_URL
}

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="caffeine-counter-test-e361ec2882be.json"

def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
def detect_image(path):
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.relpath(path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)

def detect_both(path):
    detect_text(path)
    detect_image(path)

detect_both("./images/brisk.png")
