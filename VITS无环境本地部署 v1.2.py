import requests
import json
import re
import time
import os
from pydub import AudioSegment


global name
global now
global name_list
global list_of_slices
now = 0
list_of_slices = []
name_list = []
global size


def read_download():
    global name
    choice = input('1:继续下载 2:重新加载文本')
    choice = int(choice)
    if choice == 1:
        with open('config.json', 'r') as f:
            name = f.read()
            name = int(name)
            f.close()
    elif choice == 2:
        name = 1


def getname():
    url1 = 'http://dullwolf.natapp1.cc/sovits/getAllMod'
    response = requests.post(url=url1)
    print(response.text)


def readwork():
    global lines
    global size
    global list_of_slices
    global ID
    lines = []
    filename = 'tts.txt'
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.read()
    lines = re.sub(r'[\n\\n]', '', lines)
    # print(lines)
    size = len(lines)
    print('输入文本模式')
    io = input(
        '1:把文本切成十个字然后合成，适用于评论区，弹幕等缺少标点符号的情况 2:切割标点符号，适用于小说等长篇')
    io=int(io)
    ID=input('输入角色语音ID(详情请看文档模型ID，派蒙为551)')
    if io == 1:
        list_of_slices = [lines[i:i + 10] for i in range(0, size, 10)]

    elif io == 2:

        list_of_slices = re.split("[,;:,。，！!?？.]",lines)
        # list_of_slices=lines.split('，')

        mode=input('1：原版语音 2：优化语音(平静情绪，感情起伏更小)')
        mode=int(mode)
        if mode==2:
            list_of_slices = [x + "~" for x in list_of_slices]


def usingapi(text):
    global name
    global size
    global now
    global ID
    url2 = 'http://dullwolf.natapp1.cc/sovits/genByText'
    print(text)
    text = f"[ZH]{text}[ZH]"
    data = {"modelId": "3", "roleId": f"{ID}", "text": f"{text}"}
    data = json.dumps(data, ensure_ascii=False)
    # print(data2)
    response2 = requests.post(url=url2, data=data.encode("utf-8"), timeout=111111)
    returnjson = response2.text
    # print(returnjson)
    txt = returnjson
    txt = re.findall(r'".*?"', txt, re.S)
    txt[2] = re.sub(r'"', '', txt[2], re.S)
    url3 = txt[2]
    print(url3)
    reponse3 = requests.get(url=url3)
    resouce = reponse3.content
    set_name(resouce)
    print(f'完成进度{now}')


def set_name(resouce):
    global name
    global name_list
    with open(f"{name}.wav", mode='wb') as f:
        f.write(resouce)
    name_list.append(f"{name}.wav")
    name += 1


def conbine_wav():
    global name_list
    combined = AudioSegment.empty()
    for audio_file in name_list:
        combined += AudioSegment.from_wav(audio_file)
    combined.export("combined.wav", format="wav")


def delete_temp():
    global name_list
    for i in name_list:
        os.remove(i)
        print(f'临时文件{i}已删除')
    print('conbined.wav合成完毕')
    print('建议0.87倍速食用')


def save(name):
    with open('config.json', 'w') as fp:
        str_name = str(name)
        fp.write(str_name)
        fp.close()


# def craw():
#     url2 = 'http://dullwolf.natapp1.cc/sovits/genByText'


if __name__ == '__main__':
    print('十分感谢大佬@dullwolf蠢狼提供的API!!!!!! by-b站@纯度Official @dullwolf蠢狼')
    def work():
        global now
        global name
        global list_of_slices
        read_download()
        readwork()
        for x in range(name-1, len(list_of_slices) ):
            save(name)
            usingapi(list_of_slices[x])
            now = (name) / len(list_of_slices) * 100
        conbine_wav()
        delete_temp()
    start=time.time()
    work()
    end=time.time()
    print(f'共耗时{end-start}s')


    # getname()
