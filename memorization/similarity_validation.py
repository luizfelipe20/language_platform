import sklearn
import os
import numpy as np
from skllm.preprocessing import GPTVectorizer
from skllm.config import SKLLMConfig
from sklearn.metrics.pairwise import cosine_similarity


from sklearn.feature_extraction.text import TfidfVectorizer
from thefuzz import fuzz


SKLLMConfig.set_openai_key(os.getenv("GPT_API_KEY"))
model = GPTVectorizer()


def similarity_comparison(answer, translation):
    similarity = fuzz.partial_ratio(answer, translation)
    return similarity


def similarity_comparison_02(answer, translation):
    vectors = model.fit_transform([answer, translation])
    vector_1 = np.array(vectors[0]).reshape(1, -1)
    vector_2 = np.array(vectors[1]).reshape(1, -1)
    similarity = cosine_similarity(vector_1, vector_2)[0][0] * 100    
    return similarity


def similarity_comparison_03(answer, translation):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([answer, translation])
    similarity = cosine_similarity(vectors)[0][0] * 100
    return similarity