import time, numpy as n, gmane as g
from scipy import stats as st
from .tableHelpers import lTable
TT=time.time()
def dl(fname,hl,vl,over=0):
    fname+=".tex"
    foo=g.doubleLines(fname,hlines=hl,vlines=vl)
    if not over:
        tablefname=fname.replace(".tex","_.tex")
    g.writeTex(foo,tablefname)
def me(fname,mark,locs,over=1):
    fn=fname+".tex"
    foo=g.markEntries_(fn,mark,locs)
    if not over:
        tn=tn.replace(".tex","_.tex")
    g.writeTex(foo,fn)

def kolmogorovSmirnovDistance(seq1,seq2,bins=300):
    """Calculate distance between histograms
    
    Adapted from the Kolmogorov-Smirnov test"""
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
    fact=((n1+n2)/(n1*n2))**0.5
    calpha=Dnn/fact
    return calpha
def kolmogorovSmirnovDistance_(seq1,seq2,bins=300):
    """Calculate distance between histograms
    
    Adapted from the Kolmogorov-Smirnov test,
    returns calpha, fact and Dnn"""
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
    return calpha, fact, Dnn
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
    a=st.norm(m1,d1)
    b=st.norm(m2,d2)
    domain=n.linspace(lb,rb,NE)
    avals=a.cdf(domain)
    bvals=b.cdf(domain)
    diffN=n.abs(avals-bvals).max()
    return diffN
def dnnUni(lb,rb,lb2,rb2,lbd=-1,rbd=4,NE=1000000):
    rb_=rb-lb
    rb2_=rb2-lb2
    a=st.uniform(lb,rb_)
    b=st.uniform(lb2,rb2_)
    domain=n.linspace(lbd,rbd,NE)
    avals=a.cdf(domain)
    bvals=b.cdf(domain)
    diffU=n.abs(avals-bvals).max()
    return diffU

def weib(x,nn,a):
    return (a / nn) * (x / nn)**(a - 1) * n.exp(-(x / nn)**a)
def dnnWeib(shape1,shape2,lb=0.00001,rb=10,NE=1000000):
    x=n.linspace(lb,rb,NE)
    step=x[1]-x[0]
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
    a=st.powerlaw(shape1)
    b=st.powerlaw(shape2)
    domain=n.linspace(lb,rb,NE)
    avals=a.cdf(domain)
    bvals=b.cdf(domain)
    diffP=n.abs(avals-bvals).max()
    return diffP





def min3(narray):
    narray_=n.array(narray)
    args=narray_.argsort()
    return narray_[args[:3]]
def max3(narray):
    narray_=n.array(narray)
    args=narray_.argsort()
    return narray_[args[-3:]]
def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()
class KSReferences:
    """Hold references and simulation routines"""
    alphas=[0.1,0.05,0.025,0.01,0.005,0.001]
    calphas=[1.22,1.36,1.48,1.63,1.73,1.95]
    def __init__(self,NC=100,NE=1000,NB=300,adir="/home/r/repos/kolmogorov-smirnov/",NE2=1000,make_all=True):
        table_dir=adir+"tables/"
        aux_dir=adir+"aux/"
        if not NE2:
            NE2=NE
        if make_all:
            self.makeAllTables(NC,NE,NE2,NB,aux_dir,table_dir)
        mvars=("NC","NE","NE2","NB","adir")
        self.vdict={}
        for mvar in mvars:
            self.vdict[mvar] = locals()[mvar]
    def makeAllTables(self,NC,NE,NE2,NB,aux_dir,table_dir):
        #self.makePreambule(NC,NE,NE2,NB,aux_dir)
        #self.makeNormalVerification(NC,NE,NE2,NB,table_dir)
        #self.makeUniformVerification(NC,NE,NE2,NB,table_dir)
        #self.makeWeibullVerification(NC,NE,NE2,NB,table_dir)
        #self.makePowerVerification(NC,NE,NE2,NB,table_dir)
        self.makeNormalDifferencesDispersion(NC,NE,NE2,NB,table_dir)
        self.makeNormalDifferencesMean(NC,NE,NE2,NB,table_dir)
        self.makeUniformDifferencesDispersion(NC,NE,NE2,NB,table_dir)
        self.makeUniformDifferencesMean(NC,NE,NE2,NB,table_dir)
        self.makeWeibullDifferencesShape(NC,NE,NE2,NB,table_dir)
        self.makePowerDifferencesShape(NC,NE,NE2,NB,table_dir)
        self.makeNormalDifferencesSamples(NC,NB,table_dir)
        self.makeNormalDifferencesSamples2(NC,NB,table_dir)
        self.makeUniformDifferencesSamples(NC,NB,table_dir)
        self.makeUniformDifferencesSamples2(NC,NB,table_dir)
        self.makeWeibullDifferencesSamples(NC,NB,table_dir)
        self.makePowerDifferencesSamples(NC,NB,table_dir)
        self.enhanceTables(table_dir)

    def makePowerDifferencesSamples(self,NC,NB,table_dir):
        #xx=n.arange(.7,2.7,0.2)
        xx=n.logspace(2,5,4)
        labels=xx
        shapes=(1.5,1.7)
        distsAllW=[[kolmogorovSmirnovDistance_(
                n.random.power(shapes[0],xxx),
                n.random.power(shapes[1],xxx), NB) for i in range(NC)]
                for xxx in xx]
        distsAllWC=[[i[0] for i in j] for j in distsAllW]
        dnns=[[i[2] for i in j] for j in distsAllW]
        data=[(n.mean(dd),n.std(dd),n.median(dd),
            ("{:.3f},"*3)[:-1].format(*min3(dd)),
            ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllWC]
        data_=[]
        i=0
        for dists in distsAllWC:
            line=[]
            dnn=dnns[i]
            kline=[n.mean(dnn), n.std(dnn)]
            for calpha in self.calphas:
                line.append(sum([dist>calpha for dist in dists])/NC)
            data_.append(list(data[i])+kline+line); i+=1
        diffP=dnnPower(shapes[0],shapes[1])
        caption=r"""Measurements of $c$ through simulations
        with fixed power distributions but different number of samples.
        One distribution has shape parameter a={}.
        The other distribution has a={}.
        The KS statistic of these distributions converges
        to {:.4f} as sample sizes increases.""".format(shapes[0],shapes[1],diffP)
        labelsh=[r"$n=n'$",r"$\mu(c)$",r"$\sigma(c)$","m(c)","min(c)","max(c)",r"$\mu(D_{F,F'})$",r"$\sigma(D_{F,F'})$"]
        labelsh+=[r"$\overline{{C({})}}$".format(alpha) for alpha in self.alphas]
        fname="tabPowerDiffSamples.tex"
        lTable(labels,labelsh,data_,caption,table_dir+fname,"kolmSamp_")
        i=0
        check("table {} written at {}".format(fname,table_dir))
    def makeWeibullDifferencesSamples(self,NC,NB,table_dir):
        #xx=n.arange(.7,2.7,0.2)
        xx=n.logspace(2,5,4)
        labels=xx
        shapes=(1.5,1.7)
        distsAllW=[[kolmogorovSmirnovDistance_(
                n.random.weibull(shapes[0],xxx),
                n.random.weibull(shapes[1],xxx), NB) for i in range(NC)]
                for xxx in xx]
        distsAllWC=[[i[0] for i in j] for j in distsAllW]
        dnns=[[i[2] for i in j] for j in distsAllW]
        data=[(n.mean(dd),n.std(dd),n.median(dd),
            ("{:.3f},"*3)[:-1].format(*min3(dd)),
            ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllWC]
        data_=[]
        i=0
        for dists in distsAllWC:
            line=[]
            dnn=dnns[i]
            kline=[n.mean(dnn), n.std(dnn)]
            for calpha in self.calphas:
                line.append(sum([dist>calpha for dist in dists])/NC)
            data_.append(list(data[i])+kline+line); i+=1
        #x=n.linspace(0,20,100000)
        #step=x[1]-x[0]
        #W=weib(x, 1., 1.5)
        #W_=W/(W*step).sum()
        #W2=weib(x, 1., 1.7)
        #W2_=W2/(W2*step).sum()
        #diffW=n.abs(W_-W2_).max()
        diffW=dnnWeib(shapes[0],shapes[1])
        caption=r"""Measurements of $c$ through simulations
        with fixed Weibull distributions but different number of samples.
        One distribution has shape parameter $a={}$.
        The other distribution has $a={}$.
        The KS statistic of these distributions converges
        to {:.4f} as sample sizes increases.""".format(shapes[0],shapes[1],diffW)
        labelsh=[r"$n=n'$",r"$\mu(c)$",r"$\sigma(c)$","m(c)","min(c)","max(c)",r"$\mu(D_{F,F'})$",r"$\sigma(D_{F,F'})$"]
        labelsh+=[r"$\overline{{C({})}}$".format(alpha) for alpha in self.alphas]
        fname="tabWeibullDiffSamples.tex"
        lTable(labels,labelsh,data_,caption,table_dir+fname,"kolmSamp_")
        i=0
        check("table {} written at {}".format(fname,table_dir))
    def makeUniformDifferencesSamples2(self,NC,NB,table_dir):
        #xx=n.arange(.7,2.7,0.2)
        xx=n.logspace(2,5,4)
        labels=xx
        distsAllW=[[kolmogorovSmirnovDistance_(
                n.random.random(xxx)*1.2-0.1,
                n.random.random(xxx), NB) for i in range(NC)]
                for xxx in xx]
        distsAllWC=[[i[0] for i in j] for j in distsAllW]
        dnns=[[i[2] for i in j] for j in distsAllW]
        data=[(n.mean(dd),n.std(dd),n.median(dd),
            ("{:.3f},"*3)[:-1].format(*min3(dd)),
            ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllWC]
        data_=[]
        i=0
        for dists in distsAllWC:
            line=[]
            dnn=dnns[i]
            kline=[n.mean(dnn), n.std(dnn)]
            for calpha in self.calphas:
                line.append(sum([dist>calpha for dist in dists])/NC)
            data_.append(list(data[i])+kline+line); i+=1
        diffU2=dnnUni(0,1,-.1,1.1)
        caption=r"""Measurements of $c$ through simulations
        with fixed uniform distributions but different number of samples.
        One distribution is uniform in [0,1].
        The other distribution is uniform in [-0.1,1.1].
        The KS statistic of these distributions converges
        to {:.4f} as sample sizes increases.""".format(diffU2)
        labelsh=[r"$n=n'$",r"$\mu(c)$",r"$\sigma(c)$","m(c)","min(c)","max(c)",r"$\mu(D_{F,F'})$",r"$\sigma(D_{F,F'})$"]
        labelsh+=[r"$\overline{{C({})}}$".format(alpha) for alpha in self.alphas]
        fname="tabUniformDiffSamples2.tex"
        lTable(labels,labelsh,data_,caption,table_dir+fname,"kolmSamp_")
        i=0
        check("table {} written at {}".format(fname,table_dir))


    def makeUniformDifferencesSamples(self,NC,NB,table_dir):
        #xx=n.arange(.7,2.7,0.2)
        xx=n.logspace(2,5,4)
        labels=xx
        distsAllW=[[kolmogorovSmirnovDistance_(
                n.random.random(xxx)+0.05,n.random.random(xxx),NB) for i in range(NC)]

                for xxx in xx]
        distsAllWC=[[i[0] for i in j] for j in distsAllW]
        dnns=[[i[2] for i in j] for j in distsAllW]
        data=[(n.mean(dd),n.std(dd),n.median(dd),
            ("{:.3f},"*3)[:-1].format(*min3(dd)),
            ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllWC]
        data_=[]
        i=0
        for dists in distsAllWC:
            line=[]
            dnn=dnns[i]
            kline=[n.mean(dnn), n.std(dnn)]
            for calpha in self.calphas:
                line.append(sum([dist>calpha for dist in dists])/NC)
            data_.append(list(data[i])+kline+line); i+=1
        diffU=dnnUni(0,1,0.05,1.05)
        caption=r"""Measurements of $c$ through simulations
        with fixed uniform distributions but different number of samples.
        One distribution is uniform in [0,1].
        The other distribution is uniform in [0.05,1.05].
        The KS statistic of these distributions converges
        to {:.4f} as sample sizes increases.""".format(diffU)
        labelsh=[r"$n=n'$",r"$\mu(c)$",r"$\sigma(c)$","m(c)","min(c)","max(c)",r"$\mu(D_{F,F'})$",r"$\sigma(D_{F,F'})$"]
        labelsh+=[r"$\overline{{C({})}}$".format(alpha) for alpha in self.alphas]
        fname="tabUniformDiffSamples.tex"
        lTable(labels,labelsh,data_,caption,table_dir+fname,"kolmSamp_")
        i=0
        check("table {} written at {}".format(fname,table_dir))



    def makeNormalDifferencesSamples2(self,NC,NB,table_dir):
        #xx=n.arange(.7,2.7,0.2)
        xx=n.logspace(2,5,4)
        labels=xx
        shape=(0,1.2)
        distsAllW=[[kolmogorovSmirnovDistance_(
                n.random.normal(0,1,xxx),
                    n.random.normal(shape[0],shape[1],xxx),NB) for i in range(NC)]

                for xxx in xx]
        distsAllWC=[[i[0] for i in j] for j in distsAllW]
        dnns=[[i[2] for i in j] for j in distsAllW]
        data=[(n.mean(dd),n.std(dd),n.median(dd),
            ("{:.3f},"*3)[:-1].format(*min3(dd)),
            ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllWC]
        data_=[]
        i=0
        for dists in distsAllWC:
            line=[]
            dnn=dnns[i]
            kline=[n.mean(dnn), n.std(dnn)]
            for calpha in self.calphas:
                line.append(sum([dist>calpha for dist in dists])/NC)
            data_.append(list(data[i])+kline+line); i+=1
        diffN2=dnnNorm(0,1,shape[0],shape[1])
        caption=r"""Measurements of $c$ through simulations
        with fixed normal distributions but different number of samples.
        One normal distribution has $\mu=0$ and $\sigma=1$.
        The other normal distribution have
        $\mu={}$ and $\sigma={}$.
        The KS statistic of these distributions converges
        to {:.4f} as sample sizes increases.""".format(shape[0],shape[1],diffN2)
        labelsh=[r"$n=n'$",r"$\mu(c)$",r"$\sigma(c)$","$m(c)$","$min(c)$","$max(c)$",r"$\mu(D_{F,F'})$",r"$\sigma(D_{F,F'})$"]
        labelsh+=[r"$\overline{{C({})}}$".format(alpha) for alpha in self.alphas]
        fname="tabNormalDiffSamples2.tex"
        lTable(labels,labelsh,data_,caption,table_dir+fname,"kolmSamp_")
        i=0
        check("table {} written at {}".format(fname,table_dir))

    def makeNormalDifferencesSamples(self,NC,NB,table_dir):
        #xx=n.arange(.7,2.7,0.2)
        xx=n.logspace(2,5,4)
        labels=xx
        distsAllW=[[kolmogorovSmirnovDistance_(
                n.random.normal(0,1,xxx),
                n.random.normal(0.1,1,xxx), NB) for i in range(NC)]

                for xxx in xx]
        distsAllWC=[[i[0] for i in j] for j in distsAllW]
        dnns=[[i[2] for i in j] for j in distsAllW]
        data=[(n.mean(dd),n.std(dd),n.median(dd),
            ("{:.3f},"*3)[:-1].format(*min3(dd)),
            ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllWC]
        data_=[]
        i=0
        for dists in distsAllWC:
            line=[]
            dnn=dnns[i]
            kline=[n.mean(dnn), n.std(dnn)]
            for calpha in self.calphas:
                line.append(sum([dist>calpha for dist in dists])/NC)
            data_.append(list(data[i])+kline+line); i+=1
        diffN=dnnNorm(0,1,0.1,1)
        caption=r"""Measurements of $c$ through simulations
        with fixed normal distributions but different number of samples.
        One normal distribution has $\mu=0$ and $\sigma=1$.
        The other normal distribution have $\mu=0.1$ and $\sigma=1$.
        The KS statistic of these distributions converges
        to {:.4f} as sample sizes increases.""".format(diffN)
        labelsh=[r"$n=n'$",r"$\mu(c)$",r"$\sigma(c)$",r"$m(c)$",r"$min(c)$",r"$max(c)$",r"$\mu(D_{F,F'})$",r"$\sigma(D_{F,F'})$"]
        labelsh+=[r"$\overline{{C({})}}$".format(alpha) for alpha in self.alphas]
        fname="tabNormalDiffSamples.tex"
        lTable(labels,labelsh,data_,caption,table_dir+fname,"kolmSamp_")
        i=0
        check("table {} written at {}".format(fname,table_dir))
    def enhanceTables(self,table_dir):
        dl(table_dir+"tabNormNull",[1],[])
        me(table_dir+"tabNormNull_","\\bf",[(i,1) for i in      range(1,7)])
        dl(table_dir+"tabUniformNull",[1],[])
        me(table_dir+"tabUniformNull_","\\bf",[(i,1) for i in      range(1,7)])
        dl(table_dir+"tabWeibullNull",[1],[])
        me(table_dir+"tabWeibullNull_","\\bf",[(i,1) for i in      range(1,7)])
        dl(table_dir+"tabPowerNull",[1],[])
        me(table_dir+"tabPowerNull_","\\bf",[(i,1) for i in      range(1,7)])
        dl(table_dir+"tabNormDiff3",[1],[],)
        me(table_dir+"tabNormDiff3_","\\bf",[(6,i) for i in         range(0,12)])
        dl(table_dir+"tabNormDiffMean",[1],[],)
        me(table_dir+"tabNormDiffMean_","\\bf",[(1,i) for i in      range(0,14)])
        g.fSize(table_dir+"tabNormDiffMean_.tex",r"\scriptsize",1)

        dl(table_dir+"tabNormDiffDispersion",[1],[],)
        me(table_dir+"tabNormDiffDispersion_","\\bf",[(6,i) for i in      range(0,14)])
        g.fSize(table_dir+"tabNormDiffDispersion_.tex",r"\scriptsize",1)

        dl(table_dir+"tabUniformDiffSpread",[1],[],)
        me(table_dir+"tabUniformDiffSpread_","\\bf",[(7,i) for i in range(0,14)])
        g.fSize(table_dir+"tabUniformDiffSpread_.tex",r"\scriptsize",1)
        dl(table_dir+"tabUniformDiffMean",[1],[],)
        me(table_dir+"tabUniformDiffMean_","\\bf",[(1,i) for i in   range(0,14)])
        g.fSize(table_dir+"tabUniformDiffMean_.tex",r"\scriptsize",1)
        dl(table_dir+"tabWeibullDiffShape",[1],[],)
        me(table_dir+"tabWeibullDiffShape_","\\bf",[(5,i) for i in  range(0,14)])
        g.fSize(table_dir+"tabWeibullDiffShape_.tex",r"\scriptsize",1)
        dl(table_dir+"tabPowerDiffShape",[1],[],)
        me(table_dir+"tabPowerDiffShape_","\\bf",[(5,i) for i in    range(0,14)])
        g.fSize(table_dir+"tabPowerDiffShape_.tex",r"\scriptsize",1)
        dl(table_dir+"tabNormalDiffSamples",[1],[],)
        me(table_dir+"tabNormalDiffSamples_","\\bf",[(i,0) for i in         range(1,5)])
        g.fSize(table_dir+"tabNormalDiffSamples_.tex",r"\vspace{-.3cm}\scriptsize",1)
        dl(table_dir+"tabNormalDiffSamples2",[1],[],)
        me(table_dir+"tabNormalDiffSamples2_","\\bf",[(i,0) for i in         range(1,5)])
        g.fSize(table_dir+"tabNormalDiffSamples2_.tex","\\vspace{-.3cm}\\scriptsize",1)
        dl(table_dir+"tabUniformDiffSamples",[1],[],)
        me(table_dir+"tabUniformDiffSamples_","\\bf",[(i,0) for i in         range(1,5)])
        g.fSize(table_dir+"tabUniformDiffSamples_.tex",r"\vspace{-.3cm}\scriptsize",1)
        dl(table_dir+"tabUniformDiffSamples2",[1],[],)
        me(table_dir+"tabUniformDiffSamples2_","\\bf",[(i,0) for i in         range(1,5)])
        g.fSize(table_dir+"tabUniformDiffSamples2_.tex",r"\vspace{-.3cm}\scriptsize",1)
        dl(table_dir+"tabWeibullDiffSamples",[1],[],)
        me(table_dir+"tabWeibullDiffSamples_","\\bf",[(i,0) for i in         range(1,5)])
        g.fSize(table_dir+"tabWeibullDiffSamples_.tex",r"\vspace{-.3cm}\scriptsize",1)
        dl(table_dir+"tabPowerDiffSamples",[1],[],)
        me(table_dir+"tabPowerDiffSamples_","\\bf",[(i,0) for i in         range(1,5)])
        g.fSize(table_dir+"tabPowerDiffSamples_.tex",r"\vspace{-.3cm}\scriptsize",1)


    def makePreambule(self,NC,NE,NE2,NB,aux_dir):
        fname=aux_dir+"preambule1.tex"
        preambule=r"""The number of comparisons is $N_c={}$,
        each with the sample sizes of $n={}$ and $n'={}$.
        Each histogram have $N_b={}$ equally spaced bins.""".format(NC,NE,NE2,NB)
        with open(fname,"w") as f:
            f.write(preambule)
    def makeNormalVerification(self,NC,NE,NE2,NB,table_dir):
        check("antes")
        dists=[kolmogorovSmirnovDistance(
                n.random.normal(0,1,NE),n.random.normal(0,1,NE2))
                for i in range(NC)]; check("normal1")
        dists2=[kolmogorovSmirnovDistance(
                n.random.normal(3,2,NE),n.random.normal(3,2,NE2))
                for i in range(NC)]; check("normal2")
        dists3=[kolmogorovSmirnovDistance(
                n.random.normal(6,3,NE),n.random.normal(6,3,NE2))
                for i in range(NC)]; check("normal3")
        labelsh=(r"$\alpha N_c$",r"$\alpha$",r"$c(\alpha)$",r"$|C_1(\alpha)|$",r"$|C_2(\alpha)|$",r"$|C_3(\alpha)|$")
        caption=r"""The theoretical maximum number $\alpha N_c$ of rejections
        of the null hypothesis for significance levels $\alpha$.
        The $c_1$ values were calculated using simulations of normal distributions with $\mu={}$ and $\sigma={}$.
        The $c_2$ values were calculated using simulations of normal distributions with $\mu={}$ and $\sigma={}$.
        The $c_3$ values were calculated using simulations of normal distributions with $\mu={}$ and $\sigma={}$.
        Over all $N_c$ comparisons,
         $\mu(c_1)={:.4f}$ and $\sigma(c_1)={:.4f}$,
         $\mu(c_2)={:.4f}$ and $\sigma(c_2)={:.4f}$,
         $\mu(c_3)={:.4f}$ and $\sigma(c_3)={:.4f}$ .
        """.format(        0,1,
                3,2,
                6,3,
                   n.mean(dists ),n.std(dists ),
                   n.mean(dists2),n.std(dists2),
                   n.mean(dists3),n.std(dists3),
                   )
        data=[]
        labels=[]
        for alpha, calpha in zip(self.alphas,self.calphas):
            n1=sum([dist>calpha for dist in dists])
            n2=sum([dist>calpha for dist in dists2])
            n3=sum([dist>calpha for dist in dists3])
            data.append((alpha,calpha,n1,n2,n3))
            labels.append(alpha*NC)
        fname="tabNormNull.tex"
        lTable(labels,labelsh,data,caption,table_dir+fname)
        check("table {} written at {}".format(fname,table_dir))
    def makeUniformVerification(self,NC,NE,NE2,NB,table_dir):
        check("antes")
        dists=[kolmogorovSmirnovDistance(
                n.random.random(NE),n.random.random(NE2))
                for i in range(NC)]; check("uniforme1")
        dists2=[kolmogorovSmirnovDistance(
                2*n.random.random(NE)+2,2*n.random.random(NE2)+2)
                for i in range(NC)]; check("uniforme2")

        dists3=[kolmogorovSmirnovDistance(
                3*n.random.random(NE)+4,3*n.random.random(NE2)+4)
                for i in range(NC)]; check("uniforme3")
        labelsh=(r"$\alpha N_c$",r"$\alpha$",r"$c(\alpha)$",r"$|C_1(\alpha)|$",r"$|C_2(\alpha)|$",r"$|C_3(\alpha)|$")
        caption=r"""The theoretical maximum number $\alpha N_c$ of rejections
        of the null hypothesis for critical values of $\alpha$.
        The $c_1$ values were calculated using simulations of uniform distributions within $[{},{})$.
        The $c_2$ values were calculated using simulations of uniform distributions within $[{},{})$.
        The $c_3$ values were calculated using simulations of uniform distributions with $\mu={}$ and $\sigma={}$.
        Over all $N_c$ comparisons,
         $\mu(c_1)={:.4f}$ and $\sigma(c_1)={:.4f}$,
         $\mu(c_2)={:.4f}$ and $\sigma(c_2)={:.4f}$,
         $\mu(c_3)={:.4f}$ and $\sigma(c_3)={:.4f}$ .
        """.format(
                0,1,
                2,6,
                4,10,
                   n.mean(dists ),n.std(dists ),
                   n.mean(dists2),n.std(dists2),
                   n.mean(dists3),n.std(dists3),
                   )
        data=[]
        labels=[]
        for alpha, calpha in zip(self.alphas,self.calphas):
            n1=sum([dist>calpha for dist in dists])
            n2=sum([dist>calpha for dist in dists2])
            n3=sum([dist>calpha for dist in dists3])
            data.append((alpha,calpha,n1,n2,n3))
            labels.append(alpha*NC)
        fname="tabUniformNull.tex"
        lTable(labels,labelsh,data,caption,table_dir+fname)
        print("table {} written at {}".format(fname,table_dir))
    def makeWeibullVerification(self,NC,NE,NE2,NB,table_dir):
        check("antes")
        dists=[kolmogorovSmirnovDistance(
                n.random.weibull(0.1,NE),n.random.weibull(0.1,NE2))
                for i in range(NC)]; check("weibull1")
        dists2=[kolmogorovSmirnovDistance(
                n.random.weibull(2,NE),n.random.weibull(2,NE2))
                for i in range(NC)]; check("weibull2")
        dists3=[kolmogorovSmirnovDistance(
                n.random.weibull(4,NE),n.random.weibull(4,NE2))
                for i in range(NC)]; check("weibull3")
        dists4=[kolmogorovSmirnovDistance(
                n.random.weibull(6,NE),n.random.weibull(6,NE2))
                for i in range(NC)]; check("weibull4")
        labelsh=(r"$\alpha N_c$",r"$\alpha$",r"$c(\alpha)$",r"$|C_1(\alpha)|$",r"$|C_2(\alpha)|$",r"$|C_3(\alpha)|$",r"$|C_4(\alpha)|$")
        caption=r"""The theoretical maximum number $\alpha N_c$ of rejections
        of the null hypothesis for critical values of $\alpha$.
        The $c_1$ values were calculated using simulations of 1-parameter Weibull distributions with $a={}$.
        The $c_2$ values were calculated using simulations of 1-parameter Weibull distributions with $a={}$.
        The $c_3$ values were calculated using simulations of 1-parameter Weibull distributions with $a={}$.
        Over all $N_c$ comparisons,
        The $N_o$ values of $c_4$ were calculated using simulations of
         1-parameter Weibull distributions with $a={}$.
        Over all $N_c$ comparisons,
         $\mu(c_1)={:.4f}$ and $\sigma(c_1)={:.4f}$,
         $\mu(c_2)={:.4f}$ and $\sigma(c_2)={:.4f}$,
         $\mu(c_3)={:.4f}$ and $\sigma(c_3)={:.4f}$ .
         $\mu(c_4)={:.4f}$ and $\sigma(c_4)={:.4f}$ .
        """.format(
                0.1,
                2,
                4,
                6,
                   n.mean(dists ),n.std(dists ),
                   n.mean(dists2),n.std(dists2),
                   n.mean(dists3),n.std(dists3),
                   n.mean(dists4),n.std(dists4),
                   )
        data=[]
        labels=[]
        for alpha, calpha in zip(self.alphas,self.calphas):
            n1=sum([dist>calpha for dist in dists])
            n2=sum([dist>calpha for dist in dists2])
            n3=sum([dist>calpha for dist in dists3])
            n4=sum([dist>calpha for dist in dists4])
            data.append((alpha,calpha,n1,n2,n3,n4))
            labels.append(alpha*NC)
        fname="tabWeibullNull.tex"
        lTable(labels,labelsh,data,caption,table_dir+fname)
        print("table {} written at {}".format(fname,table_dir))
    def makePowerVerification(self,NC,NE,NE2,NB,table_dir):
        check("antes")
        dists=[kolmogorovSmirnovDistance(
                n.random.power(0.3,NE),n.random.power(0.3,NE2))
                for i in range(NC)]; check("power1")
        dists2=[kolmogorovSmirnovDistance(
                n.random.power(1,NE),n.random.power(1,NE2))
                for i in range(NC)]; check("power2")
        dists3=[kolmogorovSmirnovDistance(
                n.random.power(2,NE),n.random.power(2,NE2))
                for i in range(NC)]; check("power3")
        dists4=[kolmogorovSmirnovDistance(
                n.random.power(3,NE),n.random.power(3,NE2))
                for i in range(NC)]; check("power4")
        dists4_=[kolmogorovSmirnovDistance(
                n.random.power(4,NE),n.random.power(4,NE2))
                for i in range(NC)]; check("power5")
        labelsh=(r"$\alpha N_c$",r"$\alpha$",r"$c(\alpha)$",r"$|C_1(\alpha)|$",r"$|C_2(\alpha)|$",r"$|C_3(\alpha)|$",r"$|C_4(\alpha)|$",r"$|C_5(\alpha)|$")
        caption=r"""The theoretical maximum number $\alpha N_c$ of rejections
        of the null hypothesis for critical values of $\alpha$.
        The $c_1$ values were calculated using simulations of power functions distributions with $a={}$.
        The $c_2$ values were calculated using simulations of power functions distributions with $a={}$.
        The $c_3$ values were calculated using simulations of power functions distributions with $a={}$.
        The $c_4$ values were calculated using simulations of power functions distributions with $a={}$.
        The $c_5$ values were calculated using simulations of power functions distributions with $a={}$.
        Over all $N_c$ comparisons,
         $\mu(c_1)={:.4f}$ and $\sigma(c_1)={:.4f}$,
         $\mu(c_2)={:.4f}$ and $\sigma(c_2)={:.4f}$,
         $\mu(c_3)={:.4f}$ and $\sigma(c_3)={:.4f}$ .
         $\mu(c_4)={:.4f}$ and $\sigma(c_4)={:.4f}$ .
         $\mu(c_5)={:.4f}$ and $\sigma(c_5)={:.4f}$ .
        """.format(
                0.3,
                1,
                2,
                3,
                4,
                   n.mean(dists ),n.std(dists ),
                   n.mean(dists2),n.std(dists2),
                   n.mean(dists3),n.std(dists3),
                   n.mean(dists4),n.std(dists4),
                   n.mean(dists4_),n.std(dists4_),
                   )
        data=[]
        labels=[]
        for alpha, calpha in zip(self.alphas,self.calphas):
            n1=sum([dist>calpha for dist in dists])
            n2=sum([dist>calpha for dist in dists2])
            n3=sum([dist>calpha for dist in dists3])
            n4=sum([dist>calpha for dist in dists4])
            n4_=sum([dist>calpha for dist in dists4_])
            data.append((alpha,calpha,n1,n2,n3,n4,n4_))
            labels.append(alpha*NC)
        fname="tabPowerNull.tex"
        lTable(labels,labelsh,data,caption,table_dir+fname)
        print("table {} written at {}".format(fname,table_dir))

    def makeNormalDifferencesDispersion(self,NC,NE,NE2,NB,table_dir):
        xxN=n.linspace(.5,2,16,endpoint=True)
        distsAllN=[[kolmogorovSmirnovDistance_(
                n.random.normal(0,xxx,NE),n.random.normal(0,1,NE2)) for i in range(NC)]
                for xxx in xxN]
        distsAllNC=[[i[0] for i in j] for j in distsAllN]
        dnns=[[i[2] for i in j] for j in distsAllN]
        distsAllN_=[(n.mean(dd),n.std(dd),
            ("{:.3f},"*3)[:-1].format(*min3(dd)),
            ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllNC]
        i=0
        labels=xxN
        labelsh=[r"$\sigma$",r"$\mu(c)$",r"$\sigma(c)$",r"$min(c)$",r"$max(c)$","$D$",r"$\mu(D_{F,F'})$",r"$\sigma(D_{F,F'})$"]
        data=distsAllN_
        caption=r"""Measurements of $c$ through simulations
        with normal distributions.
        One normal distribution is fixed, with $\mu=0$ and $\sigma=1$,
        and compared agaist normal distributions with $\mu=0$
        and different values of $\sigma$."""
        data_=[]
        i=0
        for dists in distsAllNC:
            line=[]
            dnn=dnns[i]
            kline=[dnnNorm(0,1,0,xxN[i],-4,4), n.mean(dnn), n.std(dnn)]
            for calpha in self.calphas:
                line.append(sum([dist>calpha for dist in dists])/NC)
            data_.append(list(data[i])+kline+line); i+=1
        labelsh+=[r"$\overline{{C({})}}$".format(alpha) for alpha in self.alphas]
        fname="tabNormDiffDispersion.tex"
        lTable(labels,labelsh,data_,caption,table_dir+fname,"kolmDiff3_")
        print("table {} written at {}".format(fname,table_dir))

    def makeNormalDifferencesMean(self,NC,NE,NE2,NB,table_dir):
        xxN2=n.linspace(0,1,11,endpoint=True)
        labels=xxN2
        distsAllN2=[[kolmogorovSmirnovDistance_(
                n.random.normal(xxx,1,NE),n.random.normal(0,1,NE2)) for i in range(NC)]
                for xxx in xxN2]
        distsAllNC2=[[i[0] for i in j] for j in distsAllN2]
        dnns=[[i[2] for i in j] for j in distsAllN2]
        data2=[(n.mean(dd),n.std(dd),
            ("{:.3f},"*3)[:-1].format(*min3(dd)),
            ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllNC2]
        data2_=[]
        i=0
        for dists in distsAllNC2:
            line=[]
            dnn=dnns[i]
            kline=[dnnNorm(0,1,xxN2[i],1,-4,8), n.mean(dnn), n.std(dnn)]
            for calpha in self.calphas:
                line.append(sum([dist>calpha for dist in dists])/NC)
            data2_.append(list(data2[i])+kline+line); i+=1
        caption=r"""Measurements of $c$ through simulations
        with normal distributions.
        One normal distribution is fixed, with $\mu=0$ and $\sigma=1$,
        and compared agaist normal distributions with different values of $\mu$ and fixed $\sigma=1$."""

        labelsh=[r"$\mu$",r"$\mu(c)$",r"$\sigma(c)$","$min(c)$","$max(c)$","$D$",r"$\mu(D_{F,F'})$",r"$\sigma(D_{F,F'})$"]
        labelsh+=[r"$\overline{{C({})}}$".format(alpha) for alpha in self.alphas]
        fname="tabNormDiffMean.tex"
        lTable(labels,labelsh,data2_,caption,table_dir+fname,"kolmDiff3_")
        print("table {} written at {}".format(fname,table_dir))
    def makeUniformDifferencesDispersion(self,NC,NE,NE2,NB,table_dir):
        xx=n.arange(.70,1.35,0.05)
        labels=xx
        distsAll=[[kolmogorovSmirnovDistance_(
                xxx*n.random.random(NE),n.random.random(NE2)) for i in range(NC)]
                for xxx in xx]
        distsAllC=[[i[0] for i in j] for j in distsAll]
        dnns=[[i[2] for i in j] for j in distsAll]
        data=[(n.mean(dd),n.std(dd),
            ("{:.3f},"*3)[:-1].format(*min3(dd)),
            ("{:.3f},"*3)[:-1].format(*max3(dd)) ) for dd in distsAllC]
        data_=[]
        i=0
        for dists in distsAllC:
            line=[]
            dnn=dnns[i]
            kline=[dnnUni(0,xx[i],0,1,0,1.5), n.mean(dnn), n.std(dnn)]
            for calpha in self.calphas:
                line.append(sum([dist>calpha for dist in dists])/NC)
            data_.append(list(data[i])+kline+line); i+=1
        caption=r"""Measurements of $c$ through simulations
        with uniform distributions.
        One uniform distribution has the fixed domain $[0,1)$.
        The other uniform distribution in each comparison
        is also centered around 0.5,
        but spread over $b=b_u-b_l$ there $b_l$ and $b_u$ are the lower and upper boudaries."""

        labelsh=[r"$b$",r"$\mu(c)$",r"$\sigma(c)$","min(c)","max(c)","$D$",r"$\mu(D_{F,F'})$",r"$\sigma(D_{F,F'})$"]
        labelsh+=[r"$\overline{{C({})}}$".format(alpha) for alpha in self.alphas]
        fname="tabUniformDiffSpread.tex"
        lTable(labels,labelsh,data_,caption,table_dir+fname,"kolmDiff3_")
        i=0
        check("table {} written at {}".format(fname,table_dir))

    def makeUniformDifferencesMean(self,NC,NE,NE2,NB,table_dir):
        xx=n.arange(.0,.65,0.05)
        labels=xx+.5
        distsAll=[[kolmogorovSmirnovDistance_(
                n.random.random(NE)+xxx,n.random.random(NE2)) for i in range(NC)]
                for xxx in xx]
        distsAllC=[[i[0] for i in j] for j in distsAll]
        dnns=[[i[2] for i in j] for j in distsAll]
        data=[(n.mean(dd),n.std(dd),
            ("{:.3f},"*3)[:-1].format(*min3(dd)),
            ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllC]
        data_=[]
        i=0
        for dists in distsAllC:
            line=[]
            dnn=dnns[i]
            kline=[dnnUni(xx[i],1+xx[i],0,1,0,1.5), n.mean(dnn), n.std(dnn)]
            for calpha in self.calphas:
                line.append(sum([dist>calpha for dist in dists])/NC)
            data_.append(list(data[i])+kline+line); i+=1
        caption=r"""Measurements of $c$ through simulations
        with uniform distributions.
        One uniform distribution has the fixed domain $[0,1)$.
        The other uniform distribution in each comparison
        have varied mean values but always
        spread over a fixed $b=b_u-b_l$ there $b_l$ and $b_u$ are the lower and upper boudaries."""

        labelsh=[r"$\mu$",r"$\mu(c)$",r"$\sigma(c)$","min(c)","max(c)","$D$",r"$\mu(D_{F,F'})$",r"$\sigma(D_{F,F'})$"]
        labelsh+=[r"$\overline{{C({})}}$".format(alpha) for alpha in self.alphas]
        fname="tabUniformDiffMean.tex"
        lTable(labels,labelsh,data_,caption,table_dir+fname,"kolmDiff3_")
        i=0
        check("table {} written at {}".format(fname,table_dir))
    def makeWeibullDifferencesShape(self,NC,NE,NE2,NB,table_dir):
        #xx=n.hstack(([0.01],n.arange(.10,3.,0.2)))
        #xx=n.arange(.3,3.,0.2)
        xx=n.arange(.7,3.,0.2)
        labels=xx
        distsAllW=[[kolmogorovSmirnovDistance_(
                n.random.weibull(xxx,NE),n.random.weibull(1.5,NE2),30000) for i in range(NC)]

                for xxx in xx]
        distsAllWC=[[i[0] for i in j] for j in distsAllW]
        dnns=[[i[2] for i in j] for j in distsAllW]
        data=[(n.mean(dd),n.std(dd),
            ("{:.3f},"*3)[:-1].format(*min3(dd)),
            ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllWC]
        data_=[]
        i=0
        for dists in distsAllWC:
            line=[]
            dnn=dnns[i]
            kline=[dnnWeib(1.5,xx[i],0.000001,10), n.mean(dnn), n.std(dnn)]
            for calpha in self.calphas:
                line.append(sum([dist>calpha for dist in dists])/NC)
            data_.append(list(data[i])+kline+line); i+=1
        caption=r"""Measurements of $c$ through simulations
        with 1-parameter Weibull distributions.
        One Weibull distribution has the fixed shape parameter $a=1.5$.
        The other Weibull distribution in each comparison
        has varied values of $a$."""

        labelsh=[r"$a$",r"$\mu(c)$",r"$\sigma(c)$","min(c)","max(c)","$D$",r"$\mu(D_{F,F'})$",r"$\sigma(D_{F,F'})$"]
        labelsh+=[r"$\overline{{C({})}}$".format(alpha) for alpha in self.alphas]
        fname="tabWeibullDiffShape.tex"
        lTable(labels,labelsh,data_,caption,table_dir+fname,"kolmDiff3_")
        check("table {} written at {}".format(fname,table_dir))
    def makePowerDifferencesShape(self,NC,NE,NE2,NB,table_dir):
        xx=n.arange(.7,2.7,0.2)
        labels=xx
        distsAllW=[[kolmogorovSmirnovDistance_(
                n.random.power(xxx,NE),n.random.power(1.5,NE2)) for i in range(NC)]

                for xxx in xx]
        distsAllWC=[[i[0] for i in j] for j in distsAllW]
        dnns=[[i[2] for i in j] for j in distsAllW]
        data=[(n.mean(dd),n.std(dd),
            ("{:.3f},"*3)[:-1].format(*min3(dd)),
            ("{:.3f},"*3)[:-1].format(*max3(dd))) for dd in distsAllWC]
        data_=[]
        i=0
        for dists in distsAllWC:
            line=[]
            dnn=dnns[i]
            kline=[dnnPower(1.5,xx[i],-10,10), n.mean(dnn), n.std(dnn)]
            for calpha in self.calphas:
                line.append(sum([dist>calpha for dist in dists])/NC)
            data_.append(list(data[i])+kline+line); i+=1
        caption=r"""Measurements of $c$ through simulations
        with power function distributions.
        One power distribution has the fixed exponent parameter $1-a=2.5$.
        The other power function distribution in each comparison
        has varied values of $a$."""
        labelsh=[r"$a$",r"$\mu(c)$",r"$\sigma(c)$","min(c)","max(c)","$D$",r"$\mu(D_{F,F'})$",r"$\sigma(D_{F,F'})$"]
        labelsh+=[r"$\overline{{C({})}}$".format(alpha) for alpha in self.alphas]
        fname="tabPowerDiffShape.tex"
        lTable(labels,labelsh,data_,caption,table_dir+fname,"kolmDiff3_")
        i=0
        check("table {} written at {}".format(fname,table_dir))
    def notes(self):
        print("""#############
## região crítica?
# hipótese nula?
# distribuições chi-square? lei de potência?
# Kolmogorov-Smirnov distances? https://pypi.python.org/pypi/powerlaw
# discrete cases? http://www.itl.nist.gov/div898/handbook/eda/section3/eda35g.htm
# KS statistics == KS distance?
# bootstrap resampling ... e ... ad hoc
# D statistic, p-value
# the Kolmogorov-Smirnov goodness-of-fit is the D statistic and the KS distance?
# medir Fisher information?

# Another advantage is that it is an exact test (the chi-square goodness-of-fit test depends on an adequate sample size for the approximations to be valid) http://www.itl.nist.gov/div898/handbook/eda/section3/eda35g.htm
# Note that although the K-S test is typically developed in the context of continuous distributions for uncensored and ungrouped data, the test has in fact been extended to discrete distributions and to censored and grouped data.
# We do not discuss those cases here.

# The logarithm transformation may help to overcome cases where the Kolmogorov test data does not seem to fit the assumption that it came from the normal distribution. https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test
# If one chooses a critical value of the test statistic Dα such that P(Dn > Dα) = α, then a band of width ±Dα around Fn(x) will entirely contain F(x) with probability 1 − α.


# boas referências: http://stats.stackexchange.com/questions/411/motivation-for-kolmogorov-distance-between-distributions
# Most Monte Carlo studies show that the Anderson-Darling test is more powerful than the Kolmogorov-Smirnov test. It is available in scipy.stats with critical values, and in statsmodels with approximate p-values:

# often not very sensitive in establishing distances between two distributions, and a similar EDF-based test gives a better performance. https://asaip.psu.edu/Articles/beware-the-kolmogorov-smirnov-test
# The Anderson-Darling (AD) test was developed in the 1950s as a weighted CvM test to overcome both of these problems. 
# from scipy.stats import anderson_ksamp
# Bootstrap resampling is conceptually and computationally simple, and the theory underlying the bootstrap guarantee that the resulting significance levels are unbiased for a wide range of situations.

# In R you can also do a bootstrapped KS test sekhon.berkeley.edu/matching/ks.boot.html which gets rid of the continuity requirement – Dr G http://stats.stackexchange.com/questions/13326/can-i-use-kolmogorov-smirnov-to-compare-two-empirical-distributions

# >>> sm.stats.normal_ad(x)
# (0.23016468240712129, 0.80657628536145665)

    # https://en.wikipedia.org/wiki/Anderson%E2%80%93Darling_test""")
    def readme(self):
        return "clone this repo https://github.com/ttm/kolmogorov-smirnov\n and use the path to render the tables in this class"
