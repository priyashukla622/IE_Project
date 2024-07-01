
import os
import pathlib
import time
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

'''
This sample crops an existing image then uses the Computer Vision SDK 
to extract text from the cropped image. The extracted text is
returned along with bounding boxes. There is an optional feature to draw a rectangle
around the text you want to crop, then show the image.

Prerequisites:
1. Install the Computer Vision SDK:
pip install --upgrade azure-cognitiveservices-vision-computervision
2. Create and add an Images folder to your working directory. 
Add the images you want to crop into the Images folder. Once the script runs, cropped images will
automatically be added to the CroppedImages folder.
3. Make sure your images are either JPG or PNG. Change the file extension in the code if needed.

Computer Vision SDK: https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-vision-computervision/azure.cognitiveservices.vision.computervision?view=azure-python
Computer Vision API: https://westus.dev.cognitive.microsoft.com/docs/services/5cd27ec07268f6c679a3e641/operations/56f91f2e778daf14a499f21b
'''

'''
Authenticate Computer Vision client
'''
key = 'fa2d8a13572341cbadbce74c1bfc0516'
endpoint = 'https://priya24.cognitiveservices.azure.com/'

client = ComputerVisionClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(key))
image_folder = pathlib.Path("/Users/navgurukul/OneDrive/Desktop/HVA_Task/PS1-TR-Data/PS1-TR-Data/images")


def from_image(image):
    with BytesIO() as byte_stream:
        image.save(byte_stream, format="jpeg")
        byte_stream.seek(0)

        try:
            result = client.recognize_printed_text_in_stream(byte_stream)
            extracted_text = ""
            for region in result.regions:
                for line in region.lines:
                    for word in line.words:
                        extracted_text += word.text
            return extracted_text.strip()
        except Exception as e:
            time.sleep(1)

wrong = 0
correct = 0
for image_file in image_folder.glob("*.jpg"):
    with Image.open(image_file) as image:
        extract_text = from_image(image)
        join_text = "".join(extract_text.split())
        groundtruth_folder = f"/Users/navgurukul/OneDrive/Desktop/HVA_Task/PS1-TR-Data/PS1-TR-Data/groundtruth/{image_file.stem}.txt"
        with open(groundtruth_folder, "r") as file:
            expected_text = file.read().strip()
            time.sleep(1)
            if join_text == expected_text:
                print(f"Image_text {join_text}, File_text: {expected_text}, Matched")
                correct = correct + 1
            else:
                print(f"Image_text {join_text}, File_text {expected_text},Not matched")
                wrong += 1
print("correct", correct)
print("wrong", wrong)





