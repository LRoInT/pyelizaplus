#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
#  eliza.py
#
#  a cheezy little Eliza knock-off by Joe Strout
#  with some updates by Jeff Epler
#  hacked into a module and updated by Jez Higgins
# ----------------------------------------------------------------------

import string
import re
import random
import json


class Eliza:
    def __init__(self, path):
        # 加载 gPats, gRelections
        load = json.load(open(path, "r", encoding="utf-8"))
        self.gPats = load["gPats"]
        self.gReflections = load["gReflections"]
        self.keys = [re.compile(x[0], re.IGNORECASE) for x in self.gPats ]  # 编译正则表达式
        self.values = [i[1] for i in self.gPats]
        for i in self.values:
            print(i)

    # ----------------------------------------------------------------------
    # translate: take a string, replace any words found in vocabulary.keys()
    #  with the corresponding vocabulary.values()
    # ----------------------------------------------------------------------
    def translate(self, text, vocabulary):
        words = text.lower().split()
        keys = vocabulary.keys()
        for i in range(len(words)):
            if words[i] in keys:
                words[i] = vocabulary[words[i]]
        return " ".join(words)

    # ----------------------------------------------------------------------
    #  respond: take a string, a set of regexps, and a corresponding
    #    set of response lists; find a match, and return a randomly
    #    chosen response from the corresponding list.
    # ----------------------------------------------------------------------
    def respond(self, text):
        text=text.srtip()
        while text[-1] in "!.?": #去除尾符号
            text = text[:-1]
        # find a match among keys
        for i in range(len(self.keys)): # 正则匹配
            match = self.keys[i].match(text)
            if match:
                # 找到匹配项
                # 从可用选项中随机选择
                resp = random.choice(self.values[i])
                # we've got a response... stuff in reflected text where indicated
                pos = resp.find("%")
                while pos > -1: # 循环到 "%" 处
                    num = int(resp[pos + 1 : pos + 2])
                    resp = (
                        resp[:pos]
                        + self.translate(match.group(num), self.gReflections)
                        + resp[pos + 2 :]
                    )
                    pos = resp.find("%")
                # fix munged punctuation at the end
                if resp[-2:] == "?.":
                    resp = resp[:-2] + "."
                if resp[-2:] == "??":
                    resp = resp[:-2] + "?"
                return resp
        return None


# ----------------------------------------------------------------------
#  command_interface
# ----------------------------------------------------------------------


def command_interface():
    print("Therapist\n---------")
    print("Talk to the program by typing in plain English, using normal upper-")
    print('and lower-case letters and punctuation.  Enter "quit" when done.')
    print("=" * 72)
    print("Hello.  How are you feeling today?")

    s = ""
    therapist = Eliza("./doctor.json")
    while s != "quit":
        try:
            s = input("> ")
        except EOFError:
            s = "quit"
        print(s)
        while s[-1] in "!.?": #去除符号
            s = s[:-1]
        print(therapist.respond(s))


if __name__ == "__main__":
    command_interface()
