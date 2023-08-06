import os
import sys
import re
import codecs

class RuleSubjectPredictEx(object):
    def __init__(self):
        self.regexp_list = list()
        self.regexp_obj_list = list()
        self.punc = [",", "?", "。", "，", "!", "！", ";", "；", ":", "："]
        self.punc = set(self.punc)
        self.THRESHOLD = 0.1

        model_mess_path = os.path.dirname(__file__)
        default_reg_file = os.path.join(model_mess_path, "..", "data", "rule_subject", "subject_regexp.txt")
        self.init(default_reg_file)

    def predict_doc(self, text:str):
        label, _, _ = self.process(text)
        return {"predictions": [label]}

    def init(self, reg_file):
        for line in codecs.open(reg_file, 'r', 'utf-8'):
            line = line.rstrip()
            buf = list()
            # add ignore symbol
            for w in line:
                buf.append(w)
                if w == '(':
                    buf += ["?", ":"]
            line = "".join(buf)
            self.regexp_list.append(line)
            ptnObj = re.compile(line)
            self.regexp_obj_list.append((ptnObj, line))

    def process(self, text):
        new_text = self._preprocess(text)
        #print(new_text)
        #exit(0)
        label, match_text, match_exp = self._process(new_text)
        if label == 1:
            label, score = self._postprocess(new_text)
            match_text.append(str(score))
            match_exp.append("ratio")
        return label, match_text, match_exp

    def _process(self, text):
        label = 1
        match_exp = list()
        match_text = list()
        for regObj, ptn in self.regexp_obj_list:
            res = regObj.findall(text)
            max_match_text = ''
            if res:
                for item in res:
                    if len(item) > len(max_match_text):
                        max_match_text = item
                match_exp.append(ptn)
                match_text.append(max_match_text)
                label = 0

        return label, match_text, match_exp

    def find_and_count(self, text, substr):
        count = 0
        start_pos = 0
        while True:
            find_idx = text.find(substr, start_pos)
            if find_idx == -1:
                break
            count += 1
            start_pos = find_idx + len(substr)
        return count

    def _postprocess(self, text):
        i_count = self.find_and_count(text, '我')
        we_count = self.find_and_count(text, '我们')
        i_except_count1 = self.find_and_count(text, '我的')
        i_except_count2 = self.find_and_count(text, '让我')
        i_except_count3 = self.find_and_count(text, '给我')
        i_except_count4 = self.find_and_count(text, '使我')
        we_except_count1 = self.find_and_count(text, '我们的')
        we_except_count2 = self.find_and_count(text, '让我们')
        we_except_count3 = self.find_and_count(text, '给我们')
        we_except_count4 = self.find_and_count(text, '使我们')

        i_count -= i_except_count1
        i_count -= i_except_count2
        i_count -= i_except_count3
        i_count -= i_except_count4
        i_count = max(i_count, 0)

        we_count -= we_except_count1
        we_count -= we_except_count2
        we_count -= we_except_count3
        we_count -= we_except_count4

        if i_count == 0:
            return 0, 0.0
        else:
            ratio = float(we_count) / float(i_count)
            
            if ratio <= self.THRESHOLD:
                return 0, ratio
            else:
                return 1, ratio

    def normalize(self, text):
        text = text.replace(" ", "")
        text = text.replace("\t", "")
        text = text.replace("\r", "")
        text = text.lower()
        return text

    def _preprocess(self, text):
        text = self.normalize(text)
        text = text.replace("本人", "我")
        text_list = text.split()
        new_text_list = list()
        for x in text:
            if x in self.punc:
                new_text_list.append(',')
            else:
                new_text_list.append(x)
        return "".join(new_text_list)

def main(in_file, out_file):
    m = RuleSubjectPredictEx()
    #m.init()

    result_list = list()
    for line in codecs.open(in_file, 'r', 'utf-8'):
        line = line.rstrip('\n')
        text = line.split('\t')[0]
        #text = text.replace("本人", "我")
        #text = text.replace(" ","")
        #text = text.lower()
        label, match_text, match_exp = m.process(text)
        if match_text: 
            #match_text_case = match_text[0]
            match_text_case = match_text[0]
        else:
            match_text_case = ''
        result_list.append((text, label, match_text_case))

    with codecs.open(out_file, 'w', 'utf-8') as writer:
        for text, label, match_text in result_list:
            writer.write("%s\t%g\t%s\n" % (text, label, match_text))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python %s in_file out_file" % sys.argv[0])
        exit(0)
    main(sys.argv[1], sys.argv[2])

