import re
from typing import List, Union

import numpy as np
import torch
from torch import Tensor

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace


class BaseTextEncoder:
    def __init__(self, args, vocab: List[int] = None):
        self.tokenizer = Tokenizer(BPE())
        self.tokenizer.pre_tokenizer = Whitespace()
        if args["train_mode"]:
            trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])
            self.tokenizer.train_from_iterator(vocab, trainer=trainer)
            self.tokenizer.save(args["save_path"])
        else:
            self.tokenizer = self.tokenizer.from_file(args["load_path"])

    def encode(self, text: str) -> Tensor:
        return torch.Tensor(self.tokenizer.encode(text).ids)

    def decode(self, vector: Union[Tensor, np.ndarray, List[int]]) -> str:
        raise self.tokenizer.decode(vector)

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, item: int) -> str:
        raise NotImplementedError

    @staticmethod
    def normalize_text(text: str):
        text = text.lower()
        text = re.sub(r"[^а-я ]", "", text)
        return text
