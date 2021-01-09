import pytesseract
import urllib
import cv2
from io import BytesIO
from requests import get
from numpy import asarray
#from PIL import Image

def process_image(url):
	img_resp = get(url, stream=True).raw
	#img = Image.open(BytesIO(img_resp.content))
	img = asarray(bytearray(img_resp.read()), dtype="uint8")

	#resp = urllib.urlopen(url)
	#image = np.asarray(bytearray(resp.read()), dtype="uint8")
	img = cv2.imdecode(img, cv2.IMREAD_COLOR)
	
	img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.GaussianBlur(img, (5, 5), 0)
	thr = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	return img

def accept_image(img_obj):
	img = process_image(img_obj.url)

	img_info = pytesseract.image_to_string(img, lang='eng')
	print (img_info.splitlines())
	#img_info.splitlines()[10]
	import pdb; pdb.set_trace()
	
def jams_sucks_a_lot():
	print(':spit:')
