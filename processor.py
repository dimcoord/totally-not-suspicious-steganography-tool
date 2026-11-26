from PIL import Image
import pandas as pd

cipher_key = [
    # 0-25: lowercase (26)
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    # 26-51: uppercase (26)
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    # 52-61: digits (10)
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    # 62-63: space + end-of-message marker (2) -> Total = 64
    " ", "\0"
]

def build_cipher(message):
    message_binary = []
    if message: # 6 bit per karakter (max 64 karakter untuk 6 bit) daripada ascii itu 8 bit bisa dibagi 3
        for i in message:
            apalah_binary = cipher_key.index(i)
            apalah_binary = format(apalah_binary, '06b')
            left_binary = apalah_binary[:3]
            right_binary = apalah_binary[3:]
            message_binary.append([left_binary, right_binary])
        print(message_binary)
    return message_binary

def extract(message_binary):
    message = ""
    lsb = ""
    if message_binary: # 6 bit per karakter (max 64 karakter untuk 6 bit) daripada ascii itu 8 bit bisa dibagi 3
        for i in message_binary:
            for j in i:
                for k in j:
                    lsb += k[-1]
        for i in range(0, len(lsb) - 5, 6):
            decoded = lsb[i:i+6]
            j = int(decoded, 2)
            if cipher_key[j] == "\0":
                break
            message += cipher_key[j]
        with open("output/decrypt.txt", "w") as file:
            file.write(message)

def build_csv(plaintext, ciphertext):
	plaintext_df = pd.DataFrame(plaintext)
	plaintext_df.to_csv("output/plaintext.csv", index=False)
	ciphertext_df = pd.DataFrame(ciphertext)
	ciphertext_df.to_csv("output/ciphertext.csv", index=False)

def process(path, message=[[]]):
	img = Image.open(path).convert('RGB')
	x, y = img.size

	pixel_map = img.load()
	plaintext_arr = [[[] for _ in range(x)] for _ in range(y)]
	message_length = len(message) * 2
	k = 0
	half = 0
 
	for i in range(0, y):
		for j in range(0, x):
			plaintext = img.getpixel((j,i))
			r, g, b = img.getpixel((j,i))
			# print("Plaintext: ", plaintext)

			r_bin = format(r, '08b')
			g_bin = format(g, '08b')
			b_bin = format(b, '08b')
			
			# print("R: ", r_bin)
			# print("G: ", g_bin)
			# print("B: ", b_bin)
   
			plaintext_arr[i][j].append(r_bin)
			plaintext_arr[i][j].append(g_bin)
			plaintext_arr[i][j].append(b_bin)
			   
			if k < len(message):
				r_bin = r_bin[:-1] + message[k][half][0]
				g_bin = g_bin[:-1] + message[k][half][1]
				b_bin = b_bin[:-1] + message[k][half][2]
				
				if half == 0:
					half = 1
				else:
					half = 0
					k += 1

			r = int(r_bin, 2)
			g = int(g_bin, 2)
			b = int(b_bin, 2)

			pixel_map[j,i] = (int(r), int(g), int(b))
	img.save("output/ciphertext.png", format="png")

	img = Image.open("output/ciphertext.png").convert("RGB")
	x, y = img.size
	
	pixel_map = img.load()
	ciphertext_arr = [[[] for _ in range(x)] for _ in range(y)]
	
	for i in range(0, y):
		for j in range(0, x):
			ciphertext = img.getpixel((j,i))
			# print("Ciphertext: ", ciphertext)
			r, g, b = img.getpixel((j,i))
			ciphertext_arr[i][j].append(format(r, '08b'))
			ciphertext_arr[i][j].append(format(g, '08b'))
			ciphertext_arr[i][j].append(format(b, '08b'))
   
	build_csv(plaintext_arr, ciphertext_arr)
	extract(ciphertext_arr)