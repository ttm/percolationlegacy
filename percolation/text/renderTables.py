__doc__="rendering of latex tables"

def uniteTables(TDIR,tag):
    """vstack tables TTM Deprecated?"""
    t1="geral"#"geralInline0_"
    t2="chars"
    t3="tokensMerged"
    t4="sentences"
    t5="messages"
    def makeN(ss):
        if ss==t3:
            return ss+"Inline{}".format(tag)
        return ss+"Inline{}_".format(tag)
    tt=[TDIR+makeN(i) for i in (t1,t2,t3,t4,t5)]
    foo=TDIR+"mergedA{}".format(tag)
    g.tableHelpers.vstackTables(tt[0],tt[1],foo)
    g.tableHelpers.vstackTables(foo,tt[2],foo)
    g.tableHelpers.vstackTables(foo,tt[3],foo)
    g.tableHelpers.vstackTables(foo,tt[4],foo)
def uniteTables3(TDIR,tag):
    """junta cada POS tag da wn em uma tabelona TTM"""
    tt="wnPOSInline2a","wnPOSInline2b","wnPOSInline2c","wnPOSInline2d",
    fnames=[]
    for pos in ("n","as","v","r"):
    #for pos in ("n",):
        fname=TDIR+"wnPOSInline2-{}-{}".format(pos,tag)
        fnames=[]
        for ttt in tt:
            fnames+=[TDIR+ttt+"-{}-{}tag_".format(pos,tag)]
        if os.path.isfile(fnames[1]+".tex"):
            g.tableHelpers.vstackTables_(fnames[0],fnames[1],fname)
        else:
            shutil.copyfile(fnames[0]+".tex",fname+".tex")
        if os.path.isfile(fnames[2]+".tex"):
            g.tableHelpers.vstackTables_(fname,fnames[2],fname)
        if os.path.isfile(fnames[3]+".tex"):
            g.tableHelpers.vstackTables_(fname,fnames[3],fname)
def uniteTables2(TDIR,tag):
    """vtstack tables TTM Deprecated?"""
    foo=TDIR+"posMerged{}".format(tag)
    g.tableHelpers.vstackTables_(TDIR+"posInline{}_".format(tag),
            TDIR+"wnPOSInline{}_".format(tag),foo)


