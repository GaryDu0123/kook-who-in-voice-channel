# kook-who-in-voice-channel

# 安装

## 将项目源代码下载或者clone到本地

```bash
git clone https://github.com/GaryDu0123/kook-who-in-channel.git
```

## 将解压出来的文件夹放到`moudules`目录下

期望结构: 

```text
modules/
  ...
  ├── kook-who-in-voice-channel/                            
      ├── __init__.py                          
      ├── assets                               
      │   └── voice.png                        
      ├── config.json
      ├── kook_channel_voice.py
      ├── msyh.ttc
      └── msyhbd.ttc
  ...
```

## 填写bot token

1. 在kook 开发者中心注册bot
  ![image](https://github.com/GaryDu0123/kook-who-in-channel/assets/66729711/1980db7f-ffd7-4127-8c83-a863d6cad25b)

2. 复制bot的token填入到`kook_channel_voice.py`中的`KOOK_BOT_TOKEN`中
  ![image](https://github.com/GaryDu0123/kook-who-in-channel/assets/66729711/f3c73092-3e56-49f3-97fd-51526ffcd74a)

3. 将kook bot加入到需要查看语音频道的kook服务器中

## 在 `__bot__.py` 中启用插件


在`MODULES_ON`中添加`kook-who-in-channel`

