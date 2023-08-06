__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import os
from typing import Optional
import numpy as np

from .. import BaseEncoder
from ..frameworks import BaseTextTFEncoder, BaseTextTorchEncoder
from ..helper import reduce_mean, reduce_max, reduce_min, reduce_cls
from ...decorators import batching, as_ndarray
from jina.logging.base import get_logger

logger = get_logger("transformer_encoder")


def auto_reduce(model_outputs, mask_2d, model_name):
    """
    Automatically creates a sentence embedding from its token embeddings.
        * For BERT-like models (BERT, RoBERTa, DistillBERT, Electra ...) uses embedding of first token
        * For XLM and XLNet models uses embedding of last token
        * Assumes that other models are language-model like and uses embedding of last token
    """
    if "bert" in model_name or "electra" in model_name:
        return reduce_cls(model_outputs, mask_2d)
    if "xlnet" in model_name:
        return reduce_cls(model_outputs, mask_2d, cls_pos="tail")
    logger.warning("Using embedding of a last token as a sequence embedding. "
                   "If that's not desirable, change `pooling_strategy`")
    return reduce_cls(model_outputs, mask_2d, cls_pos="tail")


class BaseTransformerEncoder(BaseEncoder):
    """
    :class:`TransformerTextEncoder` encodes data from an array of string in size `B` into an ndarray in size `B x D`.
    """

    def __init__(self,
                 pretrained_model_name_or_path: str = 'bert-base-uncased',
                 pooling_strategy: str = 'auto',
                 max_length: Optional[int] = None,
                 truncation_strategy: str = 'longest_first',
                 model_save_path: Optional[str] = None,
                 *args, **kwargs):
        """
        :param pretrained_model_name_or_path: Either:
            - a string with the `shortcut name` of a pre-trained model to load from cache or download, e.g.: ``bert-base-uncased``.
            - a string with the `identifier name` of a pre-trained model that was user-uploaded to Hugging Face S3, e.g.: ``dbmdz/bert-base-german-cased``.
            - a path to a `directory` containing model weights saved using :func:`~transformers.PreTrainedModel.save_pretrained`, e.g.: ``./my_model_directory/``.
            - a path or url to a `tensorflow index checkpoint file` (e.g. `./tf_model/model.ckpt.index`). In this case, ``from_tf`` should be set to True and a configuration object should be provided as ``config`` argument.
            This loading path is slower than converting the TensorFlow
            checkpoint in a PyTorch model using the provided conversion scripts and loading the PyTorch model afterwards.
        :param pooling_strategy: the strategy to merge the word embeddings into the chunk embedding. Supported
            strategies include 'auto', 'cls', 'mean', 'max', 'min'.
        :param max_length: the max length to truncate the tokenized sequences to.
        :param model_save_path: the path of the encoder model. If a valid path is given, the encoder will be saved to the given path
        :param truncation_strategy: select truncation strategy. Supported values
            * `True` or `'longest_first'` (default): truncate to a max length specified in `max_length` or to the max acceptable input length for the model if no length is provided (`max_length=None`).
            * `'only_first'`:  This will only truncate the first sequence of a pair if a pair of sequences (or a batch of pairs) is provided
            * `'only_second'`: This will only truncate the second sequence of a pair if a pair of sequences (or a batch of pairs) is provided
            * `False` or `'do_not_truncate'`: No truncation (i.e. can output batch with sequences length greater than the model max admissible input size)

        ..warning::
            `model_save_path` should be relative to executor's workspace
        """
        super().__init__(*args, **kwargs)
        self.pretrained_model_name_or_path = pretrained_model_name_or_path
        self.pooling_strategy = pooling_strategy
        self.max_length = max_length
        self.model_save_path = model_save_path
        self.truncation_strategy = truncation_strategy

    @batching
    @as_ndarray
    def encode(self, data: 'np.ndarray', *args, **kwargs) -> 'np.ndarray':
        """
        :param data: a 1d array of string type in size `B`
        :return: an ndarray in size `B x D`
        """
        try:
            ids_info = self.tokenizer.batch_encode_plus(data,
                                                        max_length=self.max_length,
                                                        truncation=self.truncation_strategy,
                                                        padding=True)
        except ValueError:
            self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            self.model.resize_token_embeddings(len(self.tokenizer))
            ids_info = self.tokenizer.batch_encode_plus(data, max_length=self.max_length, padding=True)
        token_ids_batch = self.array2tensor(ids_info['input_ids'])
        mask_ids_batch = self.array2tensor(ids_info['attention_mask'])
        with self.session():
            seq_output, *extra_output = self.model(token_ids_batch, attention_mask=mask_ids_batch)
            _mask_ids_batch = self.tensor2array(mask_ids_batch)
            _seq_output = self.tensor2array(seq_output)
            if self.pooling_strategy == 'auto':
                output = auto_reduce(_seq_output, _mask_ids_batch, self.model.base_model_prefix)
            elif self.pooling_strategy == 'cls':
                if hasattr(self._tokenizer, 'cls_token') and len(extra_output) > 0:
                    output = self.tensor2array(extra_output[0])
                else:
                    output = reduce_cls(_seq_output, _mask_ids_batch, self.cls_pos)
            elif self.pooling_strategy == 'mean':
                output = reduce_mean(_seq_output, _mask_ids_batch)
            elif self.pooling_strategy == 'max':
                output = reduce_max(_seq_output, _mask_ids_batch)
            elif self.pooling_strategy == 'min':
                output = reduce_min(_seq_output, _mask_ids_batch)
            else:
                self.logger.error(f'pooling strategy not found: {self.pooling_strategy}')
                raise NotImplementedError
        return output

    def __getstate__(self):
        if self.model_save_path:
            if not os.path.exists(self.model_abspath):
                self.logger.info(f'create folder for saving transformer models: {self.model_abspath}')
                os.mkdir(self.model_abspath)
            self.model.save_pretrained(self.model_abspath)
            self.tokenizer.save_pretrained(self.model_abspath)
        return super().__getstate__()

    def post_init(self):
        self._model = None
        self._tensor_func = None
        self._sess_func = None
        self._tokenizer = self.get_tokenizer()

    def array2tensor(self, array):
        return self.tensor_func(array)

    def tensor2array(self, tensor):
        return tensor.numpy()

    @property
    def model_abspath(self) -> str:
        """Get the file path of the encoder model storage
        """
        return self.get_file_from_workspace(self.model_save_path)

    @property
    def model(self):
        if self._model is None:
            self._model = self.get_model()
        return self._model

    @property
    def session(self):
        if self._sess_func is None:
            self._sess_func = self.get_session()
        return self._sess_func

    @property
    def tensor_func(self):
        if self._tensor_func is None:
            self._tensor_func = self.get_tensor_func()
        return self._tensor_func

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            self._tokenizer = self.get_tokenizer()
        return self._tokenizer

    def get_tokenizer(self):
        from transformers import AutoTokenizer
        _tokenizer = AutoTokenizer.from_pretrained(self.pretrained_model_name_or_path)
        return _tokenizer

    def get_model(self):
        raise NotImplementedError

    def get_session(self):
        raise NotImplementedError

    def get_tensor_func(self):
        raise NotImplementedError


class TransformerTFEncoder(BaseTransformerEncoder, BaseTextTFEncoder):
    """
    Internally, TransformerTFEncoder wraps the tensorflow-version of transformers from huggingface.
    """

    def get_model(self):
        from transformers import TFAutoModelForPreTraining
        _model = TFAutoModelForPreTraining.from_pretrained(self.pretrained_model_name_or_path)
        return _model

    def get_session(self):
        import tensorflow as tf
        return tf.GradientTape

    def get_tensor_func(self):
        self.to_device()
        import tensorflow as tf
        return tf.constant


class TransformerTorchEncoder(BaseTransformerEncoder, BaseTextTorchEncoder):
    """
    Internally, TransformerTorchEncoder wraps the pytorch-version of transformers from huggingface.
    """

    def get_model(self):
        from transformers import AutoModelForPreTraining
        _model = AutoModelForPreTraining.from_pretrained(self.pretrained_model_name_or_path)
        self.to_device(_model)
        return _model

    def get_session(self):
        import torch
        return torch.no_grad

    def get_tensor_func(self):
        import torch
        return torch.tensor

    def array2tensor(self, array):
        tensor = super().array2tensor(array)
        return tensor.cuda() if self.on_gpu else tensor

    def tensor2array(self, tensor):
        return tensor.cpu().numpy() if self.on_gpu else tensor.numpy()
