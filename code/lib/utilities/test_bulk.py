import os
import sys
sys.path.append(os.getcwd())

import wave
from typing import List
from lib.interpreters.speech_recognizer import SpeechRecognizer
from lib.interpreters.nlp import normalize, tokenize, untokenize
from levenshtein import jaro
from lib.utilities import settings  # for loading dotenv
import pandas as pd


def process(sr, wf):
    chunk = os.getenv("CHUNK")
    data = wf.readframes(chunk)
    while data != b'':
        gen = sr.process(data)
        stop = next(gen)
        if stop:
            ans = next(gen)
            return ans
        data = wf.readframes(chunk)
    for i in range(4):
        gen = sr.process(bytes(chunk * bytes[0]))
        if stop:
            ans = next(gen)
            return ans
    return None


def compare(x, y) -> float:
    x = normalize(x)
    x_tokens = [word.lower() for word in tokenize(x) if word.isalnum()]

    y = normalize(y)
    y_tokens = [word.lower() for word in tokenize(y) if word.isalnum()]

    return jaro(untokenize(x_tokens), untokenize(y_tokens))


def test_sr(X: List[str], Y: List[str]):
    """
    X : list of wav filenames.
    Y : list of translations of their corresponding file
    """

    sr = SpeechRecognizer("test_sr", "googlespeech")
    Yp = []
    accuracies = []

    for i, filename in enumerate(X):
        wf = wave.open(filename, 'rb')
        if wf.getframerate() != int(os.getenv("RATE")):
            raise Exception("RATE of recorded audio doesn't match mic RATE.")
        ans = process(sr, wf)
        acc = compare(ans, Y[i])
        Yp.append(ans)
        accuracies.append(acc)

    raw = {'file': X, 'text': Y, 'guess': Yp, 'accuracy': accuracies}
    df = pd.DataFrame(raw)

    return df


def main():
    pass


if __name__ == "__main__":
    main()
