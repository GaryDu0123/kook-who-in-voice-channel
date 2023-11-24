#!/usr/bin/env python
# -*-coding:utf-8 -*-
import base64
import json
from hoshino.typing import MessageSegment, CQEvent
from hoshino import Service, priv, aiorequests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from typing import List, Tuple
import random
from urllib.parse import urlparse
import os

KOOK_BOT_TOKEN = "" # todo 在这里填入bot的token

BASE_URL = "https://www.kookapp.cn/api"

header = {
    "Authorization": f"Bot {KOOK_BOT_TOKEN}"
}

help_ = """
看看谁在kook语音?
[绑定kook服务器ID] 绑定对应的服务器id, 一个群只能绑定一个
[谁在语音] 看看谁在kook语音
""".strip()

sv = Service('看看谁在kook语音', enable_on_default=False, help_=help_, manage_priv=priv.SUPERUSER)

tmp_dir_path = os.path.join(os.path.dirname(__file__), 'tmp')
if not os.path.exists(tmp_dir_path):
    os.mkdir('tmp')

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
if not os.path.exists(config_path):
    with open(config_path, 'w') as f:
        f.write('{}')

with open(config_path, "r") as f:
    config = json.load(f)

script_dir = os.path.dirname(os.path.realpath(__file__))


@sv.on_prefix("绑定kook服务器ID")
async def bind_kook_server_id(bot, ev: CQEvent):
    if not str(ev.message).isdigit():
        await bot.send(ev, "请输入正确格式的kook服务器ID")
    param = {
        'guild_id': str(ev.message)
    }
    response = await aiorequests.get(f'{BASE_URL}/v3/guild/view', headers=header, params=param)
    result = await response.json()
    if result["code"] == 0:
        config[str(ev.group_id)] = str(ev.message)
        with open(config_path, "w") as new:
            json.dump(config, new, indent=4, ensure_ascii=False)
        await bot.send(ev, "绑定成功")
    else:
        await bot.send(ev, "绑定失败")


@sv.on_fullmatch(["看看谁在语音", "谁在语音"])
async def kook_who_in_voice_channel(bot, ev: CQEvent):
    gid = ev.group_id
    if str(gid) not in config:
        await bot.send(ev, "请先绑定kook服务器ID")
        return
    param = {
        'guild_id': config[str(gid)],
        'type': 2
    }

    data = await aiorequests.get(f'{BASE_URL}/v3/channel/list', headers=header, params=param)
    data = await data.json()
    total_count: int = 0
    total_data: List[Tuple[str, dict]] = []

    for channel in data['data']['items']:
        response = await aiorequests.get(f'{BASE_URL}/v3/channel/user-list',
                                         headers=header,
                                         params={'channel_id': channel['id']})
        # todo response.headers 处理频率限制
        tmp_count, user_data = process_channel_info((await response.json())['data'])
        total_count += tmp_count
        total_data.append((channel['name'], user_data))

    base64_image = im2base64str(await output_image(total_count, total_data))
    await bot.send(ev, f'[CQ:image,file={base64_image}]')


def process_channel_info(data: dict) -> tuple:
    process_data = []
    count = 0
    for people in data:
        process_data.append(handle_channel_user_data(people))
        count += 1
    return count, process_data


def handle_channel_user_data(user_data: dict) -> dict:
    name = user_data['nickname'] if user_data['nickname'] else user_data['username']
    avatar_url = user_data['avatar']
    banner_url = user_data['banner']
    return {
        'username': name,
        'avatar_url': avatar_url,
        'banner_url': banner_url
    }


def random_light_color() -> Tuple[int, int, int]:
    return random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)


def process_image(image, target_size):
    # 图片虚化
    image = image.filter(ImageFilter.GaussianBlur(radius=6))  # 高斯模糊背景

    # 将图像等比例放大到目标宽度
    w, h = image.size
    ratio = target_size[0] / w
    new_w = target_size[0]
    new_h = h * ratio
    image = image.resize((int(new_w), int(new_h)))

    # 使图像在y轴上居中
    diff = (new_h - target_size[1]) / 2
    if diff > 0:
        image = image.crop((0, diff, new_w, new_h - diff))
    return image


async def output_image(count: int, data: List[Tuple[str, dict]]) -> Image:
    # 计算图片的宽度
    img_width = 300

    # 频道名占用30px, 用户banner占用60px
    banner_height = 60
    channel_name_height = 40

    # 计算图片的高度
    img_height = banner_height * count + len(data) * channel_name_height

    # 创建图片
    img = Image.new('RGB', (img_width, img_height))
    draw = ImageDraw.Draw(img)

    # 设置字体
    font_path = os.path.join(script_dir, "msyh.ttc")
    font_bold_path = os.path.join(script_dir, "msyhbd.ttc")
    font = ImageFont.truetype(font_path, 15)
    font_bold = ImageFont.truetype(font_bold_path, 15)
    # 图片draw对象的y坐标
    y = 0
    for item in data:
        voice_icon_path = os.path.join(script_dir, "assets", "voice.png")
        voice_icon = Image.open(voice_icon_path, 'r').resize((18, 18))
        img.paste(voice_icon, (10, y + 11))
        draw.text((34, y + 10), item[0], font=font_bold)
        y += channel_name_height

        for user_data in item[1]:
            # 加载并绘制banner图
            if user_data['banner_url']:
                file_path = await download_image_if_not_exist(user_data['banner_url'])
                banner = process_image(Image.open(file_path), (img_width, banner_height))
                img.paste(banner, (0, y))
            else:
                img.paste(random_light_color(), (0, y, img_width, y + banner_height))

            # 加载并绘制avatar图
            file_path = await download_image_if_not_exist(user_data['avatar_url'])

            avatar = Image.open(file_path).resize((50, 50))
            img.paste(avatar, (15, y + 5))  # Place avatar in the middle of the row

            # 绘制用户名
            draw.text((80, y + 20), user_data['username'], font=font, fill=(0, 0, 0))
            y += 60

    return img


async def download_image_if_not_exist(url):
    # 加载并绘制avatar图
    filename = os.path.basename(urlparse(url).path)
    file_path = os.path.join(tmp_dir_path, filename)
    if not os.path.exists(file_path):
        response = await aiorequests.get(url)
        with open(file_path, 'wb') as f:
            f.write(await response.content)
    return file_path


def im2base64str(im) -> str:
    io = BytesIO()
    im.save(io, 'png')
    base64_str = f"base64://{base64.b64encode(io.getvalue()).decode()}"
    return base64_str

