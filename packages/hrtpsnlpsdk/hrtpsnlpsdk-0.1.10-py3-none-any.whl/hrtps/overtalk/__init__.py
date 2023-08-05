import os
import requests
import collections, json
import traceback

from .over import OvertalkDetector
from ..utils import tokenization


class NNOvertalkDetecter(object):

    def __init__(self, pre_url):
        model_mess_path = os.path.dirname(__file__)
        vocab_file = os.path.join(model_mess_path, "..", "data", "overtalk", "vocab.txt")
        self.pre_url = pre_url
        self.tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file)
        self.max_seq_length = 384
        self.THRESHOLD = 2.0


    def trans_tensor(self, texts):
        data_list = list()
        index_map = list()
        lengths = list()
        for query in texts:
            tokens_a = self.tokenizer.tokenize(query)
            tokens_b = None
            if len(tokens_a) > self.max_seq_length - 2:
                tokens_a = tokens_a[0:(self.max_seq_length - 2)]

            tok_to_orig_index, orig_to_tok_index = self.convert_tokens_to_origin_index(tokens_a, query, self.max_seq_length)

            tokens = list()
            tokens.append('[CLS]')
            tokens += tokens_a
            tokens.append('[SEP]')

            segment_ids = [0 for _ in tokens]
            input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
            input_mask = [1] * len(input_ids)

            lengths.append(len(input_mask))

            while len(input_ids) < self.max_seq_length:
                input_ids.append(0)
                input_mask.append(0)
                segment_ids.append(0)

            feature = {"input_ids": input_ids, "input_mask": input_mask, "segment_ids": segment_ids}
            data_list.append(feature)
            index_map.append((tok_to_orig_index, orig_to_tok_index))

        tensor_data = {"instances": data_list}
        return tensor_data, index_map, lengths

    def predict_doc(self, text1: str):
        tensor_data, index_map, lengths = self.trans_tensor([text1])
        orig_to_tok_index, tok_to_orig_index = index_map[0]
        resp = requests.post(self.pre_url, json=tensor_data)
        resp_json = resp.json()
        result = self.format_result(resp_json, text1, orig_to_tok_index, tok_to_orig_index, lengths[0])
        return {"predictions": result}

    def convert_tokens_to_origin_index(self, tokens, raw_text, max_seq_length):
        all_text = ''
        start_pos = 0
        tok_to_orig_index = list()
        orig_to_tok_index = list()
        for i, token in enumerate(tokens):
            if token[:2] == '##':
                token = token[2:]
            findIdx = raw_text.find(token, start_pos)
            if findIdx == -1:
                end_pos = start_pos + len(token)
            else:
                start_pos = findIdx
                end_pos = start_pos + len(token)
            tok_to_orig_index.append(start_pos)

            while len(orig_to_tok_index) < start_pos:
                if orig_to_tok_index:
                    orig_to_tok_index.append(orig_to_tok_index[-1])
                else:
                    orig_to_tok_index.append(0)
            for j in range(start_pos, end_pos):
                orig_to_tok_index.append(i)

            start_pos = end_pos
        return tok_to_orig_index, orig_to_tok_index

    def format_result(self, resp_json, text, orig_to_tok_index, tok_to_orig_index, length):
        result_list = list()
        text = tokenization.convert_to_unicode(text)
        if "predictions" in resp_json:
            for index, obj in enumerate(resp_json["predictions"]):
                start_logits = obj["start_logits"]
                end_logits = obj["end_logits"]
                hypo_probabilities = obj["probabilities"]
                null_score = start_logits[0] + end_logits[0]
                max_score = -1e5
                max_start = 0
                max_end = 0
                for i in range(1, length-2):
                    start_score = start_logits[i]
                    for j in range(i+1, length-1):
                        end_score = end_logits[j]
                        cur_score = start_score + end_score
                        if cur_score > max_score:
                            max_score = cur_score
                            max_start = i
                            max_end = j
                final_score = null_score - max_score
                if final_score < self.THRESHOLD:
                    is_overtalk = False
                    start_idx = max_start
                    end_idx = max_end
                    orig_start = tok_to_orig_index[start_idx - 1]
                    orig_end = tok_to_orig_index[end_idx - 1]
                    event_part = text[orig_start: orig_end + 1]
                else:
                    is_overtalk = True
                    start_idx = 0
                    end_idx = 0
                    event_part = ""
                result_list.append({"is_overtalk": is_overtalk, "overtalk_score": final_score, "event": event_part, "tense_prob": hypo_probabilities})
        return result_list


if __name__ == "__main__":
    m = NNOvertalkDetecter()
    while True:
        text = input("input:")
        print(m.predict_doc(text))

