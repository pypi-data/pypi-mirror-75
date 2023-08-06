#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'album_sender'

from PIL import Image
from telegram import InputMediaPhoto, InputMediaVideo
import cached_url
import pic_cut
from telegram_util import cutCaption, isUrl
import os
import time

def isAnimated(path):
	cached_url.get(path, force_cache=True, mode='b')
	gif = Image.open(cached_url.getFilePath(path))
	try:
		gif.seek(1)
	except EOFError:
		return False
	else:
		return True

def properSize(fn):
	size = os.stat(fn).st_size
	return 0 < size and size < (1 << 23)

def shouldSendAnimation(result):
	if not result.imgs:
		return False
	animated_imgs = [x for x in result.imgs if isAnimated(x)]
	non_animated_imgs = [x for x in result.imgs if not isAnimated(x)]
	if len(non_animated_imgs) > len(animated_imgs): # may need to revisit
		result.imgs = non_animated_imgs
		return False
	animated_imgs = [(os.stat(cached_url.getFilePath(x)).st_size, 
		x) for x in animated_imgs]
	animated_imgs.sort()
	result.imgs = [animated_imgs[-1][1]]
	return True

def getCap(result, limit):
	if result.url:
		suffix = '[source](%s)' % result.url
	else:
		suffix = ''
	return cutCaption(result.cap, suffix, limit)

def sendVideo(chat, result):
	os.system('mkdir tmp > /dev/null 2>&1')
	with open('tmp/video.mp4', 'wb') as f:
		f.write(cached_url.get(result.video, force_cache=True, mode='b'))
	if os.stat('tmp/video.mp4').st_size > 50 * 1024 * 1024:
		return []
	group = [InputMediaVideo(open('tmp/video.mp4', 'rb'), 
		caption=getCap(result, 1000), parse_mode='Markdown')]
	return chat.bot.send_media_group(chat.id, group, timeout = 20*60)

def imgRotate(img_path, rotate):
	if not rotate:
		return
	if rotate == True:
		rotate = 180
	img = Image.open(img_path)
	img = img.rotate(rotate, expand=True)
	img.save(img_path)

def send_v2(chat, result, rotate=0, send_all=False, time_sleep=0):
	if result.video:
		return sendVideo(chat, result)
		
	if shouldSendAnimation(result):
		return chat.bot.send_document(chat.id, 
			open(cached_url.getFilePath(result.imgs[0]), 'rb'), 
			caption=getCap(result, 1000), parse_mode='Markdown', 
			timeout=20*60)
		
	img_limit = 100 if send_all else 10
	imgs = pic_cut.getCutImages(result.imgs, img_limit)	
	imgs = [x for x in imgs if properSize(x)]
	[imgRotate(x, rotate) for x in imgs]
	if imgs:
		return_result = []
		for page in range(1 + int((len(imgs) - 1) / 10)):
			group = ([InputMediaPhoto(open(imgs[page * 10], 'rb'), 
				caption=getCap(result, 1000), parse_mode='Markdown')] + 
				[InputMediaPhoto(open(x, 'rb')) for x in 
					imgs[page * 10 + 1:page * 10 + 10]])
			if page != 0:
				time.sleep(time_sleep * len(group))
			return_result += chat.bot.send_media_group(chat.id, group, timeout = 20*60)
		return return_result

	if result.cap:
		return [chat.send_message(getCap(result, 4000), 
			parse_mode='Markdown', timeout = 20*60, 
			disable_web_page_preview = (not isUrl(result.cap)))]

def send(chat, url, result, rotate=0, send_all=False):
	result.url = url
	send_v2(chat, result, rotate=rotate, send_all=send_all)