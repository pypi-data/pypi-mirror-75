import logging
import os

import jieba

from .abstract_tokenizer import VocabBasedTokenizer


class JiebaTokenizer(VocabBasedTokenizer):

    def __init__(self,
                 vocab_file=None,
                 user_dict_files=None,
                 intervener=None,
                 **kwargs):
        super(JiebaTokenizer, self).__init__(
            vocab_file=vocab_file,
            intervener=intervener,
            **kwargs)
        jieba.initialize()
        self._load_jieba_user_dict(user_dict_files)

    def tokenize(self, inputs, mode='accurate', hmm=True, **kwargs):
        if mode == 'full':
            tokens = [t for t in jieba.cut(inputs, cut_all=True, HMM=hmm)]
        elif mode == 'search':
            tokens = [t for t in jieba.cut_for_search(inputs, HMM=hmm)]
        else:
            tokens = [t for t in jieba.cut(inputs, cut_all=False, HMM=hmm)]
        if self.intervener:
            tokens = self.intervener.intervene(tokens, **kwargs)
        return tokens

    @staticmethod
    def _load_jieba_user_dict(dict_files):
        if not dict_files:
            logging.info('Argument `user_dict_files` is empty or None. Skipped.')
            return
        for f in dict_files:
            if not os.path.exists(f):
                logging.warning('Load user dict file: {} failed, files does not exist.'.format(f))
                continue
            with open(f, mode='rt', encoding='utf8') as fin:
                jieba.load_userdict(fin)
            logging.info('Load user dict file: {} successfully.'.format(f))
