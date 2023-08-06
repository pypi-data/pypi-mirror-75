import abc
import logging
import os


class AbstractIntervener(abc.ABC):

    def intervene(self, tokens, **kwargs):
        raise NotImplementedError()

    def add_split_token(self, from_token, to_token, **kwargs):
        raise NotImplementedError()

    def remove_split_token(self, key):
        raise NotImplementedError()

    def add_combine_token(self, token, **kwargs):
        raise NotImplementedError()

    def remove_combine_token(self, token):
        raise NotImplementedError()


class DefaultIntervener(AbstractIntervener):

    def __init__(self, split_vocabs=None, combine_vocabs=None, sep='\t'):
        self.split_vocabs = split_vocabs or []
        self.combine_vocabs = combine_vocabs or []
        self.sep = sep
        self.split_map = {}
        self._load_split_vocabs()
        self.combine_set = set()
        self._load_combine_set()

    def intervene(self, tokens, **kwargs):
        tokens = self._split_tokens(tokens)
        tokens = self._combine_tokens(tokens)
        return tokens

    def add_split_token(self, from_token, to_token, **kwargs):
        tokens = ''.join(to_token.split())
        if len(tokens) != len(from_token):
            return
        if not from_token:
            return
        self.split_map[from_token] = to_token

    def remove_split_token(self, key):
        if key not in self.split_map:
            return
        del self.split_map[key]

    def add_combine_token(self, token, **kwargs):
        if not token:
            return
        self.combine_set.add(token)

    def remove_combine_token(self, token):
        if token not in self.combine_set:
            return
        self.combine_set.remove(token)

    def _split_tokens(self, tokens):
        results = []
        for token in tokens:
            if token in self.split_map:
                values = self.split_map.get(token)
                # split by space
                for v in values.split():
                    results.append(v)
            else:
                results.append(token)
        return results

    def _combine_tokens(self, tokens):
        if not tokens:
            return []
        results, stack = [], []
        while tokens:
            if not stack:
                stack.append(tokens.pop(0))
                continue
            cur = tokens.pop(0)
            prev = stack.pop()
            combined = prev + cur
            if combined in self.combine_set:
                stack.append(combined)
                continue
            while stack:
                results.append(stack.pop(0))
            results.append(prev)
            stack.append(cur)
        while stack:
            results.append(stack.pop(0))
        return results

    def _load_split_vocabs(self):
        for f in self.split_vocabs:
            if not os.path.exists(f):
                continue
            with open(f, mode='rt', encoding='utf8') as fin:
                for line in fin:
                    line = line.rstrip('\n').strip()
                    parts = line.split(self.sep)
                    if len(parts) != 2:
                        continue
                    from_token, to_token = parts[0].strip(), parts[1].strip()
                    self.split_map[from_token] = to_token

    def _load_combine_set(self):
        for f in self.combine_vocabs:
            if not os.path.exists(f):
                continue
            with open(f, mode='rt', encoding='utf8') as fin:
                for line in fin:
                    line = line.rstrip('\n').strip()
                    if not line:
                        continue
                    self.combine_set.add(line)


class AbstractTokenizer(abc.ABC):

    def __init__(self, intervener: AbstractIntervener = None, **kwargs):
        self.intervener = intervener

    def tokenize(self, inputs, **kwargs):
        raise NotImplementedError()


class VocabBasedTokenizer(AbstractTokenizer):

    def __init__(self, vocab_file, intervener=None, **kwargs):
        """Init vocab based tokenizer.

        Args:
            vocab_file: Python str, vocab file used to index word to ids.
            intervener: Instance of `AbstractIntervener`, used to intervene tokenization results.
        """
        super(VocabBasedTokenizer, self).__init__(intervener=intervener, **kwargs)
        self.vocab_file = vocab_file

        self._special_tokens = []
        for k, v in kwargs.items():
            if str(k).endswith('_token') and v is not None:
                self._special_tokens.append((k, v))

        self.vocab = self._build_vocab(vocab_file)
        self.reverse_vocab = self._reverse_vocab()

        for k, v in self._special_tokens:
            _id = str(k.split('_')[0]) + '_id'
            setattr(self, k, v)
            setattr(self, _id, self.vocab[v])

    def _build_vocab(self, file):
        if not file:
            logging.warning('vocab_file is empty or None.')
            return {}
        words = []
        with open(file, mode='rt', encoding='utf8') as fin:
            for line in fin:
                line = line.strip('\n').strip()
                if not line:
                    continue
                word = line.strip()
                words.append(word)

        vocab = set(words)
        special_tokens = [v for _, v in sorted(self._special_tokens, key=lambda x: x[0])]
        for t in special_tokens:
            if t not in vocab:
                words.append(t)

        d = {}
        for i in range(len(words)):
            d[words[i]] = i
        return d

    def _reverse_vocab(self):
        reverse_vocabs = {}
        for k, v in self.vocab.items():
            reverse_vocabs[v] = k
        return reverse_vocabs

    @property
    def vocab_size(self):
        return len(self.vocab)

    def special_tokens(self):
        return self._special_tokens

    def tokenize(self, inputs, **kwargs):
        raise NotImplementedError()

    def tokens2ids(self, tokens, add_bos=False, add_eos=False, **kwargs):
        ids = [self.vocab.get(t, self.unk_id) for t in tokens]
        if add_bos:
            ids = [self.bos_id] + ids
        if add_eos:
            ids = ids + [self.eos_id]
        return ids

    def ids2tokens(self, ids, drop_bos=False, drop_eos=False, **kwargs):
        tokens = [self.reverse_vocab.get(t, self.unk_token) for t in ids]
        if drop_bos and tokens[0] == self.bos_token:
            tokens = tokens[1:]
        if drop_eos and tokens[-1] == self.eos_token:
            tokens = tokens[:-1]
        return tokens

    def encode(self, inputs, add_bos=False, add_eos=False, **kwargs):
        tokens = self.tokenize(inputs, **kwargs)
        return self.tokens2ids(tokens, add_bos=add_bos, add_eos=add_eos, **kwargs)

    def decode(self, inputs, drop_bos=True, drop_eos=True, **kwargs):
        ids = [self.reverse_vocab.get(t, self.unk_token) for t in inputs]
        if not ids:
            return []
        return self.ids2tokens(ids, drop_bos=drop_bos, drop_eos=drop_eos, **kwargs)
