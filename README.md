# kook-who-in-voice-channel

群友偷偷开黑? 看看谁在kook语音



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

# 总览

![image](https://github.com/GaryDu0123/kook-who-in-channel/assets/66729711/b18e7c43-fb49-4ab5-a6bd-3a28e24f5eab)

![image](https://github.com/GaryDu0123/kook-who-in-channel/assets/66729711/96d42394-eba6-4bdc-b5a1-77ea322e52cc)


# 目前的局限性

1. 一个群只能绑定一个kook频道
2. 绑定的kook频道必须是bot已经加入的, 但只是调用api, 不会影响kook bot上运行的服务
3. 没有对绑定频道的验证机制, 也就是任何群可以绑定bot已经加入的频道

# 使用方法

```python
help_ = """
看看谁在kook语音?
[绑定kook服务器ID] 绑定对应的服务器id, 一个群只能绑定一个
[谁在语音] 看看谁在kook语音
"""
```

## 绑定kook服务器ID

1. 打开kook的开发者模式
   ![image](https://github.com/GaryDu0123/kook-who-in-channel/assets/66729711/d24d879a-59ba-4d6e-8f17-59f049fc64b4)
2. 右键kook服务器头像, 选择复制ID
   ![image](https://github.com/GaryDu0123/kook-who-in-channel/assets/66729711/696bcd8d-e6db-43ef-9d9a-d5549847c91b)
3. 在QQ群中发送`绑定kook服务器ID XXXXXXXXXXXXXXXX` X为你实际的ID

## 谁在语音

看看谁在kook语音
