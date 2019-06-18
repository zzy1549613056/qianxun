#!/usr/local/bin/python3

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

def get_captcha():

    L = ''
    # 随机字母:
    def rndChar():
        return chr(random.randint(65, 90) + random.randint(0, 1)*32)

    # 随机颜色1:
    def rndColor():
        return (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))

    # 随机颜色2:
    def rndColor2():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    # 240 x 60:
    width = 30 * 4
    height = 30
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('Arial.ttf', 20)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    #加噪点
    for x in range(width):
        for y in range(height):
            flag = random.randint(1,10)
            if flag == 10:
                draw.point((x, y), fill=rndColor2())
    # 输出文字:
    for t in range(4):
        rndchr = rndChar()
        draw.text((30 * t + 5, 5), rndchr, font=font, fill=rndColor2())
        L = L + rndchr

    for _ in range(2):
        begin = (random.randint(0,width),random.randint(0,height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin,end], fill=rndColor2(), width=2)
    # image = image.filter(ImageFilter.BLUR)
    return (L,image)

# 模糊:
# image = image.filter(ImageFilter.BLUR)
# image.save('验证码%s.jpg'%L, 'jpeg')
