import pickle
def stopwords() -> list:
    with open('./zstopword_arr','rb') as fp:
        stopwords = list(pickle.load(fp))
    return stopwords