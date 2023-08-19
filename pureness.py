import io
import os
import re

import ffmpeg
import requests
import logging
import time
import sys

logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为INFO
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[

        logging.StreamHandler()  # 输出到控制台
    ]
)
limit = 2000
sys.setrecursionlimit(limit)


def role2id(role):
    speaker = m1.get_speaker()
    import re
    for e in range(len(speaker)):
        pattern = r"\（.*?\）"
        name = re.sub(pattern, "", speaker[e], re.S)
        if name != speaker[e]:
            speaker[e] = name
    for s in range(len(speaker)):
        if role == speaker[s]:
            return s


def id2role(id):
    import re
    speaker = m1.get_speaker()
    for e in range(len(speaker)):
        pattern = r"\（.*?\）"
        speaker[e] = re.sub(pattern, "", speaker[e], re.S)
    return speaker[int(id)]


class CUT200:
    def __init__(self):
        self.new = []
        self.newnew = []

    def slice_string(self, text):
        if len(text) < 200:
            return text

        mid_index = len(text) // 2
        left_part = ''
        right_part = ''

        for i in range(mid_index, -1, -1):
            if text[i] in ['，', '。', '！', '？', '!', '.', '?', '~', '～']:  # '、', '」', '」', '“', '，', '。'
                left_part = text[:i + 1]
                right_part = text[i + 1:]
                break

        return left_part, right_part

    def str2list(self, content):
        if isinstance(content, str):
            content_list = ['']
            content_list[0] = content

            return self.main_cutting(content_list)

    def main_cutting(self, content):

        self.newnew = content
        start = time.time()
        for i in range(50):
            self.new = []

            for l in self.newnew:

                if len(l) > 200:

                    left, right = self.slice_string(l)

                    self.new.append(left)
                    self.new.append(right)

                else:
                    selfless = self.slice_string(l)
                    self.new.append(selfless)
            # self.new = [item for item in content_list if item != '' and item is not None]
            string_list = []
            for item in self.new:
                string_list.append(str(item))
            self.new = [item for item in self.new if item != '' and item is not None]
            self.new = string_list
            self.newnew = self.new

        end = time.time()
        print(f'切片完成，耗时{end - start}')
        return [item for item in self.new if item != '' and item is not None]


class conbined_wavs:

    def __init__(self):
        self.name = None

    def make_valid_filename(self, filename):
        import re
        import os
        # 去除非法字符
        valid_filename = re.sub(r'[<>:"/\\|?*\s]', '', filename)

        # # 删除连续的空格
        # valid_filename = re.sub(r'\s+', ' ', valid_filename)

        return valid_filename

    def add_name(self, name):
        self.name = self.make_valid_filename(str(name))

    def conbine(self, wavs):

        content_list = wavs
        # print(content_list)
        # inputs = []
        # for file in content_list:
        #     inputs.append(ffmpeg.input(file))
        # # 合并输入流到一个输出流中

        # output = ffmpeg.concat(*inputs, v=0, a=1).output(f'{self.name}.wav')
        # ffmpeg.run(output)
        ffmpeg_path = r'./ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe'

        # 设置输入文件和输出文件路径
        input_files = content_list  # 假设content_list是包含待拼接语音文件的列表
        # output_file = '路径/输出文件.wav'

        inputs = []
        for file in input_files:
            inputs.append(ffmpeg.input(file))

        # 合并输入流到一个输出流中
        output = ffmpeg.concat(*inputs, v=0, a=1).output(f'{self.name}.wav')
        ffmpeg.run(output, cmd=ffmpeg_path)
        # for file_name in content_list:
        #     if os.path.exists(file_name):
        #         os.remove(file_name)
        #         print(f"已删除临时文件: {file_name}")
        #     else:
        #         print(f"临时文件不存在: {file_name}")


class main:
    def __init__(self):
        self.content = []
        self.wavs = []

    def read(self):
        speakers = m1.get_speaker()
        tempid = int(input('输入模型ID(96是安柏，133是八重神子，具体看模型列表):'))
        long = float(input('输入语速(推荐1):'))
        s = 1 / long


        with open('tts.txt', 'r', encoding='utf-8') as f:
            self.content = f.read().replace('\n ', '').replace('\n', '').replace('　　', '').replace('   ',
                                                                                                   '').replace(
                'amp;', '')
        if len(self.content) < 130000:
            self.content = c3.str2list(self.content)
            long = len(self.content)
            for i in range(long):
                process = f'{i}/{long}'
                logging.info(f'{process}|{speakers[tempid]}|{self.content[i][:8]}......')
                url = f'http://175.178.176.3:5000/run?text={self.content[i]}&id_speaker={tempid}&length={s}&noise=0.25&noisew=0.4'
                # print(url)
                r = requests.get(url)
                stream = io.BytesIO(r.content)
                file = f'./GPU音频/{time.time()}.wav'
                with open(file, "wb") as f:
                    f.write(stream.getvalue())
                self.wavs.append(file)
            # 使用 time.localtime() 将时间戳转换为具体时间
            local_time = time.localtime(time.time())

            # 格式化输出具体时间
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            # print(formatted_time)
            c1.add_name(f'{id2role(tempid)}-{formatted_time}')
            # print(self.wavs)
            c1.conbine(self.wavs)
            print(f'{id2role(tempid)}-{formatted_time}合成完成')
            input("按任意键退出...")

    def get_speaker(self):
        with open('speaker.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        decoded_string = content.encode().decode('unicode_escape')
        result_list = eval(decoded_string)
        for result in range(len(result_list)):
            pattern = r"\（.*?\）"
            result_list[result] = re.sub(pattern, "", result_list[result], re.S)
        return result_list


if __name__ == '__main__':
    c1 = conbined_wavs()
    c3 = CUT200()
    m1 = main()
    m1.read()
    # print(m1.get_speaker())
