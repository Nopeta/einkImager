#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import paho.mqtt.client as mqtt
import struct
import os
import logging
import time
import json
from PIL import Image, ImageDraw, ImageFont
from img2bytearray import convert_to_bytearray
path = os.path.dirname(__file__) + '/'

logging.basicConfig(level=logging.DEBUG)

with open(path+'/config.json') as fs:
    config = json.loads(fs.read())
client = mqtt.Client()
client.username_pw_set(config['mqtt']['username'], config['mqtt']['password'])
client.connect(config['mqtt']['host'], config['mqtt']['port'], 60)

client.loop_start()

try:
    logging.info("epd1in54_V2 Demo")

    # Drawing on the image
    logging.info("1.Drawing on the image...")
    image = Image.new('1', (200, 200), 255)  # 255: clear the frame

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(path + 'Font.ttc', 24)
    font20 = ImageFont.truetype(path + 'Font.ttc', 20)
    font18 = ImageFont.truetype(path + 'Font.ttc', 18)
    font16 = ImageFont.truetype(path + 'Font.ttc', 16)
    font10 = ImageFont.truetype(path + 'Font.ttc', 10)
    fontEmoji = ImageFont.truetype(path + 'Emoji.ttf', 14)

    dTime = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    date = [
        {"week": "Mon.", "day": 7},
        {"week": "Tue.", "day": 8},
        {"week": "Wed.", "day": 9},
        {"week": "Thu.", "day": 10},
        {"week": "Fri.", "day": 11},
        {"week": "Sat.", "day": 12},
        {"week": "Sun.", "day": 13},
    ]
    data = [
        {"start": 10, "end": 11, "title": "鄭○文"},
        {"start": 12, "end": 13, "title": "林○宏"},
        {"start": 13, "end": 15, "title": "陳○良"},
        {"start": 15, "end": 16, "title": "楊○緯"},
        {"start": 17, "end": 18, "title": "李○恩"},
        {"start": 19, "end": 21, "title": "王○龍"}
    ]

    # HEAD
    draw.text((2, 0), 'Nov.', font=font20, fill=0)
    draw.text((80, 0), '預約顯示', font=font20, fill=0)

    # BODY
    x = 0
    xLine = 0
    y = 0
    for item in date:
        draw.text((x+20, 22),  item['week'], font=font16, fill=0)
        draw.text((x+54, 22),  f"{item['day']}", font=font16, fill=0)
        draw.line((xLine+67, 35, xLine+67, 200), fill=0)
        x += 57.5
        xLine += 60

    for item in dTime:
        draw.text((2, y+37),  f"{item}", font=font10, fill=0)
        draw.line((14, y+43, 200, y+43), fill=0)
        y += 20

    draw.rounded_rectangle((15, 45, 65, 81), 3, fill=0)
    draw.text((31, 47), '預', font=font18, fill=255)
    draw.text((28, 67), '10~12', font=font10, fill=255)

    # draw.text((32, 67), "✍🏻", font=fontEmoji, fill=255)

    # y = 32

    # for item in data:
    #     draw.rectangle((0, y, 100, y+24), fill = 0)
    #     draw.text((7, y+4), f"{item['time']}:00~{item['time']+item['hour']}:00", font = font16, fill = 255)
    #     draw.text((110, y-2), item['title'], font = font, fill = 0)
    #     y += 28

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
