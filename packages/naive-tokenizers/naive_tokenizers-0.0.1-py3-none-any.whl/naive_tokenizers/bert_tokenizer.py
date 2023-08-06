from .transformer_tokenizer import TransformerTokenizer


class BertTokenizer(TransformerTokenizer):

    def __init__(self, vocab_file, cls_token='[CLS]', sep_token='[SEP]', mask_token='[MASK]', **kwargs):
        super().__init__(vocab_file, cls_token=cls_token, sep_token=sep_token, mask_token=mask_token, **kwargs)
