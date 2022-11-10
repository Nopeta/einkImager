#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import paho.mqtt.client as mqtt
import struct
import os

import logging
import time
from PIL import Image, ImageDraw, ImageFont
from img2bytearray import convert_to_bytearray
path = os.path.dirname(__file__) + '/'
logging.basicConfig(level=logging.DEBUG)

client = mqtt.Client()
client.username_pw_set('app', 'dev')
client.connect('192.168.168.173', 1883, 60)

client.loop_start()

try:
    logging.info("epd1in54_V2 Demo")

    # Drawing on the image
    logging.info("1.Drawing on the image...")
    image = Image.new('1', (200, 200), 255)  # 255: clear the frame

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(path + 'Font.ttc', 24)
    font18 = ImageFont.truetype(path + 'Font.ttc', 18)
    font16 = ImageFont.truetype(path + 'Font.ttc', 16)
    # HEAD
    # draw.rectangle((0, 0, 50, 24), fill=0)
    draw.rounded_rectangle((0, 0, 53, 24), 3, fill=0)
    draw.text((3, 2), '11/07', font=font18, fill=255)
    draw.text((80, 0), '預約列表', font=font, fill=0)

    currentTime = 0

    # BODY
    data = [
        {"start": 10, "end": 11, "title": "鄭○文"},
        {"start": 12, "end": 13, "title": "林○宏"},
        {"start": 13, "end": 15, "title": "陳○良"},
        {"start": 15, "end": 16, "title": "楊○緯"},
        {"start": 17, "end": 18, "title": "李○恩"},
        {"start": 19, "end": 21, "title": "王○龍"}
    ]

    y = 32
    x = 56

    for item in data:
        current = currentTime >= item['start'] and currentTime < item['end']
        draw.polygon([(100, y), (100, y+24), (110, y+24)], fill=0)
        draw.rectangle((0, y, 100, y+24), fill=0 if not current else 255)
        draw.text((7, y+4), f"{item['start']}:00~{item['end']}:00",
                  font=font16, fill=255 if not current else 0)
        draw.text((120, y-2), item['title'], font=font, fill=0)
        draw.line((190, x, 36, x), fill=0)
        y += 28
        x += 28

    # draw.rectangle((0, 28, 90, 52), fill = 0)
    # draw.text((2, 32), '10:00~11:00', font = font16, fill = 255)
    # draw.text((100, 28), '鄭○○', font = font, fill = 0)

    # draw.rectangle((0, 56, 90, 80), fill = 0)
    # draw.text((2, 60), '13:00~15:00', font = font16, fill = 255)
    # draw.text((100, 56), '鄭○○', font = font, fill = 0)

    # draw.rectangle((0, 84, 90, 108), fill = 0)
    # draw.text((2, 88), '15:00~16:00', font = font16, fill = 255)
    # draw.text((100, 84), '鄭○○', font = font, fill = 0)

    client.publish(
        'eink/image', bytearray(convert_to_bytearray(image, 200, 200)), qos=2)
    time.sleep(2)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
