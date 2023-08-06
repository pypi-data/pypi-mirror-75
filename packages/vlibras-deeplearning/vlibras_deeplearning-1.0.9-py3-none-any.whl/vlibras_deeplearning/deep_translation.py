import os

import fairseq

from . import model_utils

class DeepTranslation():

    def __init__(self):
        PWD = os.path.dirname(os.path.realpath(__file__))

        # prepare model files (check version, download, unzip etc)
        model_utils.prepare_model()

        # load fairseq model
        self._arch = fairseq.models.lightconv.LightConvModel
        self._model = self._arch.from_pretrained(
            os.path.join(PWD, 'model', 'Checkpoints'),
            checkpoint_file='checkpoint_best.pt',
            data_name_or_path=os.path.join(PWD, 'model', 'BIN'),
            bpe='subword_nmt',
            bpe_codes=os.path.join(PWD, 'model', 'BPE', 'bpe_code')
        )

        # set model to evaluation mode
        self._model.eval()


    def translate(self, gr):
        # break up sentences so we can feed them individually to the model
        tokenized_sentence = [g for g in gr
            .replace('[PONTO]', '[PONTO]\n')
            .replace('[INTERROGAÇÃO]', '[INTERROGAÇÃO]\n')
            .replace('[EXCLAMAÇÃO]', '[EXCLAMAÇÃO]\n')
            .split('\n') if g.strip()
        ]

        translated_sentence = []
        for token in tokenized_sentence:
            translated_sentence.append(self._model.translate(token))

        return ' '.join(translated_sentence)

