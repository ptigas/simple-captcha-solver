from PIL import Image

def ocr(im, threshold = 200, aplhabet = "0123456789abcdef"):
	img = Image.open(im)
	img = img.convert("RGB")
	box = (8, 8, 58, 18)
	img = img.crop(box)
	pixdata = img.load()

	letters = Image.open('letters.bmp')
	ledata = letters.load()

	def test_letter(img, letter):
		A = img.load()
		B = letter.load()
		mx = 1000000
		max_x = 0
		x = 0
		for x in xrange(img.size[0]-letter.size[0]):
			sum = 0
			for i in xrange(letter.size[0]):
			    for j in xrange(letter.size[1]):
					sum = sum + abs(A[x+i, j][0] - B[i, j][0])
			if sum < mx :
				mx = sum
				max_x = x
		return (mx, max_x)
	
	# Clean the background noise, if color != black, then set to white.
	for y in xrange(img.size[1]):
	    for x in xrange(img.size[0]):
			if not(pixdata[x, y][0] > threshold and pixdata[x, y][1] > threshold and pixdata[x, y][2] > threshold):
				pixdata[x, y] = (0, 0, 0, 255)
			else:
				pixdata[x, y] = (255, 255, 255, 255)

	counter = 0;
	old_x = -1;

	letterlist = []

	for x in xrange(letters.size[0]):
		black = True
		for y in xrange(letters.size[1]):
			if ledata[x, y][0] <> 0 :
				black = False
				break
		if black :
			if True :
				box = (old_x+1, 0, x, 10)
				letter = letters.crop(box)
				t = test_letter(img, letter);
				letterlist.append((t[0],aplhabet[counter], t[1]))
			old_x = x
			counter = counter + 1
		
	box = (old_x+1, 0, 140, 10)
	letter = letters.crop(box)
	t = test_letter(img, letter)
	letterlist.append((t[0],aplhabet[counter], t[1]))

	t = sorted(letterlist)
	t = t[0:5] # 5-letter captcha

	final = sorted(t, key=lambda x: x[2])
	answer = ""
	for l in final:
		answer = answer + l[1]
	return answer

print ocr('test.jpg')