import os
import requests

from hrtps.utils import tokenization


class MeanfulDetecter(object):

    def __init__(self):
        model_mess_path = os.path.dirname(__file__)
        vocab_file = os.path.join(model_mess_path, "..", "data", "meanful", "vocab.txt")
        self.pre_url = r"http://model.ai-open.hrtps.com/v1/models/meanless:predict"
        self.tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file, do_lower_case=False)
        self.max_seq_length = 128

    def trans_tensor(self, texts):
        data_list = []
        for query in texts:
            tokens_a = self.tokenizer.tokenize(query)
            tokens_b = None
            if len(tokens_a) > self.max_seq_length - 2:
                tokens_a = tokens_a[0:(self.max_seq_length - 2)]

            tokens = []
            tokens.append('[CLS]')
            tokens += tokens_a
            tokens.append('[SEP]')

            segment_ids = [0 for _ in tokens]
            input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
            input_mask = [1] * len(input_ids)

            while len(input_ids) < self.max_seq_length:
                input_ids.append(0)
                input_mask.append(0)
                segment_ids.append(0)

            feature = {"input_ids": input_ids, "input_mask": input_mask, "segment_ids": segment_ids, "label_ids": 0}
            data_list.append(feature)

        tensor_data = {"instances": data_list}
        return tensor_data

    def predict_doc(self, text1: str):
        tensor_data = self.trans_tensor([text1])
        resp = requests.post(self.pre_url, json=tensor_data)
        resp_json = resp.json()
        return resp_json


if __name__ == "__main__":
    m = MeanfulDetecter()
    while True:
        text = input("input:")
        print(m.predict_doc(text))
    # print(request_from_raw_text(text, 'meanless'))
