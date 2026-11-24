from PIL import Image

x, y = 2,0
img = Image.open("input/photo.png").convert('RGB')

pixel_map = img.load()
plaintext = img.getpixel((x,y))
r, g, b = img.getpixel((x,y))
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

pixel_map[x,y] = (int(r), int(g), int(b+1))
img.save("output/ciphertext.png", format="png")

img = Image.open("output/ciphertext.png").convert("RGB")
ciphertext = img.getpixel((x,y))
print("Ciphertext: ", ciphertext)
r, g, b = img.getpixel((x,y))
r_bin = format(r, '08b')
g_bin = format(g, '08b')
b_bin = format(b, '08b')
print("R: ", r_bin)
print("G: ", g_bin)
print("B: ", b_bin)