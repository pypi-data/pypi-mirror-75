import collections
import json
import logging
import pydoc
import operator

from typing import List, Dict, Optional, Any, Union

from sklearn.preprocessing import MultiLabelBinarizer

import numpy as np
import six


def pad_sequences(sequences, maxlen=None, dtype='int32',
                  padding='pre', truncating='pre', value=0.):
    """Pads sequences to the same length.

    This function transforms a list of
    `num_samples` sequences (lists of integers)
    into a 2D Numpy array of shape `(num_samples, num_timesteps)`.
    `num_timesteps` is either the `maxlen` argument if provided,
    or the length of the longest sequence otherwise.

    Sequences that are shorter than `num_timesteps`
    are padded with `value` at the beginning or the end
    if padding='post.

    Sequences longer than `num_timesteps` are truncated
    so that they fit the desired length.
    The position where padding or truncation happens is determined by
    the arguments `padding` and `truncating`, respectively.

    Pre-padding is the default.

    # Arguments
        sequences: List of lists, where each element is a sequence.
        maxlen: Int, maximum length of all sequences.
        dtype: Type of the output sequences.
            To pad sequences with variable length strings, you can use `object`.
        padding: String, 'pre' or 'post':
            pad either before or after each sequence.
        truncating: String, 'pre' or 'post':
            remove values from sequences larger than
            `maxlen`, either at the beginning or at the end of the sequences.
        value: Float or String, padding value.

    # Returns
        x: Numpy array with shape `(len(sequences), maxlen)`

    # Raises
        ValueError: In case of invalid values for `truncating` or `padding`,
            or in case of invalid shape for a `sequences` entry.
    """
    if not hasattr(sequences, '__len__'):
        raise ValueError('`sequences` must be iterable.')
    num_samples = len(sequences)

    lengths = []
    sample_shape = ()
    flag = True

    # take the sample shape from the first non empty sequence
    # checking for consistency in the main loop below.

    for x in sequences:
        try:
            lengths.append(len(x))
            if flag and len(x):
                sample_shape = np.asarray(x).shape[1:]
                flag = False
        except TypeError:
            raise ValueError('`sequences` must be a list of iterables. '
                             'Found non-iterable: ' + str(x))

    if maxlen is None:
        maxlen = np.max(lengths)

    is_dtype_str = np.issubdtype(dtype, np.str_) or np.issubdtype(dtype, np.unicode_)
    if isinstance(value, six.string_types) and dtype != object and not is_dtype_str:
        raise ValueError("`dtype` {} is not compatible with `value`'s type: {}\n"
                         "You should set `dtype=object` for variable length strings."
                         .format(dtype, type(value)))

    x = np.full((num_samples, maxlen) + sample_shape, value, dtype=dtype)
    for idx, s in enumerate(sequences):
        if not len(s):
            continue  # empty list/array was found
        if truncating == 'pre':
            trunc = s[-maxlen:]
        elif truncating == 'post':
            trunc = s[:maxlen]
        else:
            raise ValueError('Truncating type "%s" '
                             'not understood' % truncating)

        # check `trunc` has expected shape
        trunc = np.asarray(trunc, dtype=dtype)
        if trunc.shape[1:] != sample_shape:
            raise ValueError('Shape of sample %s of sequence at position %s '
                             'is different from expected shape %s' %
                             (trunc.shape[1:], idx, sample_shape))

        if padding == 'post':
            x[idx, :len(trunc)] = trunc
        elif padding == 'pre':
            x[idx, -len(trunc):] = trunc
        else:
            raise ValueError('Padding type "%s" not understood' % padding)
    return x


def get_list_subset(target: List, index_list: List[int]) -> List:
    return [target[i] for i in index_list if i < len(target)]




class BaseProcessor(object):
    """
    Corpus Pre Processor class
    """

    def __init__(self, **kwargs):
        self.token2idx: Dict[str, int] = kwargs.get('token2idx', {})
        self.idx2token: Dict[int, str] = dict([(v, k) for (k, v) in self.token2idx.items()])

        self.token2count: Dict = {}

        self.label2idx: Dict[str, int] = kwargs.get('label2idx', {})
        self.idx2label: Dict[int, str] = dict([(v, k) for (k, v) in self.label2idx.items()])

        self.token_pad: str = kwargs.get('token_pad', '<PAD>')
        self.token_unk: str = kwargs.get('token_unk', '<UNK>')
        self.token_bos: str = kwargs.get('token_bos', '<BOS>')
        self.token_eos: str = kwargs.get('token_eos', '<EOS>')

        self.dataset_info: Dict[str, Any] = kwargs.get('dataset_info', {})

        self.add_bos_eos: bool = kwargs.get('add_bos_eos', False)

        self.sequence_length = kwargs.get('sequence_length', None)

        self.min_count = kwargs.get('min_count', 3)

    def info(self):
        return {
            'class_name': self.__class__.__name__,
            'config': {
                'label2idx': self.label2idx,
                'token2idx': self.token2idx,
                'token_pad': self.token_pad,
                'token_unk': self.token_unk,
                'token_bos': self.token_bos,
                'token_eos': self.token_eos,
                'dataset_info': self.dataset_info,
                'add_bos_eos': self.add_bos_eos,
                'sequence_length': self.sequence_length
            },
            'module': self.__class__.__module__,
        }

    def analyze_corpus(self,
                       corpus: Union[List[List[str]]],
                       labels: Union[List[List[str]], List[str]],
                       force: bool = False):
        rec_len = sorted([len(seq) for seq in corpus])[int(0.95 * len(corpus))]
        self.dataset_info['RECOMMEND_LEN'] = rec_len

        if len(self.token2idx) == 0 or force:
            self._build_token_dict(corpus, self.min_count)
        if len(self.label2idx) == 0 or force:
            self._build_label_dict(labels)

    def _build_token_dict(self, corpus: List[List[str]], min_count: int = 3):
        """
        Build token index dictionary using corpus

        Args:
            corpus: List of tokenized sentences, like ``[['I', 'love', 'tf'], ...]``
            min_count:
        """
        token2idx = {
            self.token_pad: 0,
            self.token_unk: 1,
            self.token_bos: 2,
            self.token_eos: 3
        }

        token2count = {}
        for sentence in corpus:
            for token in sentence:
                count = token2count.get(token, 0)
                token2count[token] = count + 1
        self.token2count = token2count

        # 按照词频降序排序
        sorted_token2count = sorted(token2count.items(),
                                    key=operator.itemgetter(1),
                                    reverse=True)
        token2count = collections.OrderedDict(sorted_token2count)

        for token, token_count in token2count.items():
            if token not in token2idx and token_count >= min_count:
                token2idx[token] = len(token2idx)

        self.token2idx = token2idx
        self.idx2token = dict([(value, key)
                               for key, value in self.token2idx.items()])
        logging.debug(f"build token2idx dict finished, contains {len(self.token2idx)} tokens.")
        self.dataset_info['token_count'] = len(self.token2idx)

    def _build_label_dict(self, corpus: Union[List[List[str]], List[str]]):
        raise NotImplementedError

    def process_x_dataset(self,
                          data: List[List[str]],
                          max_len: Optional[int] = None,
                          subset: Optional[List[int]] = None) -> np.ndarray:
        if max_len is None:
            max_len = self.sequence_length
        if subset is not None:
            target = get_list_subset(data, subset)
        else:
            target = data
        numerized_samples = self.numerize_token_sequences(target)

        return pad_sequences(numerized_samples, max_len, padding='post', truncating='post')

    def process_y_dataset(self,
                          data: Union[List[List[str]], List[str]],
                          max_len: Optional[int],
                          subset: Optional[List[int]] = None) -> np.ndarray:
        raise NotImplementedError

    def numerize_token_sequences(self,
                                 sequences: List[List[str]]):
        raise NotImplementedError

    def numerize_label_sequences(self,
                                 sequences: List[List[str]]) -> List[List[int]]:
        raise NotImplementedError

    def reverse_numerize_label_sequences(self, sequence, **kwargs):
        raise NotImplementedError

    def __repr__(self):
        return f"<{self.__class__}>"

    def __str__(self):
        return self.__repr__()




class LabelingProcessor(object):

    def __init__(self, **kwargs):
        """
        Corpus Pre Processor class
        """
        self.token2idx: Dict[str, int] = kwargs.get('token2idx', {})
        self.idx2token: Dict[int, str] = dict([(v, k) for (k, v) in self.token2idx.items()])

        self.token2count: Dict = {}

        self.label2idx: Dict[str, int] = kwargs.get('label2idx', {})
        self.idx2label: Dict[int, str] = dict([(v, k) for (k, v) in self.label2idx.items()])

        self.token_pad: str = kwargs.get('token_pad', '<PAD>')
        self.token_unk: str = kwargs.get('token_unk', '<UNK>')
        self.token_bos: str = kwargs.get('token_bos', '<BOS>')
        self.token_eos: str = kwargs.get('token_eos', '<EOS>')

        self.dataset_info: Dict[str, Any] = kwargs.get('dataset_info', {})

        self.add_bos_eos: bool = kwargs.get('add_bos_eos', False)

        self.sequence_length = kwargs.get('sequence_length', None)

        self.min_count = kwargs.get('min_count', 3)

    def _build_label_dict(self, label_list: List[List[str]]):
        """
        Build label2idx dict for sequence labeling task

        Args:
            label_list: corpus label list
        """
        label2idx: Dict[str: int] = {
            self.token_pad: 0
        }

        token2count = {}

        for sequence in label_list:
            for label in sequence:
                count = token2count.get(label, 0)
                token2count[label] = count + 1

        sorted_token2count = sorted(token2count.items(),
                                    key=operator.itemgetter(1),
                                    reverse=True)
        token2count = collections.OrderedDict(sorted_token2count)

        for token in token2count.keys():
            if token not in label2idx:
                label2idx[token] = len(label2idx)

        self.label2idx = label2idx
        self.idx2label = dict([(value, key)
                               for key, value in self.label2idx.items()])
        logging.debug(f"build label2idx dict finished, contains {len(self.label2idx)} labels.")

    def numerize_token_sequences(self,
                                 sequences: List[List[str]]):

        result = []
        for seq in sequences:
            if self.add_bos_eos:
                seq = [self.token_bos] + seq + [self.token_eos]
            unk_index = self.token2idx[self.token_unk]
            result.append([self.token2idx.get(token, unk_index) for token in seq])
        return result

    def numerize_label_sequences(self,
                                 sequences: List[List[str]]) -> List[List[int]]:
        result = []
        for seq in sequences:
            if self.add_bos_eos:
                seq = [self.token_pad] + seq + [self.token_pad]
            result.append([self.label2idx[label] for label in seq])
        return result

    def reverse_numerize_label_sequences(self,
                                         sequences,
                                         lengths=None):
        result = []

        for index, seq in enumerate(sequences):
            labels = []
            if self.add_bos_eos:
                seq = seq[1:]
            for idx in seq:
                labels.append(self.idx2label[idx])
            if lengths is not None:
                labels = labels[:lengths[index]]
            result.append(labels)
        return result

    def process_x_dataset(self,
                          data: List[List[str]],
                          max_len: Optional[int] = None,
                          subset: Optional[List[int]] = None) -> np.ndarray:
        if max_len is None:
            max_len = self.sequence_length
        if subset is not None:
            target = get_list_subset(data, subset)
        else:
            target = data
        numerized_samples = self.numerize_token_sequences(target)

        return pad_sequences(numerized_samples, max_len, padding='post', truncating='post')


class ClassificationProcessor(BaseProcessor):
    """
    Corpus Pre Processor class
    """

    def __init__(self, multi_label=False, **kwargs):
        super(ClassificationProcessor, self).__init__(**kwargs)
        self.multi_label = multi_label
        if self.label2idx:
            self.multi_label_binarizer: MultiLabelBinarizer = MultiLabelBinarizer(classes=list(self.label2idx.keys()))
            self.multi_label_binarizer.fit([])
        else:
            self.multi_label_binarizer: MultiLabelBinarizer = None

    def info(self):
        info = super(ClassificationProcessor, self).info()
        info['task'] = "classification"
        info['config']['multi_label'] = self.multi_label
        return info

    def _build_label_dict(self,
                          labels: List[str]):
        if self.multi_label:
            label_set = set()
            for i in labels:
                label_set = label_set.union(list(i))
        else:
            label_set = set(labels)
        self.label2idx = {}
        for idx, label in enumerate(sorted(label_set)):
            self.label2idx[label] = len(self.label2idx)

        self.idx2label = dict([(value, key) for key, value in self.label2idx.items()])
        self.dataset_info['label_count'] = len(self.label2idx)
        self.multi_label_binarizer = MultiLabelBinarizer(classes=list(self.label2idx.keys()))


    def numerize_token_sequences(self,
                                 sequences: List[List[str]]):
        result = []
        for seq in sequences:
            if self.add_bos_eos:
                seq = [self.token_bos] + seq + [self.token_eos]
            unk_index = self.token2idx[self.token_unk]
            result.append([self.token2idx.get(token, unk_index) for token in seq])
        return result

    def numerize_label_sequences(self,
                                 sequences: List[str]) -> List[int]:
        """
        Convert label sequence to label-index sequence
        ``['O', 'O', 'B-ORG'] -> [0, 0, 2]``

        Args:
            sequences: label sequence, list of str

        Returns:
            label-index sequence, list of int
        """
        return [self.label2idx[label] for label in sequences]

    def reverse_numerize_label_sequences(self, sequences, **kwargs):
        if self.multi_label:
            return self.multi_label_binarizer.inverse_transform(sequences)
        else:
            return [self.idx2label[label] for label in sequences]


def load_processor(model_info_path: str) -> LabelingProcessor:
    with open(model_info_path, 'r') as f:
        model_info = json.load(f)

    processor_info = model_info['embedding']['processor']
    # processor_class = pydoc.locate(f"{processor_info['module']}.{processor_info['class_name']}")
    processor: LabelingProcessor = LabelingProcessor(**processor_info['config'])
    return processor


def load_clf_processor(model_info_path: str) -> ClassificationProcessor:
    with open(model_info_path, 'r') as f:
        model_info = json.load(f)

    processor_info = model_info['embedding']['processor']
    # processor_class = pydoc.locate(f"{processor_info['module']}.{processor_info['class_name']}")
    processor: ClassificationProcessor = ClassificationProcessor(**processor_info['config'])
    return processor

