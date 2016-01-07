__doc__="Term frequency - inverse document frequency distance between documents"
from sklearn.feature_extraction.text import TfidfVectorizer
def analyseAll(texts):
    texts_measures={"texts_overall":[{"tfIdf":{"matrix":{}}}]}
    texts_measures["texts_overall"][-1]["tfIdf"]["matrix"]["distances"]=tfIdf(texts)

def tfIdf(texts):
    """Returns distance matrix for the texts"""
    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform([tt.lower() for tt in texts])
    aa=(tfidf * tfidf.T).A
    return aa
