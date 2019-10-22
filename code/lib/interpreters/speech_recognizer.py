from lib.interpreters.interpreter_base import Interpreter
from lib.types import Identifier
from typing import List, Generator, Any
from os import path
from pocketsphinx.pocketsphinx import Decoder
from google.cloud import speech
from google.oauth2 import service_account


class SpeechRecognizer(Interpreter):
    def __init__(self, name: str, sr: str = "pocketsphinx"):
        super().__init__(name, True)
        self.sr = sr
        self.current_data = []
        self.setup()

    def setup(self) -> None:
        self.RATE = 48000  # TODO: this is defined in Audition Sensor.
        self.setup_pocketsphinx()

        if (self.sr == "googlespeech"):
            self.setup_googlespeech()

    def setup_pocketsphinx(self) -> None:
        print("Setting up PocketSphinx.")
        self.MODELDIR = "resources/model"

        config = Decoder.default_config()
        config.set_string('-hmm', path.join(self.MODELDIR, 'es-es'))
        config.set_string('-lm', path.join(self.MODELDIR, 'es-es.lm'))
        config.set_string('-dict', path.join(self.MODELDIR, 'es.dict'))

        self.decoder = Decoder(config)

        self.prev_buf_is_speech = False
        self.decoder.start_utt()
        print("Done setting up PocketSphinx.")

    def setup_googlespeech(self) -> None:
        print("Setting up Google Speech.")
        credentials = service_account.Credentials.from_service_account_file(
            'resources/keys/credentials.json')
        config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code='es-PE',
            sample_rate_hertz=self.RATE,
        )
        self.client = speech.SpeechClient(credentials=credentials)
        self.streaming_config = speech.types.StreamingRecognitionConfig(
            config=config)
        print("Done setting up Google Speech.")

    def get_destinations_ID(self, raw_data) -> List[Identifier]:
        return [self.destinations_ID[0]]

    def preprocess(self, raw_data):
        """Filtering"""
        return raw_data

    def process(self, raw_data) -> Generator:
        self.decoder.process_raw(raw_data, False, False)
        cur_buf_is_speech = self.decoder.get_in_speech()
        data = None
        print(f"prev: {self.prev_buf_is_speech}, current: {cur_buf_is_speech}")

        if not self.prev_buf_is_speech and cur_buf_is_speech:
            # Now in speech -> Start listening
            self.current_data.append(raw_data)
            self.prev_buf_is_speech = cur_buf_is_speech
            yield False

        elif self.prev_buf_is_speech and cur_buf_is_speech:
            # Still in speech -> Keep on listening
            self.current_data.append(raw_data)
            self.prev_buf_is_speech = cur_buf_is_speech
            yield False

        elif self.prev_buf_is_speech and not cur_buf_is_speech:
            # No longer in speech -> stop listening and process
            print("No longer in speech, yielding True.")
            yield True
            self.decoder.end_utt()
            if (self.sr == "googlespeech"):
                requests = (speech.types.StreamingRecognizeRequest(
                    audio_content=chunk) for chunk in self.current_data)
                responses = self.client.streaming_recognize(
                    config=self.streaming_config, requests=requests)
                try:
                    response = next(responses)
                    data = response.results[0].alternatives[0].transcript
                    conf = response.results[0].alternatives[0].confidence
                except Exception as e:
                    print(f"{self.name}>> {e}")
                    conf = None
                    data = None
                self.current_data.clear()
            elif (self.sr == "pocketsphinx"):
                try:
                    data = self.decoder.hyp().hypstr
                    conf = self.decoder.hyp().best_score
                    if data == "":
                        data = None
                except Exception as e:
                    print(f"{self.name}>> {e}")
                    conf = None
                    data = None
            print(
                f"{self.name}>> Heard DATA: '{data}' with confidence: {conf}.")
            self.decoder.start_utt()
            self.prev_buf_is_speech = cur_buf_is_speech
        else:
            self.prev_buf_is_speech = cur_buf_is_speech
            yield False

        yield data
        return

    def pass_msg(self, msg: str) -> None:
        if msg == "RESUME":
            self.e.set()

    def dump_history(self, filename: str, data: List[Any]) -> None:
        pass
