import string
import random

# working punctuation
punc = "!#$%&()<=>?@[]}{~:;|*+-"
simple_passwords = [
	"password", "123456", "12345678", "1234", "qwerty", "12345", "dragon", "baseball", "football", "letmein", "monkey", "696969", "abc123", "mustang", "michael", "shadow", "master", "jennifer",
	"111111", "2000", "jordan", "superman", "harley", "1234567", "hunter", "trustno1", "ranger", "buster", "thomas", "tigger", "robert", "soccer", "batman", "test", "pass",
	"killer", "hockey", "george", "charlie", "andrew", "michelle", "love", "sunshine", "jessica", "asshole", "6969", "pepper", "daniel", "access", "123456789", "654321", "joshua", "maggie", "starwars",
	"silver", "william", "dallas", "yankees", "123123", "ashley", "666666", "hello", "amanda", "orange", "biteme", "freedom", "computer", "thunder", "nicole", "ginger", "heather", "hammer",
	"summer", "corvette", "taylor", "austin", "1111", "merlin", "matthew", "121212", "golfer", "cheese", "princess", "martin", "chelsea", "patrick", "richard", "diamond", "yellow", "bigdog",
	"secret", "asdfgh", "sparky", "cowboy"
]


def passgen(cipher_type, cipher, func):
	if cipher_type == "text_full":
		chars = string.ascii_letters + string.digits + punc
		length = random.randint(16, 50)
	elif cipher_type == "text_full_lowercase":
		chars = string.ascii_lowercase + string.digits + punc
		length = random.randint(16, 50)
	elif cipher_type == "lowercase_punc":
		chars = string.ascii_lowercase + punc
		length = random.randint(16, 50)
	elif cipher_type == "image_hexahue":
		chars = string.ascii_lowercase + string.digits + " ,."
		length = random.randint(16, 50)
	elif cipher_type == "hashes":
		chars = simple_passwords
		length = 1
	elif cipher_type == "audio_nato":
		chars = string.ascii_letters + string.digits + punc
		length = random.randint(10, 25)
	elif cipher_type == "audio_morse":
		chars = string.ascii_lowercase + string.digits
		length = random.randint(10, 25)

	password = "".join(random.choices(chars, k=length))
	if cipher_type != "hashes":
		password = f"password{password}password"
		ciphered, steps = func(password)
	else:
		ciphered, steps = func(password.encode('utf-8'))
		ciphered = f"hash:{ciphered}:hash"
		password = f"hash:{password}:hash"

	return ciphered, password.encode("utf-8"), steps


if __name__ == '__main__':
	passgen("hashes", "", "")
