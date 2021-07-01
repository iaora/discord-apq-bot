import pytesseract
import urllib
import cv2
from io import BytesIO
from requests import get
import numpy as np
#from PIL import Image

"""Converts processed image (removed black text, increased size) into greyscale """
def img_to_greyscale(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	white_img = cv2.GaussianBlur(img, (5, 5), 0)
	(thresh, img_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	return img_bw

"""Converts all black text into white. increase image size"""
def clean_img(img):
	img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
	# Load the image and convert to HSV colourspace
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	# Define lower and uppper limits of what we call "black"
	lo=np.array([0,0,0])
	hi=np.array([0,0,255])

	# Mask image to only select black
	mask=cv2.inRange(hsv,lo,hi)

	# Change image to white where we found black
	white_img = img.copy()
	white_img[mask>0]=(255,255,255)
	return img_to_greyscale(white_img)

"""Takes image URl and parses it into an image object"""
def url_to_img(url):
	img_resp = get(url, stream=True).raw
	img = np.asarray(bytearray(img_resp.read()), dtype="uint8")
	return cv2.imdecode(img, cv2.IMREAD_COLOR)

"""Use python tesseract to convert image into list of strings based on the image"""
def img_to_text(img_bw):
	return pytesseract.image_to_string(img_bw, lang='eng').splitlines()

"""First method to get called by the Discord bot. Takes in the message cattachements and returns a list of CLEANED (removed spaces/empty) strings from the image"""
def process_image_to_text(url):
	img = url_to_img(url)
	img_bw = clean_img(img)
	img_to_str = img_to_text(img_bw)

	return [x.strip() for x in img_to_str if x.strip()]
