from PIL import Image
import math
from io import BytesIO

# modified from: https://github.com/kusuwada/hexahue/


# Settings:
settings = {
	"max_width": 1200,
	"space": "all",
	"padding": {
		"top": 0,
		"right": 0,
		"bottom": 0,
		"left": 0,
	}
}


class HexahueMap():
	def __init__(self, space_color):
		pink = (255, 0, 255)
		red = (255, 0, 0)
		green = (0, 255, 0)
		yellow = (255, 255, 0)
		blue = (0, 0, 255)
		sky = (0, 255, 255)
		white = (255, 255, 255)
		gray = (128, 128, 128)
		black = (0, 0, 0)
		
		self.hmap = {}
		self.hmap[(pink, red, green, yellow, blue, sky)] = 'a'
		self.hmap[(red, pink, green, yellow, blue, sky)] = 'b'
		self.hmap[(red, green, pink, yellow, blue, sky)] = 'c'
		self.hmap[(red, green, yellow, pink, blue, sky)] = 'd'
		self.hmap[(red, green, yellow, blue, pink, sky)] = 'e'
		self.hmap[(red, green, yellow, blue, sky, pink)] = 'f'
		self.hmap[(green, red, yellow, blue, sky, pink)] = 'g'
		self.hmap[(green, yellow, red, blue, sky, pink)] = 'h'
		self.hmap[(green, yellow, blue, red, sky, pink)] = 'i'
		self.hmap[(green, yellow, blue, sky, red, pink)] = 'j'
		self.hmap[(green, yellow, blue, sky, pink, red)] = 'k'
		self.hmap[(yellow, green, blue, sky, pink, red)] = 'l'
		self.hmap[(yellow, blue, green, sky, pink, red)] = 'm'
		self.hmap[(yellow, blue, sky, green, pink, red)] = 'n'
		self.hmap[(yellow, blue, sky, pink, green, red)] = 'o'
		self.hmap[(yellow, blue, sky, pink, red, green)] = 'p'
		self.hmap[(blue, yellow, sky, pink, red, green)] = 'q'
		self.hmap[(blue, sky, yellow, pink, red, green)] = 'r'
		self.hmap[(blue, sky, pink, yellow, red, green)] = 's'
		self.hmap[(blue, sky, pink, red, yellow, green)] = 't'
		self.hmap[(blue, sky, pink, red, green, yellow)] = 'u'
		self.hmap[(sky, blue, pink, red, green, yellow)] = 'v'
		self.hmap[(sky, pink, blue, red, green, yellow)] = 'w'
		self.hmap[(sky, pink, red, blue, green, yellow)] = 'x'
		self.hmap[(sky, pink, red, green, blue, yellow)] = 'y'
		self.hmap[(sky, pink, red, green, yellow, blue)] = 'z'
		self.hmap[(black, white, white, black, black, white)] = '.'
		self.hmap[(white, black, black, white, white, black)] = ','
		self.hmap[(black, gray, white, black, gray, white)] = '0'
		self.hmap[(gray, black, white, black, gray, white)] = '1'
		self.hmap[(gray, white, black, black, gray, white)] = '2'
		self.hmap[(gray, white, black, gray, black, white)] = '3'
		self.hmap[(gray, white, black, gray, white, black)] = '4'
		self.hmap[(white, gray, black, gray, white, black)] = '5'
		self.hmap[(white, black, gray, gray, white, black)] = '6'
		self.hmap[(white, black, gray, white, gray, black)] = '7'
		self.hmap[(white, black, gray, white, black, gray)] = '8'
		self.hmap[(black, white, gray, white, black, gray)] = '9'
		if space_color == 'black':
			self.hmap[(black, black, black, black, black, black)] = ' '
		elif space_color == 'white':
			self.hmap[(white, white, white, white, white, white)] = ' '
		elif space_color == 'all':
			self.hmap[(black, black, black, black, black, black)] = ' '
			self.hmap[(white, white, white, white, white, white)] = ' '
		else:
			raise Exception('[Error] invalid space setting: ' + space_color)


def hexahue_decode(img):
	hexahue_map = HexahueMap(settings["space"])
	padding = settings["padding"]
	width, height = img.size
	decoded = ""
	for hi in range((height - padding['top'] - padding['bottom']) // 3):
		for wi in range((width - padding['left'] - padding['right']) // 2):
			block = (
				img.getpixel((wi * 2 + 0 + padding['left'], hi * 3 + 0 + padding['top'])),
				img.getpixel((wi * 2 + 1 + padding['left'], hi * 3 + 0 + padding['top'])),
				img.getpixel((wi * 2 + 0 + padding['left'], hi * 3 + 1 + padding['top'])),
				img.getpixel((wi * 2 + 1 + padding['left'], hi * 3 + 1 + padding['top'])),
				img.getpixel((wi * 2 + 0 + padding['left'], hi * 3 + 2 + padding['top'])),
				img.getpixel((wi * 2 + 1 + padding['left'], hi * 3 + 2 + padding['top'])))
			try:
				decoded += hexahue_map.hmap[block]
			except KeyError:
				raise Exception(f'[Error] Current decode message: {decoded} \nNo Hexahue Mapping found: {repr(block)}')
	
	return decoded


def hexahue_encode(message):
	hexahue_map = HexahueMap(settings["space"])
	padding = settings["padding"]
	# check message for non allowed chars
	for m in message:
		if not (m.isalpha() or m.isdigit() or (m in [',', '.', ' '])):
			raise Exception('[Error] invalid message input: ' + m)
	# create image
	w_num = min((settings['max_width'] - padding['right'] - padding['left']) // 2, len(message))
	h_num = math.ceil(len(message) / w_num)
	width = w_num * 2 + padding['right'] + padding['left']
	height = h_num * 3 + padding['top'] + padding['bottom']
	img = Image.new('RGB', (width, height), [k for k, v in hexahue_map.hmap.items() if v == ' '][0][0])
	for i in range(len(message)):
		m = message[i]
		if m.isupper():
			m = m.lower()
		block = [k for k, v in hexahue_map.hmap.items() if v == m][0]
		hi = i // w_num
		wi = i % w_num
		for h in range(3):
			for w in range(2):
				img.putpixel((wi * 2 + w + padding['left'], hi * 3 + h + padding['top']), block[h * 2 + w])
	return img


def main(text, encode=True, steps=0):
	if encode:
		img = hexahue_encode(text)
		return img, steps
	else:
		image = Image.open(BytesIO(text))
		decoded = hexahue_decode(image)
		return decoded, steps


if __name__ == '__main__':
	mode = input('input mode (d: decode, e: encode) > ')
	if mode == 'd' or mode == 'D' or mode == 'decode':
		filename = input('input source filename > ')
		img = Image.open(filename)
		print(hexahue_decode(img))
	elif mode == 'e' or mode == 'E' or mode == 'encode':
		filename = input('input output image filename > ')
		message = input('input message for encript > ')
		output_img = hexahue_encode(message)
		output_img.save(filename)
	else:
		raise Exception('[Error] invalid mode input!')
