#!/usr/bin/python
# -*- coding:utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from img2bytearray import convert_to_bytearray
import openpyxl
import paho.mqtt.client as mqtt
import os
import logging
import time
import datetime
import json

path = os.path.dirname(__file__) + '/'
wb = openpyxl.load_workbook(path + 'data_test.xlsx')
today = datetime.datetime.today().strftime('%m/%d')
year = datetime.datetime.today().strftime('%Y')
s1 = wb[year]
# s1 = wb.active


def get_values(sheet):
    arr = []                      # 第一層串列
    for row in sheet:
        arr2 = []                # 第二層串列
        if row[0].value == 'date':
            continue
        else:
            # if row[0].value.strftime('%m/%d') == today:
            if row[0].value.strftime('%m/%d') == '11/15':
                for column in row:
                    arr2.append(column.value)  # 寫入內容
                obj = {"date": arr2[0].strftime('%m/%d'), "start": arr2[1].strftime('%H:%M'),
                       "end": arr2[2].strftime('%H:%M'), "name": arr2[3], "use": arr2[4]}
                arr.append(obj)
            else:
                continue
    return arr


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
    font18 = ImageFont.truetype(path + 'Font.ttc', 18)
    font16 = ImageFont.truetype(path + 'Font.ttc', 16)
    fontEmoji = ImageFont.truetype(path + 'Emoji.ttf', 72)

    data = get_values(s1)

    # HEAD
    draw.rounded_rectangle((0, 0, 53, 24), 3, fill=0)
    draw.text((3, 2), today, font=font18, fill=255)
    draw.text((80, 0), '預約列表', font=font, fill=0)

    currentTime = 17

    # BODY
    # data = [
    #     {"start": 10, "end": 11, "title": "鄭○文"},
    #     {"start": 12, "end": 13, "title": "林○宏"},
    #     {"start": 13, "end": 15, "title": "陳○良"},
    #     {"start": 15, "end": 16, "title": "楊○緯"},
    #     {"start": 17, "end": 18, "title": "李○恩"},
    #     {"start": 19, "end": 21, "title": "王○龍"}
    # ]

    y = 32
    x = 56
    if len(data) == 0:
        draw.text((55, 60), "⏰", font=fontEmoji, fill=0)
        draw.text((4, 150), '今日沒有任何預約', font=font, fill=0)
    else:
        for item in data:
            current = currentTime >= int(
                item['start'][0:2]) and currentTime < int(item['end'][0:2])
            draw.polygon([(100, y), (100, y+24), (110, y+24)],
                         fill=0 if not current else 255)
            draw.ellipse((0, y, 5, y+5), fill=0 if not current else 255)
            draw.rectangle((0+5/2, y, 100, y+24),
                           fill=0 if not current else 255 if not current else 255)
            draw.rectangle((0, y+5/2, 100, y+24),
                           fill=0 if not current else 255)
            draw.text((7, y+4), f"{item['start']}~{item['end']}",
                      font=font16, fill=255 if not current else 0)
            draw.text((120, y-2), item['name'], font=font, fill=0)
            draw.line((0, x, 200, x), fill=0)
            y += 28
            x += 28

    client.publish(
        'eink/image', bytearray(convert_to_bytearray(image, 200, 200)), qos=2)
    time.sleep(2)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
