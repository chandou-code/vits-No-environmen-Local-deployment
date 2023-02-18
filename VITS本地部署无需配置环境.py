import requests
import json
import re
import time
import threading
import os
from pydub import AudioSegment
import tqdm
global name
global now
global name_list
global list_of_slices
now=0
list_of_slices=[]
name_list=[]
global size
def read_download():
    global name
    choice=input('1:继续下载 2:重新加载文本')
    choice=int(choice)
    if choice==1:
        with open('config.json', 'r') as f:
            name = f.read()
            name=int(name)
            f.close()
    elif choice==2:
        name=1
def getname():
    url1 = 'http://dullwolf.natapp1.cc/sovits/getAllMod'
    response=requests.post(url=url1)
    print(response.text)
def readwork():
    global lines
    global size
    global list_of_slices

    lines=[]
    filename='tts.txt'
    with open(filename,'r' ,encoding='utf-8')as f:
        lines=f.read()
    lines = re.sub(r'[\n\\n]', '', lines)
    # print(lines)
    size=len(lines)
    list_of_slices = [lines[i:i + 10] for i in range(0, size, 10)]
def usingapi(text):
    global name
    global size
    global now
    url2 = 'http://dullwolf.natapp1.cc/sovits/genByText'
    text=f"[ZH]{text}[ZH]"
    print(text)
    data = {"modelId": "7", "roleId": "10", "text": f"{text}"}
    data = json.dumps(data, ensure_ascii=False)
    # print(data2)
    response2 = requests.post(url=url2, data=data.encode("utf-8"),timeout=111111)
    returnjson = response2.text
    # print(returnjson)
    txt = returnjson
    txt = re.findall(r'".*?"', txt, re.S)
    txt[2] = re.sub(r'"', '', txt[2], re.S)
    downlown = txt[2]
    url3 = f'https://dullwolf.oss-accelerate.aliyuncs.com/{downlown}.wav.wav'
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
def save(name):
    with open('config.json','w') as fp:
        str_name=str(name)
        fp.write(str_name)
        fp.close()
# def craw():
#     url2 = 'http://dullwolf.natapp1.cc/sovits/genByText'

if __name__ == '__main__':

    def work():
        global now
        global name
        global list_of_slices
        read_download()
        readwork()
        for x in range(name, len(list_of_slices)+1):
            save(name)
            usingapi(list_of_slices[x])
            now = (name + 1) / len(list_of_slices) * 100
        conbine_wav()
        delete_temp()
    work()
    #getname()





