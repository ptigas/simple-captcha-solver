This is a very simple method for exploiting very simple CAPTCHAs  like those proposed [here](http://www.white-hat-web-design.co.uk/articles/php-captcha.php) and [here](http://www.white-hat-web-design.co.uk/articles/php-captcha.php) .

In this example we are going to use the following images.

![](http://ptigas.com/blog/wp-content/uploads/2011/02/test1.jpg "test") 

![](http://ptigas.com/blog/wp-content/uploads/2011/02/test2.jpg "test2")


It&#8217;s easy to observe the followings. First of all, a fixed size (monospace) font has been used. This makes extracting all the letters and using them as masks to check each digit, one by one, very easy. Also, the alphabet is simple lowercase hexadecimal letters. Thus, we had to extract only 16 letters.

The first part was to to extract all the letters. To achieve that, first of all we sampled several images so as to be sure that the images we have contains all the 16 letters. Then, using a simple image editor we cropped all the letters, one by one. We had to be careful so all the letters be aligned properly. Here is the final mask.

![](http://ptigas.com/blog/wp-content/uploads/2011/02/letters.bmp "letters")

As you can notice there is some noise which we have to remove. After playing with several techniques we finally ended to the following. We turned the image to greyscale. Then we used a threshold to remove some of the noise. Here is the example after the filtering (cropping also applied).

![](http://ptigas.com/blog/wp-content/uploads/2011/02/source.bmp "source")

So, now we have the image almost cleared and some letters to play with.

## Procedure

Move each letter across the image and take the difference of the pixels for each position and sum them. Thus for each position we have a score of how much the letter (mask) fits the letter behind it. Then, store for each letter the position where the maximum score found. Then sort by score, take the top five results (our captcha is five letters) and finally sort by position. The result is the CAPTCHA text.

<pre data-language="python">def p(img, letter):
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
            if sum &lt; mx :
                mx = sum
                max_x = x
        return (mx, max_x)</pre>

Here is the code which implements this method. You can browse and download everything from [https://github.com/ptigas/simple-CAPTCHA-solver](https://github.com/ptigas/simple-CAPTCHA-solver)

<pre data-language="python">from PIL import Image

def ocr(im, threshold = 200, aplhabet = "0123456789abcdef"):
    img = Image.open(im)
    img = img.convert("RGB")
    box = (8, 8, 58, 18)
    img = img.crop(box)
    pixdata = img.load()

    letters = Image.open('letters.bmp')
    ledata = letters.load()

    # Clean the background noise, if color != black, then set to white.
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if not(pixdata[x, y][0] &gt; threshold \
            and pixdata[x, y][1] &gt; threshold \
            and pixdata[x, y][2] &gt; threshold):
                pixdata[x, y] = (0, 0, 0, 255)
            else:
                pixdata[x, y] = (255, 255, 255, 255)

    counter = 0;
    old_x = -1;

    letterlist = []

    for x in xrange(letters.size[0]):
        black = True
        for y in xrange(letters.size[1]):
            if ledata[x, y][0] &lt;&gt; 0 :
                black = False
                break
        if black :
            if True :
                box = (old_x+1, 0, x, 10)
                letter = letters.crop(box)
                t = p(img, letter);
                print counter, x, t
                letterlist.append((t[0],aplhabet[counter], t[1]))
            old_x = x
            counter = counter + 1

    box = (old_x+1, 0, 140, 10)
    letter = letters.crop(box)
    t = p(img, letter)
    letterlist.append((t[0],aplhabet[counter], t[1]))

    t = sorted(letterlist)
    t = t[0:5] # 5-letter captcha

    final = sorted(t, key=lambda x: x[2])
    answer = ""
    for l in final:
        answer = answer + l[1]
    return answer

print ocr('test.jpg')</pre>

p.s. I found [this](http://www.wausita.com/captcha/). Very nice tutorial for CAPTCHA solving using python and vector space searching.