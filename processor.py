from PIL import Image

def build_cipher(message):
    cipher_key = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    message_binary = []
    if message: # 6 bit per karakter (max 64 karakter untuk 6 bit) daripada ascii itu 8 bit bisa dibagi 3
        for i in message:
            apalah_binary = cipher_key.index(i)
            apalah_binary = format(apalah_binary, '06b')
            message_binary.append(apalah_binary)
        print(message_binary)

def process(path):
	img = Image.open(path).convert('RGB')
	x, y = img.size

	pixel_map = img.load()
 
	for i in range(0, y):
		for j in range(0, x):
			plaintext = img.getpixel((j,i))
			r, g, b = img.getpixel((j,i))
			print("Plaintext: ", plaintext)

			r_bin = format(r, '08b')
			g_bin = format(g, '08b')
			b_bin = format(b, '08b')
			print("R: ", r_bin)
			print("G: ", g_bin)
			print("B: ", b_bin)

			g_bin = g_bin[:-1] + '1'
			b_bin = b_bin[:-1] + '1'

			r = int(r_bin, 2)
			g = int(g_bin, 2)
			b = int(b_bin, 2)

			pixel_map[j,i] = (int(r), int(g), int(b+1))
			img.save("output/ciphertext.png", format="png")

			img = Image.open("output/ciphertext.png").convert("RGB")
			ciphertext = img.getpixel((j,i))
			print("Ciphertext: ", ciphertext)
			r, g, b = img.getpixel((j,i))
			r_bin = format(r, '08b')
			g_bin = format(g, '08b')
			b_bin = format(b, '08b')
			print("R: ", r_bin)
			print("G: ", g_bin)
			print("B: ", b_bin)