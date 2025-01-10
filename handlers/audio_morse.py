from pydub import AudioSegment
import wave
import struct
from tempfile import TemporaryFile
from io import BytesIO

# adapted from https://github.com/jvmeifert/morseaudiosuite + my nato tts


# my settings
path = "./audio/morse"
files = {".": "dot", "-": "dash", "_": "underscore"}

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
	".-...": "&", "---...": ":", "-.-.-.": ";", "-...-": "=", ".-.-.": "+", "-....-": "-", "..--.-": "_", ".-..-.": '"', "...-..-": "$", ".--.-.": "@", " ": "/"
}

# settings from original (complicated dont change)
UNIT_TIME = 2400
AMPLITUDE_LOGIC_THRESHOLD = 13000
START_DECODE_OFFSET = -8


# Decide if a certain deviation is considered logically ON or OFF.
def logicalDecode(deviation):
	if (deviation > AMPLITUDE_LOGIC_THRESHOLD):
		return 1
	else:
		return 0


# Find the average absolute deviation of the amplitude of a chunk of audio.
def avgAbsDeviation(chunk):
	totFrames = 0
	for frame in chunk:
		totFrames += abs(frame)
	return totFrames / len(chunk)


# Find the start of the morse code data in a stream by detecting the first logical ON
# Make sure your squelch is ON to prevent noise from tripping this block.
def findStart(chunk):
	iterIndex = 0
	while (abs(chunk[iterIndex]) < AMPLITUDE_LOGIC_THRESHOLD):
		iterIndex += 1
	iterIndex += START_DECODE_OFFSET
	if (iterIndex < 0):
		iterIndex = 0
	return iterIndex


# Get raw morse data from a wav file - the heart of the program
# Splits a file into its individual frames, arranges them into chunks,
# analyzes the average absolute deviation of each chunk, and outputs
# the resulting digital data.
def getMorseData(filename):
	with wave.open(filename, "r") as f:
		nFrames = f.getnframes()
		expFrames = []
		chunkDevs = []
		decodedChunks = []

		# Unpack the frames of the input .wav file
		for i in range(0, nFrames):
			sFrame = f.readframes(1)
			expFrames.append(struct.unpack("<h", sFrame)[0])

		# Find the start of the morse data
		startSample = findStart(expFrames)

		# Split wav data into chunks and analyze the avg. abs. deviation of each chunk
		chunkIter = startSample + UNIT_TIME
		while (chunkIter < nFrames - int(UNIT_TIME - 1)):
			chunk = expFrames[int(chunkIter - UNIT_TIME):int(chunkIter)]
			chunkDevs.append(int(avgAbsDeviation(chunk)))
			chunkIter += UNIT_TIME

		# Get logic zeros or ones from average abs. deviation
		for i in chunkDevs:
			decodedChunks.append(logicalDecode(i))
		return decodedChunks


# Convert raw morse data into human readable dits, dahs, and slashes.
# International morse defines a dit as one time unit and a dah as three time units.
# It also defines the space between characters as three units of silence, and the
# space between words as seven units of silence.
def getHumanReadableMorse(morseData):
	humanMorse = ""
	morseIter = 0
	streak0 = 0
	streak1 = 0
	while (morseIter < len(morseData)):		# Iterate over each item and determine if it is the start, end, or part of a character.
		if (morseData[morseIter] == 1):
			if (streak0 > 6):
				humanMorse += "/"		# 7 zeroes in a row means a space.
				streak0 = 0
				streak1 = 0
			elif (streak0 > 2):		# 3 zeroes in a row means a new character.
				humanMorse += ","
				streak0 = 0
				streak1 = 0
			else:
				streak0 = 0
			streak1 += 1
		else:
			if (streak1 > 2):
				humanMorse += "-"		# 3 ones in a row means a dah.
				streak1 = 0
				streak0 = 0
			elif (streak1 > 0):
				humanMorse += "."		# 1 one means a dit.
				streak1 = 0
				streak0 = 0
			else:
				streak1 = 0
			streak0 += 1
		morseIter += 1
	return humanMorse


# Decode human readable morse into letters, numbers, and spaces.
def decodeHumanReadableMorse(message):
	words = message.split("/")
	letters = []
	for word in words:
		letters.append(word.split(","))
	mc = ""
	for letter in letters:
		for code in letter:
			try:
				mc += outkey[code]
			except KeyError:
				mc += "?"
		mc += " "
	return (mc)


def morse_encode(text):
	encoded = ""
	# convert to text repersentation
	for char in text:
		if char in inkey:
			encoded += f"{inkey[char]} "
		else:
			print(char)
			raise Exception
	encoded = encoded[:-1]

	# convert to paths
	paths = []
	for char in encoded.split():
		for c in char:
			paths.append(f"{path}/{files[c]}.wav")
			paths.append(f"{path}/{files['_']}.wav")		# inter char space
		# inter letter space
		paths.append(f"{path}/{files['_']}.wav")
		paths.append(f"{path}/{files['_']}.wav")
		paths.append(f"{path}/{files['_']}.wav")

	# convert to audio
	output = AudioSegment.empty()
	for file in paths:
		new = AudioSegment.from_wav(file)
		output = output + new
	return output


def morse_decode(file):
	data = getMorseData(file)
	human_readable = getHumanReadableMorse(data)
	decoded = decodeHumanReadableMorse(human_readable)
	return decoded


def main(text, encode=True, steps=0):		# no space + no uppercase + no steps
	if encode:
		output = morse_encode(text)
	else:
		output = morse_decode(BytesIO(text))[:-1]
	return output, steps


if __name__ == '__main__':
	pass
