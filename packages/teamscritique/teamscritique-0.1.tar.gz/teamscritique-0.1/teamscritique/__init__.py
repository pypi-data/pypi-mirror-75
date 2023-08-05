from .utils import extract_feature
from .utils import emotionsToLables
import pickle
import numpy as np

def analyze(file):
    model = pickle.load(open("teamscritique/mlp_classifier.model", "rb"))
    emotion = emotionsToLables[model.predict(np.array([extract_feature(file, mfcc=True, chroma=True, mel=True)]))[0]]
    return emotion