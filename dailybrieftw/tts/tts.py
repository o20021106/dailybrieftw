import os
import re
import zipfile

import tensorflow as tf
import soundfile as sf
import yaml
import opencc
from tensorflow_tts.inference import AutoConfig
from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor

from dailybrieftw.utils.utils import download_blob

    
class TTS():
    def __init__(self):
        self.converter = opencc.OpenCC('tw2s.json')
        tts_model_dir = os.environ['TTS_MODEL_DIR']
        if not os.path.exists(tts_model_dir):
            parent_dir = os.path.dirname(tts_model_dir)
            zip_file_path = os.path.join(parent_dir, 'model_files.zip')
            download_blob('dailybrief', 'models/model_files.zip', zip_file_path)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(parent_dir)
        tacotron2_config_file = os.path.join(
            tts_model_dir, 'config/tacotron2.baker.v1.yaml')
        mb_melgan_config_file = os.path.join(
            tts_model_dir, 'config/multiband_melgan.baker.v1.yaml')
        tacotron2_config = AutoConfig.from_pretrained(tacotron2_config_file)
        mb_melgan_config = AutoConfig.from_pretrained(mb_melgan_config_file)
        text2mel_model_file = os.path.join(
            tts_model_dir, 'models/tacotron-model-100000.h5')
        vocoder_model_file = os.path.join(tts_model_dir, 'models/generator-920000.h5')
        baker_mapper_file = os.path.join(tts_model_dir, 'models/baker_mapper.json')

        self.text2mel_model = TFAutoModel.from_pretrained(
            config=tacotron2_config,
            pretrained_path=text2mel_model_file,
            name='tacotron2'
        )
        self.vocoder_model = TFAutoModel.from_pretrained(
            config=mb_melgan_config,
            pretrained_path=vocoder_model_file,
            name='mb_melgan'
        )
        self.processor = AutoProcessor.from_pretrained(pretrained_path=baker_mapper_file)

    def do_synthesis(self, input_text, simplified=True):
        input_text = self.preprocess(input_text, simplified)
        input_ids = self.processor.text_to_sequence(input_text, inference=True)

        _, mel_outputs, stop_token_prediction, alignment_history = self.text2mel_model.inference(
            tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
            tf.convert_to_tensor([len(input_ids)], tf.int32),
            tf.convert_to_tensor([0], dtype=tf.int32)
        )

        remove_end = 1024
        audio = self.vocoder_model.inference(mel_outputs)[0, :-remove_end, 0]
        return mel_outputs.numpy(), alignment_history.numpy(), audio.numpy()

    def map_nums(self, text):
        maps = '零一二三四五六七八九'
        nums = '0123456789'
        transformed_text = ''
        for c in text:
            if c in nums:
                c = maps[int(c)]
            transformed_text += c
        return transformed_text

    def replace_punctuation(self, text):
        return re.sub(r'[!！,，。.?？、～~]', '#3', text)

    def replace_space(self, text):
        text = re.sub(r'[ 　]', ',', text)
        return text

    def remove_hash(self, text):
        return re.sub(r'#', '', text)  

    def simplify(self, text):
        return self.converter.convert(text)

    def preprocess(self, text, simplified):
        if not simplified:
            text = self.simplify(text)
        text = self.map_nums(text)
        text = self.remove_hash(text)
        text = self.replace_space(text)
        text = self.replace_punctuation(text)
        return text
    

if __name__ == '__main__':
    input_text = '今天天氣晴朗ㄋ'
    file_path = './audio.wav'
    tts = TTS()
    mels, alignment_history, audios = tts.do_synthesis(input_text, False)
    sf.write(file_path, audios, 22050, "PCM_16")
