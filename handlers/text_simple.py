import base64 as base
import random
import hashlib


def base85(text, encode=True, steps=0):			# using ipv6 instead of standered
	if steps == 0:
		steps = random.randint(1, 10)
	if encode:
		for i in range(steps):
			text = base.b85encode(bytes(text, "utf-8"))
			text = text.decode("utf-8")
		return text, steps
	else:
		for i in range(steps):
			text = base.b85decode(bytes(text, "utf-8"))
			text = text.decode("utf-8")
		return text, steps


def base64(text, encode=True, steps=0):
	if steps == 0:
		steps = random.randint(1, 10)
	if encode:
		for i in range(steps):
			text = base.b64encode(bytes(text, "utf-8"))
			text = text.decode("utf-8")
		return text, steps
	else:
		for i in range(steps):
			text = base.b64decode(bytes(text, "utf-8"))
			text = text.decode("utf-8")
		return text, steps


def base32(text, encode=True, steps=0):
	if steps == 0:
		steps = random.randint(1, 10)
	if encode:
		for i in range(steps):
			text = base.b32encode(bytes(text, "utf-8"))
			text = text.decode("utf-8")
		return text, steps
	else:
		for i in range(steps):
			text = base.b32decode(bytes(text, "utf-8"))
			text = text.decode("utf-8")
		return text, steps


def base16(text, encode=True, steps=0):
	if steps == 0:
		steps = random.randint(1, 10)
	if encode:
		for i in range(steps):
			text = base.b16encode(bytes(text, "utf-8")).decode("utf-8")
		return text, steps
	else:
		for i in range(steps):
			text = base.b16decode(bytes(text, "utf-8")).decode("utf-8")
		return text, steps


def ceasar(text, encode=True, steps=0):
	lower = 'abcdefghijklmnopqrstuvwxyz'
	upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	output = ""
	if steps == 0:
		steps = random.randint(1, 25)
	if encode:
		for char in text:
			if char in lower:
				output += lower[((lower.find(char) + steps) % 26)]
			elif char in upper:
				output += upper[((upper.find(char) + steps) % 26)]
			else:
				output += char
		return output, steps
	else:
		for char in text:
			if char in lower:
				output += lower[((lower.find(char) - steps) % 26)]
			elif char in upper:
				output += upper[((upper.find(char) - steps) % 26)]
			else:
				output += char
		return output, steps


def decimal(text, encode=True, steps=0):
	if steps == 0:
		steps = random.randint(1, 10)
	if encode:
		for i in range(steps):
			text = " ".join(str(format(ord(char), "d")) for char in text)
		return text, steps
	else:
		for i in range(steps):
			text = "".join(str(format(int(char, 10), "c")) for char in text.split())
		return text, steps


def octal(text, encode=True, steps=0):
	if steps == 0:
		steps = random.randint(1, 10)
	if encode:
		for i in range(steps):
			text = " ".join(str(format(ord(char), "o")) for char in text)
		return text, steps
	else:
		for i in range(steps):
			text = "".join(str(format(int(char, 8), "c")) for char in text.split())
		return text, steps


def unicode(text, encode=True, steps=0):
	if steps == 0:
		steps = random.randint(1, 3)
	if encode:
		for i in range(steps):
			text = "".join(f'\\u{base.b16encode(bytes(char, "utf-8")).decode("utf-8").zfill(4)}' for char in text)
		return text, steps
	else:
		for i in range(steps):
			text = "".join(base.b16decode(bytes(char.lstrip("0"), "utf-8")).decode("utf-8") for char in text.split("\\u")[1:])
		return text, steps


def html(text, encode=True, steps=0):
	if steps == 0:
		steps = random.randint(1, 3)
	if encode:
		for i in range(steps):
			text = "".join(f'&#{str(format(ord(char), "d"))};' for char in text)
		return text, steps
	else:
		for i in range(steps):
			text = "".join(str(format(int(char.rstrip(";"), 10), "c")) for char in text.split("&#")[1:])
		return text, steps


def atbash(text, encode=True, steps=0):		# no steps
	if encode:
		return text[::-1], steps
	else:
		return text[::-1], steps


def binary(text, encode=True, steps=0):
	if steps == 0:
		steps = random.randint(1, 3)
	if encode:
		for i in range(steps):
			text = " ".join(str(format(ord(char), "08b")) for char in text)
		return text, steps
	else:
		for i in range(steps):
			text = "".join(str(format(int(char, 2), "c")) for char in text.split())
		return text, steps


def rot47(text, encode=True, steps=0):		# no steps (add)
	output = []
	for num in range(len(text)):
		char = ord(str(text[num]))
		if char >= 33 and char <= 126:
			output.append(chr(33 + ((char + 14) % 94)))
		else:
			output.append(text[num])
	return ''.join(output), steps


def nato(text, encode=True, steps=0):		# No space + no steps
	inkey = {
		"a": "alfa", "b": "bravo", "c": "charlie", "d": "delta", "e": "echo", "f": "foxtrot", "g": "golf", "h": "hotel", "i": "india", "j": "juliett", "k": "kilo", "l": "lima", "m": "mike", "n": "november",
		"o": "oscar", "p": "papa", "q": "quebec", "r": "romeo", "s": "sierra", "t": "tango", "u": "uniform", "v": "victor", "w": "whiskey", "x": "xray", "y": "yankee", "z": "zulu", "A": "Alfa",
		"B": "Bravo", "C": "Charlie", "D": "Delta", "E": "Echo", "F": "Foxtrot", "G": "Golf", "H": "Hotel", "I": "India", "J": "Juliett", "K": "Kilo", "L": "Lima", "M": "Mike", "N": "November",
		"O": "Oscar", "P": "Papa", "Q": "Quebec", "R": "Romeo", "S": "Sierra", "T": "Tango", "U": "Uniform", "V": "Victor", "W": "Whiskey", "X": "Xray", "Y": "Yankee", "Z": "Zulu"
	}
	outkey = {
		"alfa": "a", "bravo": "b", "charlie": "c", "delta": "d", "echo": "e", "foxtrot": "f", "golf": "g", "hotel": "h", "india": "i", "juliett": "j", "kilo": "k", "lima": "l", "mike": "m", "november": "n",
		"oscar": "o", "papa": "p", "quebec": "q", "romeo": "r", "sierra": "s", "tango": "t", "uniform": "u", "victor": "v", "whiskey": "w", "xray": "x", "yankee": "y", "zulu": "z", "Alfa": "A",
		"Bravo": "B", "Charlie": "C", "Delta": "D", "Echo": "E", "Foxtrot": "F", "Golf": "G", "Hotel": "H", "India": "I", "Juliett": "J", "Kilo": "K", "Lima": "L", "Mike": "M", "November": "N",
		"Oscar": "O", "Papa": "P", "Quebec": "Q", "Romeo": "R", "Sierra": "S", "Tango": "T", "Uniform": "U", "Victor": "V", "Whiskey": "W", "Xray": "X", "Yankee": "Y", "Zulu": "Z"
	}
	output = ""
	if encode:
		for char in text:
			if char in inkey:
				output += f"{inkey[char]} "
			else:
				output += f"{char} "
		return output[:-1], steps
	else:
		for char in text.split():
			if char in outkey:
				output += f"{outkey[char]}"
			else:
				output += f"{char}"
		return output, steps


def braille(text, encode=True, steps=0):		# No space + Uppercase + no steps
	inkey = {
		"a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑", "f": "⠋", "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚", "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕", "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎",
		"t": "⠞", "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽", "z": "⠵", "0": "⠼⠚", "1": "⠼⠁", "2": "⠼⠃", "3": "⠼⠉", "4": "⠼⠙", "5": "⠼⠑", "6": "⠼⠋", "7": "⠼⠛", "8": "⠼⠓", "9": "⠼⠊",
	}
	outkey = {
		"⠁": "a", "⠃": "b", "⠉": "c", "⠙": "d", "⠑": "e", "⠋": "f", "⠛": "g", "⠓": "h", "⠊": "i", "⠚": "j", "⠅": "k", "⠇": "l", "⠍": "m", "⠝": "n", "⠕": "o", "⠏": "p", "⠟": "q", "⠗": "r", "⠎": "s",
		"⠞": "t", "⠥": "u", "⠧": "v", "⠺": "w", "⠭": "x", "⠽": "y", "⠵": "z", "⠼⠚": "0", "⠼⠁": "1", "⠼⠃": "2", "⠼⠉": "3", "⠼⠙": "4", "⠼⠑": "5", "⠼⠋": "6", "⠼⠛": "7", "⠼⠓": "8", "⠼⠊": "9",
	}
	output = ""
	if encode:
		for char in text:
			if char in inkey:
				output += f"{inkey[char]} "
			else:
				output += f"{char} "
		return output[:-1], steps
	else:
		for char in text.split():
			if char in outkey:
				output += f"{outkey[char]}"
			else:
				output += f"{char}"
		return output, steps


def bacon(text, encode=True, steps=0):		# No space + no steps
	inkey = {
		"a": "aaaaa", "b": "aaaab", "c": "aaaba", "d": "aaabb", "e": "aabaa", "f": "aabab", "g": "aabba", "h": "aabbb", "i": "abaaa", "j": "abaab", "k": "ababa", "l": "ababb", "m": "abbaa", "n": "abbab",
		"o": "abbba", "p": "abbbb", "q": "baaaa", "r": "baaab", "s": "baaba", "t": "baabb", "u": "babaa", "v": "babab", "w": "babba", "x": "babbb", "y": "bbaaa", "z": "bbaab", "A": "AAAAA", "B": "AAAAB",
		"C": "AAABA", "D": "AAABB", "E": "AABAA", "F": "AABAB", "G": "AABBA", "H": "AABBB", "I": "ABAAA", "J": "ABAAB", "K": "ABABA", "L": "ABABB", "M": "ABBAA", "N": "ABBAB", "O": "ABBBA", "P": "ABBBB",
		"Q": "BAAAA", "R": "BAAAB", "S": "BAABA", "T": "BAABB", "U": "BABAA", "V": "BABAB", "W": "BABBA", "X": "BABBB", "Y": "BBAAA", "Z": "BBAAB"
	}
	outkey = {
		"aaaaa": "a", "aaaab": "b", "aaaba": "c", "aaabb": "d", "aabaa": "e", "aabab": "f", "aabba": "g", "aabbb": "h", "abaaa": "i", "abaab": "j", "ababa": "k", "ababb": "l", "abbaa": "m", "abbab": "n",
		"abbba": "o", "abbbb": "p", "baaaa": "q", "baaab": "r", "baaba": "s", "baabb": "t", "babaa": "u", "babab": "v", "babba": "w", "babbb": "x", "bbaaa": "y", "bbaab": "z", "AAAAA": "A", "AAAAB": "B",
		"AAABA": "C", "AAABB": "D", "AABAA": "E", "AABAB": "F", "AABBA": "G", "AABBB": "H", "ABAAA": "I", "ABAAB": "J", "ABABA": "K", "ABABB": "L", "ABBAA": "M", "ABBAB": "N", "ABBBA": "O", "ABBBB": "P",
		"BAAAA": "Q", "BAAAB": "R", "BAABA": "S", "BAABB": "T", "BABAA": "U", "BABAB": "V", "BABBA": "W", "BABBB": "X", "BBAAA": "Y", "BBAAB": "Z" 
	}
	output = ""
	if encode:
		for char in text:
			if char in inkey:
				output += f"{inkey[char]} "
			else:
				output += f"{char} "
		return output[:-1], steps
	else:
		for char in text.split():
			if char in outkey:
				output += f"{outkey[char]}"
			else:
				output += f"{char}"
		return output, steps


def morse(text, encode=True, steps=0):		# No space + Uppercase + no steps
	inkey = {
		"a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.", "g": "--.", "h": "....", "i": "..", "j": ".---", "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---", "p": ".--.",
		"q": "--.-", "r": ".-.", "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-", "y": "-.--", "z": "--..", "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
		"5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.", ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.", "!": "-.-.--", "/": "-..-.", "(": "-.--.", ")": "-.--.-",
		"&": ".-...", ":": "---...", ";": "-.-.-.", "=": "-...-", "+": ".-.-.", "-": "-....-", "_": "..--.-", '"': ".-..-.", "$": "...-..-", "@": ".--.-."
	}
	outkey = {
		".-": "a", "-...": "b", "-.-.": "c", "-..": "d", ".": "e", "..-.": "f", "--.": "g", "....": "h", "..": "i", ".---": "j", "-.-": "k", ".-..": "l", "--": "m", "-.": "n", "---": "o", ".--.": "p",
		"--.-": "q", ".-.": "r", "...": "s", "-": "t", "..-": "u", "...-": "v", ".--": "w", "-..-": "x", "-.--": "y", "--..": "z", "-----": "0", ".----": "1", "..---": "2", "...--": "3", "....-": "4",
		".....": "5", "-....": "6", "--...": "7", "---..": "8", "----.": "9", ".-.-.-": ".", "--..--": ",", "..--..": "?", ".----.": "'", "-.-.--": "!", "-..-.": "/", "-.--.": "(", "-.--.-": ")",
		".-...": "&", "---...": ":", "-.-.-.": ";", "-...-": "=", ".-.-.": "+", "-....-": "-", "..--.-": "_", ".-..-.": '"', "...-..-": "$", ".--.-.": "@", " ": ""
	}
	output = ""
	if encode:
		for char in text:
			if char in inkey:
				output += f"{inkey[char]} "
			else:
				output += f"{char} "
		return output[:-1], steps
	else:
		for char in text.split():
			if char in outkey:
				output += f"{outkey[char]}"
			else:
				output += f"{char}"
		return output, steps


def a1z26(text, encode=True, steps=0):		# No space + number support + Uppercase + no steps
	inkey = {
		"a": "1", "b": "2", "c": "3", "d": "4", "e": "5", "f": "6", "g": "7", "h": "8", "i": "9", "j": "10", "k": "11", "l": "12", "m": "13", "n": "14", "o": "15", "p": "16", "q": "17", "r": "18",
		"s": "19", "t": "20", "u": "21", "v": "22", "w": "23", "x": "24", "y": "25", "z": "26"
	}
	outkey = {
		"1": "a", "2": "b", "3": "c", "4": "d", "5": "e", "6": "f", "7": "g", "8": "h", "9": "i", "10": "j", "11": "k", "12": "l", "13": "m", "14": "n", "15": "o", "16": "p", "17": "q", "18": "r",
		"19": "s", "20": "t", "21": "u", "22": "v", "23": "w", "24": "x", "25": "y", "26": "z"
	}
	output = ""

	if encode:
		for char in text:
			if char in inkey:
				output += f"{inkey[char]} "
			else:
				output += f"{char} "
		return output[:-1], steps
	else:
		for char in text.split():
			if char in outkey:
				output += f"{outkey[char]}"
			else:
				output += f"{char}"
		return output, steps


def hashes(text, encode=True, steps=0):		# no decode + no steps
	hashtype = random.choice(["md5", "sha1", "sha224", "sha256", "sha384", "sha512", "blake2b", "blake2s"])

	if hashtype == "md5":
		text = hashlib.md5(text)
	elif hashtype == "sha1":
		text = hashlib.sha1(text)
	elif hashtype == "sha224":
		text = hashlib.sha224(text)
	elif hashtype == "sha256":
		text = hashlib.sha256(text)
	elif hashtype == "sha384":
		text = hashlib.sha384(text)
	elif hashtype == "sha512":
		text = hashlib.sha512(text)
	elif hashtype == "blake2b":
		text = hashlib.blake2b(text)
	elif hashtype == "blake2s":
		text = hashlib.blake2s(text)

	return text.hexdigest(), steps


if __name__ == '__main__':
	pass
