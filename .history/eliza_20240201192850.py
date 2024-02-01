import logging
import random
import re
from collections import namedtuple
import datetime
import os

# Fix Python2/Python3 incompatibility

# 日志
if not os.path.exists("./log"):
    os.mkdir("./log")

log_name = "./log/log"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + \
    ".log"  # 日志文件命名 年,月,日,时,分
log = logging.getLogger(__name__)
formatter = logging.Formatter(  # 消息格式
    '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
file_handler = logging.FileHandler(log_name, encoding='UTF-8')  # 日志文件
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
log.addHandler(file_handler)
#log.propagate = False  # 不再控制台输出


class Key:
    def __init__(self, word, weight, decomps):
        self.word = word
        self.weight = weight
        self.decomps = decomps

    def __str__(self):
        return f"{self.word},{self.weight},{self.decomps}"

    def __repr__(self):
        return self.__str__()


class Decomp:
    def __init__(self, parts, save, reasmbs):
        self.parts = parts
        self.save = save
        self.reasmbs = reasmbs
        self.next_reasmb_index = 0

    def __str__(self):
        return f"{self.parts},{self.save},{self.reasmbs},{self.next_reasmb_index}"

    def __repr__(self):
        return self.__str__()


class Eliza:
    def __init__(self):
        self.initials = []
        self.finals = []
        self.quits = []
        self.pres = {}
        self.posts = {}
        self.synons = {}
        self.keys = {}
        self.memory = []
        self.symbol = []
        self.sym_ch_en = {}

    def load(self, path):
        key = None
        decomp = None
        with open(path, encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                tag, content = [part.strip() for part in line.split(':')]
                if tag == 'initial':  # 开始语
                    self.initials.append(content)
                elif tag == 'final':  # 结束语
                    self.finals.append(content)
                elif tag == 'quit':  # 退出词
                    self.quits.append(content)
                elif tag == 'pre':  # 同义词
                    parts = content.split(' ')
                    self.pres[parts[0]] = parts[1:]
                elif tag == 'post':
                    parts = content.split(' ')
                    self.posts[parts[0]] = parts[1:]
                elif tag == 'synon':
                    parts = content.split(' ')
                    self.synons[parts[0]] = parts
                elif tag == 'key':  # 关键词
                    parts = content.split(' ')
                    word = parts[0]
                    weight = int(parts[1]) if len(parts) > 1 else 1
                    key = Key(word, weight, [])
                    self.keys[word] = key
                elif tag == 'decomp':
                    parts = content.split(' ')
                    save = False
                    if parts[0] == '$':
                        save = True
                        parts = parts[1:]
                    decomp = Decomp(parts, save, [])
                    key.decomps.append(decomp)
                elif tag == 'reasmb':
                    parts = content.split(' ')
                    decomp.reasmbs.append(parts)
                elif tag == 'symbol':  # 正式符号(英文)
                    self.symbol.append(content)
                elif tag == 'sym_ch_en':  # 中文符号转英文符号
                    parts = content.split(' ')
                    self.sym_ch_en[parts[0]] = parts[1]

    def _match_decomp_r(self, parts, words, results):
        if not parts and not words:
            return True
        if not parts or (not words and parts != ['*']):
            return False
        if parts[0] == '*':
            for index in range(len(words), -1, -1):
                results.append(words[:index])
                if self._match_decomp_r(parts[1:], words[index:], results):
                    return True
                results.pop()
            return False
        elif parts[0].startswith('@'):
            root = parts[0][1:]
            if not root in self.synons:
                raise ValueError("Unknown synonym root {}".format(root))
            if not words[0].lower() in self.synons[root]:
                return False
            results.append([words[0]])
            return self._match_decomp_r(parts[1:], words[1:], results)
        elif parts[0].lower() != words[0].lower():
            return False
        else:
            return self._match_decomp_r(parts[1:], words[1:], results)

    def _match_decomp(self, parts, words):
        results = []
        if self._match_decomp_r(parts, words, results):
            return results
        return None

    def _next_reasmb(self, decomp):
        index = decomp.next_reasmb_index
        result = decomp.reasmbs[index % len(decomp.reasmbs)]
        decomp.next_reasmb_index = index + 1
        return result

    def _reassemble(self, reasmb, results):
        output = []
        for reword in reasmb:
            if not reword:
                continue
            if reword[0] == '(' and reword[-1] == ')':
                index = int(reword[1:-1])
                if index < 1 or index > len(results):
                    raise ValueError("Invalid result index {}".format(index))
                insert = results[index - 1]
                for punct in [',', '.', ';']:
                    if punct in insert:
                        insert = insert[:insert.index(punct)]
                output.extend(insert)
            else:
                output.append(reword)
        return output

    def _sub(self, words, sub):
        # 输入一个可迭代对象 words , 遍历 words
        # 在 sub 中搜索键 word 完成转换, 如果没有表明不需要转换
        output = []
        for word in words:
            word_lower = word.lower()  # 小写
            if word_lower in sub:
                output.extend(sub[word_lower])  # 匹配
            else:
                output.append(word)  # 添加本身
        return output

    def _match_key(self, words, key):
        for decomp in key.decomps:
            results = self._match_decomp(decomp.parts, words)
            if results is None:
                log.debug('Decomp did not match: %s', decomp.parts)
                continue
            log.debug('Decomp matched: %s', decomp.parts)
            log.debug('Decomp results: %s', results)
            results = [self._sub(words, self.posts) for words in results]
            log.debug('Decomp results after posts: %s', results)
            reasmb = self._next_reasmb(decomp)
            log.debug('Using reassembly: %s', reasmb)
            if reasmb[0] == 'goto':
                goto_key = reasmb[1]
                if not goto_key in self.keys:
                    raise ValueError("Invalid goto key {}".format(goto_key))
                log.debug('Goto key: %s', goto_key)
                return self._match_key(words, self.keys[goto_key])
            output = self._reassemble(reasmb, results)
            if decomp.save:
                self.memory.append(output)
                log.debug('Saved to memory: %s', output)
                continue
            return output
        return None

    def sym_replace(self, text):
        for i in self.sym_ch_en: # 中文符号转英文符号
            if i in text:
                text = text.replace(i, self.sym_ch_en[i])
        for i in self.symbol:
            text = re.sub(r'\s*\{}+\s*'.format(i), f' {i} ', text)
        return text

    def respond(self, text):
        log.debug("---respond(%s)---", text)
        if text.lower() in self.quits:
            log.debug("Quit")
            return None

        # 将句号,逗号,分号替换为原符号在左右添加空格
        text = self.sym_replace(text)
        log.debug('After punctuation cleanupv 有效词语: %s', text)

        words = [w for w in text.split(' ') if w]  # 将 text 转为 以单词为项的列表
        log.debug('Input 输入: %s', words)

        words = self._sub(words, self.pres)  # 将 words 内的单词转化为统一的单词
        log.debug('After pre-substitution 统一用词: %s', words)

        keys = [self.keys[w.lower()] for w in words if w.lower()
                in self.keys]  # 在keys中匹配words中的单词
        keys = sorted(keys, key=lambda k: -k.weight)  # 排序
        log.debug('Sorted keys 被匹配的关键词: %s', [
                  (k.word, k.weight) for k in keys])

        output = None

        for key in keys:
            output = self._match_key(words, key)
            if output:
                log.debug('Output from key: %s', output)
                break
        if not output:
            if self.memory:
                index = random.randrange(len(self.memory))
                output = self.memory.pop(index)
                log.debug('Output from memory: %s', output)
            else:
                output = self._next_reasmb(self.keys['xnone'].decomps[0])
                log.debug('Output from xnone: %s', output)

        return " ".join(output)

    def initial(self):
        return random.choice(self.initials)

    def final(self):
        return random.choice(self.finals)

    def run(self):
        print(self.initial())

        while True:
            sent = input('> ')

            output = self.respond(sent)
            if output is None:
                break

            print(output)

        print(self.final())


def main():
    eliza = Eliza()
    eliza.load('doctor.txt')
    eliza.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
