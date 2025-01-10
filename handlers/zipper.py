from tempfile import TemporaryFile
import pyzipper
import random
import string


# types
text = ["text_full", "text_full_lowercase", "lowercase_punc", "hashes"]
image = ["image_hexahue"]
wav = ["audio_nato", "audio_morse"]


# generate random file names
def file_names():
	chars = string.ascii_letters + string.digits
	return "".join(random.choices(chars, k=16))


# create zip, write the ciphered pw to it then enable encryption and write old file
def zipper(previous_file, ciphered_pw, password, tmpdir, cipher_type=""):
	new_file = f"{file_names()}.zip"
	with pyzipper.AESZipFile(f"{tmpdir}/{new_file}", "w", compression=pyzipper.ZIP_DEFLATED) as file:
		if cipher_type in text:
			file.writestr(f"{file_names()}.txt", ciphered_pw)
		elif cipher_type in image:
			with TemporaryFile() as temp:
				ciphered_pw.save(temp, "PNG")
				temp.seek(0)
				file.writestr(f"{file_names()}.png", temp.read())
		elif cipher_type in wav:
			with TemporaryFile() as temp:
				ciphered_pw.export(temp, format="wav")
				temp.seek(0)
				file.writestr(f"{file_names()}.wav", temp.read())
		else:
			print(f"Error none supported cipher_type\n{cipher_type}")
			raise Exception
		file.setencryption(pyzipper.WZ_AES)
		file.setpassword(password)
		file.write(f"{tmpdir}/{previous_file}", arcname=previous_file)

	return new_file


def dezipper(file, tmpdir, password=""):
	with pyzipper.AESZipFile(f"{tmpdir}/{file}", "r", compression=pyzipper.ZIP_DEFLATED) as file:
		files = file.namelist()

		if password != "":
			file.setencryption(pyzipper.WZ_AES)
			file.setpassword(password)
			file.extract(files[1], path=tmpdir)
			return files[1]
		else:
			return file.read(files[0])

	# return new_file


if __name__ == '__main__':
	pass
