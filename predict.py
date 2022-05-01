from sentence_transformers import SentenceTransformer, util
import numpy as np
import pickle
import os

def load_model():
    with open(os.path.join('resources', 'model.pkl'), 'rb') as f:
        return pickle.load(f)

def load_embeddings():
    with open(os.path.join('resources', 'doc_emb.pkl'), 'rb') as f:
        return pickle.load(f)

def load_answers():
    with open(os.path.join('resources', 'answers.pkl'), 'rb') as f:
        return pickle.load(f)

model = load_model()
doc_emb = load_embeddings()
answers = load_answers()

def predict(sentence):
    sentence_embedding = model.encode(sentence)
    scores = util.dot_score(sentence_embedding, doc_emb)[0].cpu().tolist()

    # Find the closest sentence embeddings
    idx = np.argmax(scores)
    # Find the exact sentence in the answer
    tmp_ans = answers[idx].split('\n')
    tmp_ans_emb = model.encode(tmp_ans)
    tmp_score = util.dot_score(sentence_embedding, tmp_ans_emb)[0].cpu().tolist()

    # Return string if the score is more than 0.5, otherwise return 'I don't know'
    if max(tmp_score) >= 0.5:
        return tmp_ans[np.argmax(tmp_score)]
    else:
        return 'Sorry, I don\'t know the answer to that.'