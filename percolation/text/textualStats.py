#import time, numpy as n, re, nltk as k, collections as c, string, pickle, os, langid, shutil
def analyseAll(texts):
    rawAnalysis=P.text.raw.analyseAll(texts) # measure stuff from raw strings: chars, tokens, sentences, messages
    posAnalysis=P.text.pos.analyseAll(texts,rawAnalysis["tokens"])
    wnAnalysis=P.text.pos.analyseAll(texts,rawAnalysis["tokens"])
    ksAnalysis=P.text.ks.selectedComparisons(texts,locals())
    auxAnalysis=P.text.auxAnalysis(texts)
    return locals()
