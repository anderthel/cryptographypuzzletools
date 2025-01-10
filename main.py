import random
import tempfile
from pathlib import Path
from tqdm import tqdm
from shutil import copy

from handlers.zipper import zipper, dezipper
import handlers.text_simple as text_simple
import handlers.image_hexahue as image_hexahue
import handlers.audio_nato as audio_nato
import handlers.audio_morse as audio_morse
from handlers.passgen import passgen


# Settings
ciphers = {
	# format:
	# "name": [module.function, "cipher type(for passgen)"],

	# text_simple
	"a1z26": [text_simple.a1z26, "lowercase_punc"],
	"atbash": [text_simple.atbash, "text_full"],
	"bacon": [text_simple.bacon, "text_full"],
	"base16": [text_simple.base16, "text_full"],
	"base32": [text_simple.base32, "text_full"],
	"base64": [text_simple.base64, "text_full"],
	"base85": [text_simple.base85, "text_full"],
	"binary": [text_simple.binary, "text_full"],
	"braille": [text_simple.braille, "text_full_lowercase"],
	"decimal": [text_simple.decimal, "text_full"],
	"ceasar": [text_simple.ceasar, "text_full"],
	"html": [text_simple.html, "text_full"],
	"morse": [text_simple.morse, "text_full_lowercase"],
	"nato": [text_simple.nato, "text_full"],
	"octal": [text_simple.octal, "text_full"],
	"rot47": [text_simple.rot47, "text_full"],
	"unicode": [text_simple.unicode, "text_full"],
	# "hashes": [text_simple.hashes, "hashes"],		# no decode

	# images
	"image_hexahue": [image_hexahue.main, "image_hexahue"],

	# audio
	# "audio_nato": [audio_nato.main, "audio_nato"],			# no decode
	"audio_morse": [audio_morse.main, "audio_morse"],
}


def random_cipher():
	cipher = random.choice(list(ciphers.keys()))
	func = ciphers[cipher][0]
	cipher_type = ciphers[cipher][1]
	return cipher_type, cipher, func


def generate(file, total):
	previous_file = file
	ciphers_used = {}

	# if ending file does not exist
	if not Path(file).exists():
		with open(file, "w") as f:
			f.write("Woot you won!")

	with tempfile.TemporaryDirectory(dir=".") as tmpdir:
		copy(file, f"{tmpdir}/{file}")
		for i in tqdm(range(1, total + 1)):
			# print(i)
			cipher_type, cipher, func = random_cipher()
			# print(cipher)
			ciphered_pw, password, steps = passgen(cipher_type, cipher, func)
			# print(password)
			previous_file = zipper(previous_file, ciphered_pw, password, tmpdir, cipher_type)
			# print(previous_file)
			ciphers_used[i] = [cipher, steps]
		
		# path
		Path(f"{tmpdir}/{previous_file}").rename("./output.zip")
		print(ciphers_used)


def crack(file, order):
	total = list(order.keys())[-1]
	with tempfile.TemporaryDirectory(dir=".") as tmpdir:
		copy(file, f"{tmpdir}/{file}")
		while total > 0:
			cipher, steps = order[total]
			# print(cipher)
			func, cipher_type = ciphers[cipher]
			text = dezipper(file, tmpdir)
			if cipher_type not in ["image_hexahue", "audio_nato", "audio_morse"]:
				text = text.decode("utf-8")
			passwd = func(text, False, steps)[0]
			passwd = passwd.encode("utf-8")
			file = dezipper(file, tmpdir, passwd)
			total -= 1
		Path(f"{tmpdir}/{file}").rename(f"./{file}")
		print(file)


if __name__ == '__main__':
	# generate("Ending.txt", 100)
	order = {1: ['braille', 0], 2: ['rot47', 0], 3: ['a1z26', 0], 4: ['ceasar', 5], 5: ['unicode', 1], 6: ['rot47', 0], 7: ['image_hexahue', 0], 8: ['atbash', 0], 9: ['octal', 4], 10: ['binary', 1], 11: ['unicode', 1], 12: ['base85', 4], 13: ['decimal', 8], 14: ['a1z26', 0], 15: ['binary', 2], 16: ['audio_morse', 0], 17: ['rot47', 0], 18: ['base32', 3], 19: ['base85', 7], 20: ['image_hexahue', 0], 21: ['base32', 9], 22: ['atbash', 0], 23: ['nato', 0], 24: ['base85', 2], 25: ['image_hexahue', 0], 26: ['a1z26', 0], 27: ['html', 2], 28: ['ceasar', 9], 29: ['a1z26', 0], 30: ['ceasar', 10], 31: ['base16', 1], 32: ['binary', 3], 33: ['a1z26', 0], 34: ['atbash', 0], 35: ['braille', 0], 36: ['morse', 0], 37: ['image_hexahue', 0], 38: ['html', 1], 39: ['base64', 5], 40: ['bacon', 0], 41: ['image_hexahue', 0], 42: ['base16', 1], 43: ['audio_morse', 0], 44: ['base64', 6], 45: ['binary', 1], 46: ['a1z26', 0], 47: ['nato', 0], 48: ['base85', 4], 49: ['atbash', 0], 50: ['nato', 0], 51: ['bacon', 0], 52: ['html', 3], 53: ['image_hexahue', 0], 54: ['bacon', 0], 55: ['a1z26', 0], 56: ['base16', 1], 57: ['image_hexahue', 0], 58: ['html', 3], 59: ['audio_morse', 0], 60: ['morse', 0], 61: ['atbash', 0], 62: ['base64', 6], 63: ['base64', 9], 64: ['rot47', 0], 65: ['a1z26', 0], 66: ['unicode', 2], 67: ['image_hexahue', 0], 68: ['morse', 0], 69: ['ceasar', 12], 70: ['ceasar', 22], 71: ['html', 2], 72: ['unicode', 3], 73: ['bacon', 0], 74: ['decimal', 3], 75: ['image_hexahue', 0], 76: ['ceasar', 9], 77: ['base16', 2], 78: ['ceasar', 2], 79: ['braille', 0], 80: ['bacon', 0], 81: ['ceasar', 12], 82: ['octal', 8], 83: ['nato', 0], 84: ['audio_morse', 0], 85: ['rot47', 0], 86: ['audio_morse', 0], 87: ['base85', 10], 88: ['octal', 5], 89: ['unicode', 2], 90: ['octal', 7], 91: ['image_hexahue', 0], 92: ['nato', 0], 93: ['decimal', 6], 94: ['image_hexahue', 0], 95: ['morse', 0], 96: ['html', 1], 97: ['morse', 0], 98: ['base85', 2], 99: ['octal', 9], 100: ['unicode', 3]}
	file = "./output.zip"
	crack(file, order)
