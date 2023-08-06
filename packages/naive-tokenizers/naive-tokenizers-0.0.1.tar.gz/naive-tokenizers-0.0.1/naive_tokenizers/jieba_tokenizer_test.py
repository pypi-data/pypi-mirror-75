import unittest

import jieba

from .jieba_tokenizer import JiebaTokenizer
from .abstract_tokenizer import DefaultIntervener


class JiebaTokenizerTest(unittest.TestCase):

    def testTokenize(self):
        vocab_file = 'testdata/vocab_chinese.txt'
        user_dict_files = [
            'data/jieba/hello.txt',
            'naivenlp/tokenizers/data/dict.txt',
        ]
        intervener = DefaultIntervener()
        tokenizer = JiebaTokenizer(
            vocab_file=vocab_file,
            user_dict_files=user_dict_files,
            intervener=intervener,
            pad_token='[PAD]',
            unk_token='[UNK]',
            bos_token='<S>',
            eos_token='<T>',
            cls_token='[CLS]',
            sep_token='[SEP]',
            mask_token='[MASK]',
        )

        self.assertEqual(0, tokenizer.pad_id)
        self.assertEqual(100, tokenizer.unk_id)
        self.assertEqual(104, tokenizer.bos_id)
        self.assertEqual(105, tokenizer.eos_id)
        self.assertEqual(101, tokenizer.cls_id)
        self.assertEqual(102, tokenizer.sep_id)
        self.assertEqual(103, tokenizer.mask_id)

        sentences = [
            '我在上海工作',
            '我来到北京清华大学',
            '乒乓球拍卖完了',
            '中国科学技术大学',
        ]

        for sent in sentences:
            self.assertEqual(
                [t for t in jieba.cut(sent, cut_all=False, HMM=True)],
                tokenizer.tokenize(sent, mode='accurate', hmm=True))
            self.assertEqual(
                [t for t in jieba.cut(sent, cut_all=False, HMM=False)],
                tokenizer.tokenize(sent, mode='accurate', hmm=False))
            self.assertEqual(
                [t for t in jieba.cut(sent, cut_all=True, HMM=True)],
                tokenizer.tokenize(sent, mode='full', hmm=True))
            self.assertEqual(
                [t for t in jieba.cut(sent, cut_all=True, HMM=False)],
                tokenizer.tokenize(sent, mode='full', hmm=True))
            self.assertEqual(
                [t for t in jieba.cut_for_search(sent, HMM=True)],
                tokenizer.tokenize(sent, mode='search', hmm=True))
            self.assertEqual(
                [t for t in jieba.cut_for_search(sent, HMM=False)],
                tokenizer.tokenize(sent, mode='search', hmm=False))

        tokens = tokenizer.tokenize('高级javadeveloper')
        self.assertListEqual(['高级', 'javadeveloper'], tokens)

        intervener.add_split_token('javadeveloper', 'java developer')
        tokens = tokenizer.tokenize('高级javadeveloper')
        self.assertListEqual(['高级', 'java', 'developer'], tokens)

        intervener.add_combine_token('javadeveloper')
        tokens = tokenizer.tokenize('高级javadeveloper')
        self.assertListEqual(['高级', 'javadeveloper'], tokens)

        intervener.remove_combine_token('javadeveloper')
        tokens = tokenizer.tokenize('高级javadeveloper')
        self.assertListEqual(['高级', 'java', 'developer'], tokens)

        intervener.remove_split_token('javadeveloper')
        tokens = tokenizer.tokenize('高级javadeveloper')
        self.assertListEqual(['高级', 'javadeveloper'], tokens)


if __name__ == "__main__":
    unittest.main()
