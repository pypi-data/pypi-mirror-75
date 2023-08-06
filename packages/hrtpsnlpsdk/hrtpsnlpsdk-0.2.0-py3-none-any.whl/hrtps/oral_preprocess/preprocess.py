import sys
import re
import os
import codecs

sys.path.append(os.getcwd())


class OralPreprocessor(object):
    def __init__(self):
        self.modal_word = list()
        self.aux_word = list()
        self.punc = [",", "?", "。", "，", "!", "！", ";"]
        model_mess_path = os.path.dirname(__file__)
        data_dir = os.path.join(model_mess_path, "..", "data", "oral_preprocess")
        default_modal_word_file = os.path.join(data_dir, "modal_word.txt")
        default_aux_word_file = os.path.join(data_dir, "aux_word.txt")
        self.init_vocab(default_modal_word_file, default_aux_word_file)

    def _read_file(self, filename):
        result_list = list()
        for line in open(filename):
            line = line.rstrip()
            result_list.append(line)
        return result_list

    def init_vocab(self, modal_word_file, aux_word_file):
        self.modal_word = self._read_file(modal_word_file)
        self.aux_word = self._read_file(aux_word_file)

        self.modal_word = set(self.modal_word)
        self.aux_word = set(self.aux_word)
        self.punc = set(self.punc)

    def process_punc(self, text):
        new_text = list()
        new_to_origin_index = list()
        for i, x in enumerate(text):
            if i > 0 and \
                    x in self.punc and \
                    text[i-1] in self.punc:
                continue
            new_text.append(x)
            new_to_origin_index.append(i)
        return new_text, new_to_origin_index

    def process_modal_word(self, text):
        new_text = list()
        new_to_origin_index = list()
        for i, x in enumerate(text):
            if x in self.modal_word:
                continue
            new_text.append(x)
            new_to_origin_index.append(i)
        return new_text, new_to_origin_index

    def process_aux_word(self, text):
        new_text = list()
        new_to_origin_index = list()

        buf_text = list()
        buf_index = list()
        for i, x in enumerate(text):
            if x in self.punc:
                tmp_text = "".join(buf_text)
                if tmp_text in self.aux_word:
                    pass
                else:
                    new_text += buf_text
                    new_to_origin_index += buf_index
                    new_text.append(x)
                    new_to_origin_index.append(i)

                buf_text = []
                buf_index = []
            else:
                buf_text.append(x)
                buf_index.append(i)

        if buf_text:
            new_text += buf_text
            new_to_origin_index += buf_index
        return new_text, new_to_origin_index

    def process(self, text):
        new_text, new_to_origin_index1 = self.process_aux_word(text)
        new_text, new_to_origin_index2 = self.process_modal_word(new_text)
        new_text, new_to_origin_index3 = self.process_punc(new_text)

        new_to_origin_index = [new_to_origin_index2[x] for x in new_to_origin_index3]
        new_to_origin_index = [new_to_origin_index1[x] for x in new_to_origin_index]
        new_text = "".join(new_text)
        return new_text, new_to_origin_index


def main(in_file, out_file):
    processor = OralPreprocessor()
    processor.init_vocab('../data/oral_preprocess/modal_word.txt', '../data/oral_preprocess/aux_word.txt')

    result_list = list()
    for line in open(in_file):
        line = line.rstrip()
        line, _ = processor.process(line)
        result_list.append(line)
    
    with codecs.open(out_file, 'w', 'utf-8') as writer:
        for line in result_list:
            writer.write("%s\n" % line)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python %s in_file out_file" % sys.argv[0])
        exit(0)
    main(sys.argv[1], sys.argv[2])
