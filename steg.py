russianLetters = "КАМОНВЕРХСТрохуаес"
englishLetters = "KAMOHBEPXCTpoxyaec"

def encrypt(toEncodeName, key):
	toEncodeFile = open(toEncodeName + '.txt', 'r')
	encrypted = open('encrypted.txt', 'w')

	while True:
		symbolFromEncode = toEncodeFile.read(1)

		if not symbolFromEncode:
			break

		symbolFromEncode = (ord(symbolFromEncode) + key) % 128

		encrypted.write(chr(symbolFromEncode))

	toEncodeFile.close()
	encrypted.close()

def encode(toEncodeName, textName):
	toEncodeFile = open(toEncodeName + '.txt', 'r')
	textFile = open(textName + '.txt', 'r')
	encoded = open('encoded.txt', 'w')

	letterToEncode = 0	#буква, которую надо считать с файла toEncode
	encodedBits = 8

	while True:
		symbolFromText = textFile.read(1)

		if not symbolFromText:
			break

		if symbolFromText in englishLetters:
			if encodedBits == 8:
				letterToEncode = toEncodeFile.read(1)

				if not letterToEncode:
					encoded.write(symbolFromText)
					break

				print("To encode {0} = {1:b} = {1}".format(letterToEncode, ord(letterToEncode)))
				letterToEncode = ord(letterToEncode)
				encodedBits = 0

			bitFromLetter = (letterToEncode & 0b10000000) >> 7

			print("Read {0}, bit {1}".format(symbolFromText, bitFromLetter))

			if bitFromLetter:
				symbolFromText = russianLetters[englishLetters.index(symbolFromText)]

			letterToEncode <<= 1

			letterToEncode %= 256
			encodedBits += 1

		encoded.write(symbolFromText)

	# encoded.write(textFile.read())
			
	toEncodeFile.close()
	textFile.close()
	encoded.close()

def decode(encodedName, toRead):
	encoded = open(encodedName + '.txt', 'r')
	decoded = open('decoded.txt', 'w')

	read = 0
	bitsRead = 0
	byte = 0

	while read < toRead:
		symbol = encoded.read(1)
		if not symbol:
			break

		if symbol in englishLetters:
			byte <<= 1
			bitsRead += 1
			print("Symbol {0}, bit 0, byte {1:b}".format(symbol, byte))
		elif symbol in russianLetters:
			byte <<= 1
			byte |= 1
			bitsRead += 1
			print("Symbol {0}, bit 0, byte {1:b}".format(symbol, byte))

		if bitsRead == 8:
			print("{0}, {0:b}, {0:c}".format(byte))
			decoded.write(chr(byte))
			read += 1
			bitsRead = byte = 0

	encoded.close()
	decoded.close()

def decrypt(decoded, key):
	decodedFile = open(decoded + '.txt', 'r')
	decodedAndDecryptedFile = open('decodedAndDecrypted.txt', 'w')

	while True:
		symbolFromDecoded = decodedFile.read(1)

		if not symbolFromDecoded:
			break

		symbolFromDecoded = chr((ord(symbolFromDecoded) - key) % 128)

		decodedAndDecryptedFile.write(symbolFromDecoded)

	decodedFile.close()
	decodedAndDecryptedFile.close()

def start():
	while True:
		choice = int(input("Enter number (1 - encode; 2 - decode; 3 - quit): "))

		if choice is 1:
			toEncodeName = input("Enter name of file with secret message: ")
			textName = input("Enter name of file container: ")

			key = int(input("Enter the key for encryption: "))

			encrypt(toEncodeName, key)
			encode("encrypted", textName)

			print("Your message has encrypted and encoded")
		elif choice is 2:
			keyForDecode = int(input("How long is encoded message: "))

			keyForDecrypt = int(input("What was the key for encryption: "))

			decode("encoded", keyForDecode)
			decrypt("decoded", keyForDecrypt)

			print("Your message has decoded and decrypted")
		elif choice is 3:
			break
		else:
			print("Uknown command")

start()