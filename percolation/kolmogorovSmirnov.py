__doc__="Kolmogorov-Smirnov routines"
import numpy as n
from scipy import stats
def kolmogorovSmirnovDistance__(seq1,seq2,bins=300):
    """Calculate distance between histograms
    
    Adapted from the Kolmogorov-Smirnov test,
    returns calpha, and Dnn"""
    amin=min(min(seq1),min(seq2))
    amax=max(max(seq1),max(seq2))
    bins=n.linspace(amin,amax,bins+1,endpoint=True)
    h1=n.histogram(seq1,bins,density=True)[0]
    h2=n.histogram(seq2,bins,density=True)[0]
    space=bins[1]-bins[0]
    cs1=n.cumsum(h1*space)
    cs2=n.cumsum(h2*space)

    dc=n.abs(cs1-cs2)
    Dnn=max(dc)
    n1=len(seq1)
    n2=len(seq2)
    fact=((n1*n2)/(n1+n2))**0.5
    calpha=Dnn*fact
    return calpha, Dnn
def dnnNorm(m1,d1,m2,d2,lb=-4,rb=4,NE=1000000):
    """Calculate the Kolmogorov-Smirnov distance for two normal distributions"""
    a=stats.norm(m1,d1)
    b=stats.norm(m2,d2)
    domain=n.linspace(lb,rb,NE)
    avals=a.cdf(domain)
    bvals=b.cdf(domain)
    diffN=n.abs(avals-bvals).max()
    return diffN
def dnnUni(lb,rb,lb2,rb2,lbd=-1,rbd=4,NE=1000000):
    """Calculate the Kolmogorov-Smirnov distance for two uniform distributions"""
    rb_=rb-lb
    rb2_=rb2-lb2
    a=stats.uniform(lb,rb_)
    b=stats.uniform(lb2,rb2_)
    domain=n.linspace(lbd,rbd,NE)
    avals=a.cdf(domain)
    bvals=b.cdf(domain)
    diffU=n.abs(avals-bvals).max()
    return diffU

def weib(x,nn,a):
    """The Weibull (bivariate) distribution probability density function.

    According to Wikipedia and other sources.
    In Scipy I could only find the univariate, exponential and double
    Weibull distributions."""
    return (a / nn) * (x / nn)**(a - 1) * n.exp(-(x / nn)**a)
class WeibullGen(stats.rv_continuous):
    """A Weibull bivariate distritribution helper class.

    According to Wikipedia and other sources.
    In Scipy I could only find the univariate, exponential and double
    Weibull distributions."""
    def _pdf(self,a,k):
        return (a / k) * (x / k)**(a - 1) * n.exp(-(x / k)**a)
def dnnWeib(shape1,shape2,lb=0.00001,rb=10,NE=1000000):
    """Calculate the KS distance for two Weibull distributions."""
    x=n.linspace(lb,rb,NE)
    step=x[1]-x[0]
    raise NotImplementedError("Need to draw samples from the Weibull distribution")
    W=weib(x, 1., shape1)
    #W_=W/((W*step).sum())
    W_=W/((W).sum())
    W__=n.cumsum(W_)
    W2=weib(x, 1., shape2)
    #W2_=W2/((W2*step).sum())
    W2_=W2/((W2).sum())
    W2__=n.cumsum(W2_)
    diffW=n.abs(W__-W2__).max()
    return diffW
def dnnPower(shape1,shape2,lb=0,rb=1,NE=1000000):
    """Calculate the Kolmogorov-Smirnov distance for two power-function distributions"""
    a=stats.powerlaw(shape1)
    b=stats.powerlaw(shape2)
    domain=n.linspace(lb,rb,NE)
    avals=a.cdf(domain)
    bvals=b.cdf(domain)
    diffP=n.abs(avals-bvals).max()
    return diffP

