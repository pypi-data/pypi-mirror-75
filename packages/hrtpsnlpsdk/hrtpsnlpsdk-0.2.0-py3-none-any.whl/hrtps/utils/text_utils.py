import math
import os
import unicodedata

import numpy as np
import requests

from hrtps.kashgari.process import load_processor


def sen_tokenizer(text: str, split_set="。!?！？"):
    sen = []
    sen_ind = 0
    for i, cs in enumerate(text):
        if cs in split_set:
            sen.append(cs)
            if len("".join(sen).strip()) > 1:
                yield sen, sen_ind, len(sen)
            # yield sen, sen_ind, len(sen)
            sen = []
            sen_ind = i + 1
        else:
            sen.append(cs)
    else:
        if len("".join(sen).strip()) > 1:
            yield sen, sen_ind, len(sen)


def min_len_sen_tokenizer(text: str, split_set="。!?！？", minlen=128):
    """
    句子切分， 同时设置切分长度， 当单句过长时进行分割
    :param text:
    :param split_set:
    :param minlen:
    :return:
    """
    for sen_s in sen_tokenizer(text, split_set):
        sen_text, sen_ind, sen_len = sen_s
        if len(sen_text) < minlen:
            yield sen_s
        else:
            # 次数
            subnub = math.ceil(len(sen_text) / minlen)
            # 每次的长度
            step = math.ceil(len(sen_text) / subnub)
            for i in range(0, len(sen_text), step):
                sub_sen_text = sen_text[i: i + step]
                sub_sen_len = len(sub_sen_text)
                sub_sen_ind = sen_ind + i
                yield sub_sen_text, sub_sen_ind, sub_sen_len


class MaskSenSuber(object):

    # def __init__(self, req_url=f"http://model.ai-open.hrtps.com/v1/models/subsen_masktoken_lstmcrf_epoch1_batch32_seq512:predict"):
    def __init__(self, req_url=f"http://model.ai-open.hrtps.com/v1/models/sen-sub:predict"):
        self.req_url = req_url
        model_mess_path = os.path.dirname(__file__)
        self.sub_process = load_processor(os.path.join(model_mess_path, "..", "data", "subsen", "mask_model_info.json"))
        self.mask_token = "[MASK]"
        # self.mask_token = "[UNK]"

    def format_inp(self, inp):
        """
        文本格式化、去除标点符号
        :param inp:
        :return:
        """
        splice_token = "。!?！？；;，,"
        for i in inp:
            if i not in splice_token:
                yield i
            else:
                yield self.mask_token

    def predict(self, texts: list):
        """
        调用API
        :param text:
        :return:
        """

        token_texts = [tokenize(text) for text in texts]
        texts = [list(self.format_inp(text)) for text in token_texts]

        tensor = self.sub_process.process_x_dataset(texts)
        tensor = [{
            "Input-Token:0": i.tolist(),
            "Input-Segment:0": np.zeros(i.shape).tolist()
        } for i in tensor]

        r = requests.post(self.req_url, json={"instances": tensor})
        if r.status_code == 404:
            raise Exception("api not fount error: {}".format(self.req_url))
        preds = r.json()['predictions']
        return preds, texts, token_texts

    def seq_sen_sub(self, texts: list):
        """
        使用序列模型切分句子
        :param texts:
        :return:
        """
        id2label = self.sub_process.idx2label
        preds, x_datas, token_texts = self.predict(texts)

        for sen_i, x_data in enumerate(x_datas):
            text_line = token_texts[sen_i]
            pred = preds[sen_i][1:]
            # x_data = x_datas[i]
            sub_sen = []
            max_ind = np.argmax(pred, axis=1)
            pre_label = [id2label[p] for p in max_ind]
            # 在最后增加一个结束符
            pre_label.append("E")
            subsen = ""
            # for i, pre in enumerate(pre_label):
            # for i, token in enumerate(x_data):
            for i, token in enumerate(text_line):
            # for i, pre in enumerate(pre_label):
            #     token = text_line[i]
                if i >= len(pre_label):
                    break

                pre = pre_label[i]
                subsen += token
                if pre == "E":
                    sub_sen.append(subsen)
                    subsen = ""
            if len(subsen) > 0:
                sub_sen.append(subsen)
            yield sub_sen

    def seq_sen_sub_len_limit(self, text: str, split_set="。!?！？", maxlen=128):
        """
        优先使用标点符号，当文本过长时使用序列模型
        :param text:
        :param split_set:
        :param maxlen:
        :return:
        """
        if split_set:
            for sen_s in sen_tokenizer(text, split_set):
                sen_text, sen_ind, sen_len = sen_s
                sen_text = "".join(sen_text)
                if len(sen_text) < maxlen:
                    yield sen_text
                else:
                    for r in self.seq_sen_sub([sen_text]):
                        for sen in r:
                            yield sen

    def seq_rule_sen_sub(self, text: str, window=500):
        text_len = len(text)+1
        if text_len < window:
            for sens in self.seq_sen_sub([text]):
                for sen in sens:
                    yield sen
            # return self.seq_sen_sub([text])
        else:
            subs = []
            for i in range(0, text_len, window):
                sub_sen = text[i:i+window]
                if len(sub_sen) > 0:
                    subs.append(sub_sen)
            for sens in self.seq_sen_sub(subs):
                for sen in sens:
                    yield sen


mask_seq_sub = MaskSenSuber().seq_sen_sub
mask_limit_seq_sub = MaskSenSuber().seq_sen_sub_len_limit
seq_rule_sen_sub = MaskSenSuber().seq_rule_sen_sub


SEP = "[SEP]"


def is_whitespace(char):
    """Checks whether `chars` is a whitespace character."""
    # \t, \n, and \r are technically contorl characters but we treat them
    # as whitespace since they are generally considered as such.
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False


def is_control(char):
    """Checks whether `chars` is a control character."""
    # These are technically control characters but we count them as whitespace
    # characters.
    if char == "\t" or char == "\n" or char == "\r":
        return False
    cat = unicodedata.category(char)
    if cat in ("Cc", "Cf"):
        return True
    return False


def clean_text(text):
    """Performs invalid character removal and whitespace cleanup on text."""
    output = []
    for char in text:
        cp = ord(char)
        if cp == 0 or cp == 0xfffd or is_control(char):
            continue
        if is_whitespace(char):
            output.append(" ")
        else:
            output.append(char)
    return "".join(output)


def is_chinese_char(cp):
    """Checks whether CP is the codepoint of a CJK character."""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all of the other languages.
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
            (cp >= 0x3400 and cp <= 0x4DBF) or  #
            (cp >= 0x20000 and cp <= 0x2A6DF) or  #
            (cp >= 0x2A700 and cp <= 0x2B73F) or  #
            (cp >= 0x2B740 and cp <= 0x2B81F) or  #
            (cp >= 0x2B820 and cp <= 0x2CEAF) or
            (cp >= 0xF900 and cp <= 0xFAFF) or  #
            (cp >= 0x2F800 and cp <= 0x2FA1F)):  #
        return True
    return False


def tokenize_chinese_chars(text):
    """Adds whitespace around any CJK character."""
    output = []
    for char in text:
        cp = ord(char)
        if is_chinese_char(cp):
            output.append(" ")
            output.append(char)
            output.append(" ")
        else:
            output.append(char)
    return "".join(output)


def whitespace_tokenize(text):
    """Runs basic whitespace cleaning and splitting on a piece of text."""
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    return tokens


def tokenize(text):
    text = clean_text(text)
    tks = tokenize_chinese_chars(text)
    return whitespace_tokenize(tks)
