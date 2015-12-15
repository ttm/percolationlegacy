import numpy as n, string, re, builtins as B, langid
import gmane as g
def fSize(tablefname,ftag="scriptsize",write=False):
    """Change size of table font"""
    with open(tablefname,"r") as f:
        lines=f.read()
    l=lines.split("\n")
    l.insert(1,ftag)
    l="\n".join(l)
    if not write:
        return l
    else:
        writeTex(l,tablefname)


def doubleLines(tablefname,hlines=["i1","i2"],vlines=["j1","j2"],hlines_=[]):
    """make some double lines in a latex table"""
    with open(tablefname,"r") as f:
        lines=f.read()
    # colocando barras nas linhas verticais
    header=re.findall(r"\\begin{tabular}{(.*)}\\hline\n",lines)[0]
    indexes=[i.start() for i in re.finditer("\|",header)]
    js=vlines
    header_=header[:]
    foo=0
    for j in js:
        j_=indexes[j]+foo
        header_=header_[:j_]+"||"+header_[j_+1:]
        foo+=1
    lines__=lines.replace(header,header_)
    # colocando barras nas linhas horizontais
    linhas=lines__.split("\\hline")
    ii=hlines
    linesF=lines__[:]
    for i in ii:
        linha=linhas[i]
        linha_=linha+"\\hline"
        if lines__.count(linha)==1:
            linesF=linesF.replace(linha,linha_)
        elif lines__.count(linha)>1:
            print("mais de uma linha igual ERRO!!!",tablefname)
        else:
            print("linha não existe!!! ERRO!!",tablefname)
    ii=hlines_
    for i in ii:
        linha=linhas[i]
        if lines__.count(linha)==1:
            linesF=linesF.replace(linha+"\\hline",linha)
        elif lines__.count(linha)>1:
            print("mais de uma linha igual ERRO!!!",tablefname)
        else:
            print("linha não existe!!! ERRO!!",tablefname)
    #linesF=lines__[:]
    return linesF
def markEntries_(tablefname,marker,locs=[("i","j")]):
    with open(tablefname,"r") as f:
        lines=f.read()
    for loc in locs:
        linha=re.findall(r"\\hline\n.*"*loc[0]+r"\\hline\n(.*)\\hline\n",lines)[0]

        elementos=[i.strip() for i in linha.split("&")]
        elementos_=elementos[:]
        elementos_[-1],resto=elementos[-1].split(" ")
        elemento=elementos_[loc[1]]
        elemento_="{{{} {}}}".format(marker,elemento)
        elementos_[loc[1]]=elemento_
        linha_=" & ".join(elementos_)+" "+resto
        if lines.count(linha)==1:
            #print(linha,linha_)
            lines=lines.replace(linha,linha_)
        elif lines.count(linha)>1:
            print("mais de uma linha igual ERRO!!!",tablefname)
        else:
            print("linha não existe!!! ERRO!!",tablefname)
    #print("\n\n\nLINES",lines)
    return lines
def markEntries(table,marker):
    """Make entries in a table boldface or use other markings"""
    # open rendered table as text
    #print("YEAH")
    with open(table,"r") as f:
        lines=f.read()
    lines=lines.split("\n")
    lines[3:-3]=[i.split("&") for i in lines[3:-3]]
    for i,line in enumerate(lines[3:-3]):
        i1,i2=line[-1].split("\\\\\\")
        i2="\\\\\\"+i2
        lines[i+3]=line[:-1]+[i1,i2]
    #print(lines)
    #print(len(lines[0]))
    for column in range(1,len(lines[3])-1):
        #print("column")
        values=[]
        for linei in range(3,len(lines)-3):
            if lines[linei][column].strip(): # can be empty
                value=float(lines[linei][column].split("{")[-1].split("}")[0])
                values.append(value)
        #print(values)
        mav=max(values)
        miv=min(values)
        #print(mav,miv)
        for linei in range(3,len(lines)-3):
            if lines[linei][column].strip(): # can be empty
                orig="{:.2f}".format(mav)
                tnew="\\{}{{ {} }}".format(marker,mav)
                #print(orig,tnew)
                lines[linei][column]=lines[linei][column].replace(orig,tnew)
    lines=lines[:3]+[" & ".join(line[:-1])+line[-1] for line in lines[3:-3]]+lines[-3:]
    lines=" \n ".join(lines)
    writeTex(lines,table.replace(".tex","_.tex"))
    # find maximum and minimum in each row
    # boldface them all
    return lines
def encapsulateTable(string_table,column_labels, caption,ttype=None):
    """Uses the output of makeTables to render a complete latex table"""
    if ttype in ("kolmDiff3","kolmDiff3_","kolmSamp_","kolmSamp","textCorr"):
        header="\\begin{table*}[h!]\n\\begin{center}\n\\begin{tabular}{| l |"+" c |"*(string_table.split("hline")[0].count("&")) +"}\\hline\n"
    elif ttype=="audioDistances":
        header="\\begin{table*}[h!]\n\\begin{center}\n\\begin{tabular}{| l |"+" c |"*(string_table.split("hline")[0].count("&")) +"}\\hline\n"
    elif ttype=="textsDistances":
        header="\\begin{table*}[h!]\n\\begin{center}\n\\begin{tabular}{| l |"+" c |"*(string_table.split("hline")[0].count("&")) +"}\\hline\n"
    elif ttype=="textsGeneral":
        header="\\begin{table*}[h!]\n\\begin{center}\n\\begin{tabular}{| l |"+" c |"*(string_table.split("hline")[0].count("&")) +"}\\hline\n"
    else:
        header="\\begin{table}[h!]\n\\begin{center}\n\\begin{tabular}{| l |"+" c |"*(string_table.split("hline")[0].count("&")) +"}\\hline\n"
#    header+="\\footnotesize"
    if column_labels:
        header+=("& {} "*len(column_labels)+"\\\\\\hline\n").format(*column_labels)[2:]
    if "tag" in dir(B):
        caption+=" TAG: {}".format(B.tag)
    caption_="\\caption{{{}}}\n".format(caption)
    if ttype in ("kolmDiff3","kolmDiff3_","kolmSamp_","kolmSamp","textCorr"):
        footer="\\end{{tabular}}\n{}\\end{{center}}\n\\end{{table*}}".format(caption_)
    elif ttype=="audioDistances":
        footer="\\end{{tabular}}\n{}\\end{{center}}\n\\end{{table*}}".format(caption_)
    elif ttype=="textsGeneral":
        footer="\\end{{tabular}}\n{}\\end{{center}}\n\\end{{table*}}".format(caption_)
    elif ttype=="textsDistances":
        footer="\\end{{tabular}}\n{}\\end{{center}}\n\\end{{table*}}".format(caption_)
    else:
        footer="\\end{{tabular}}\n{}\\end{{center}}\n\\end{{table}}".format(caption_)
    table=header+string_table+footer
    return table
def lTable(labels,labelsh,data,caption,filename,ttype="kolmNull"):
    t1=makeTables(labels,data,True,ttype)
    t1_=t1.split("\\hline")[:-1]
    #tvals=[int(float(tt.split("&")[-1].split(" \\\\")[0])) for tt in t1_]
    #print("AQUIIII!!!B",tvals)
    #print(t1)
    #for tval in tvals:
    #    print(str(tval)+".00",str(tval))
    #    t1=t1.replace(" {}.00 ".format(tval)," {} ".format(tval))
    t2=encapsulateTable(t1,labelsh,caption,ttype)
    B.b=(t1,t1_,t2)
    writeTex(t2,filename)
#def makeTables2(data,two_decimal=False):
#    """Variation of makeTables for tables withour row labels"""
def makeTables(labels,data,two_decimal=False,ttype=None):
    """Returns a latex table of data with Label in first column.
    
    Returns latex printable or writable to files to
    be imported by latex files.
    ttype gives a known table type:
    kolmNull for the Kolmogorov-Smirnov Null hypothesis checking.
    """
    if len(labels)!=len(data):
        print("input one label per data row")
        return
    if not two_decimal:
        data="".join([(labels[i]+" & {} "*len(datarow)+"\\\\\\hline\n").format(*datarow) for i, datarow in enumerate(data)])
    else:
        if ttype in ("textCorr","textPCA"):
            data="".join([str(labels[i])+((" & %.2f "*(len(datarow))+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif labels[0]=="$cc$" and len(labels)>10:
            data="".join([((labels[i]+" & %.2f "*len(datarow)+"\\\\\\hline\n")%tuple(datarow)) if labels[i] in ("$cc$","$bt$") else (((labels[i]+" & %.2f "*len(datarow)+"\\\\\n")%tuple(datarow)) if labels[i] != "$\\sigma_{dis}$" else ((labels[i]+" & %.2f "*len(datarow)+"\\\\\\hline\\hline\n")%tuple(datarow))) for i, datarow in enumerate(data)])
        elif ttype=="textGeral_":
            data="".join([str(labels[i])+((" & %.2f "*(len(datarow))+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif ttype=="textCorr":
            data="".join([str(labels[i])+((" & %.2f "*(len(datarow))+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif labels[0]=="$cc$" and len(labels)>5:
            data="".join([((labels[i]+" & %.2f "*len(datarow)+"\\\\\\hline\n")%tuple(datarow)) if labels[i] in ("$cc$",) 
                else 
                       (((labels[i]+" & %.2f "*len(datarow)+"\\\\\n")%tuple(datarow))           if labels[i] != "$bt$" 
                      else 
                          ((labels[i]+" & %.2f "*len(datarow)+"\\\\\\hline\\hline\n")%tuple(datarow))) for i, datarow in enumerate(data)])
        elif labels[0]=="$cc$":
            data="".join([((labels[i]+" & %.2f "*len(datarow)+"\\\\\\hline\n")%tuple(datarow)) if labels[i] in ("$asdaoijsd$",) 
                else 
                       (((labels[i]+" & %.2f "*len(datarow)+"\\\\\n")%tuple(datarow))           if labels[i] != "$bt$" 
                      else 
                          ((labels[i]+" & %.2f "*len(datarow)+"\\\\\\hline\\hline\n")%tuple(datarow))) for i, datarow in enumerate(data)])
        elif ttype=="ksDistances":
            data="".join([((str(labels[i])+" & %.3f "*4 +"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif ttype=="audioDistances":
            data="".join([((str(labels[i])+" & %.3f "*15 +"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif ttype=="textsDistances":
            data="".join([((str(labels[i])+" & %.3f "*12 +"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif ttype in ("audioGeneral","musicGeneral","osGeneral"):
            data="".join([((str(labels[i])+" & %s & %d " +"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif ttype=="textsGeneral":
            data="".join([((str(labels[i])+" & %s & %d & %d & %d & %d & %.3f & %.3f & %d & %.3f & %.3f " +"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif ttype=="kolmSamp":
            data="".join([((str(int(labels[i]))+" & %.3f & %.3f & %.3f & %s & %s "+" & %.3f "*6+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif ttype=="kolmSamp_":
            data="".join([((str(int(labels[i]))+" & %.3f & %.3f & %.3f & %s & %s "+" & %.3f "*8+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif ttype=="kolmDiff3_":
            data="".join([((str(labels[i])+" & %.3f & %.3f & %s & %s "+" & %.3f "*9+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif ttype=="kolmDiff3":
            data="".join([((str(labels[i])+" & %.3f & %.3f & %.3f & %s & %s "+" & %.3f "*6+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif ttype=="textGeral":
            dataFoo="".join([str(labels[:1][i])+((" & %d "*(len(datarow))+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data[:1])])
            data=dataFoo+"".join([str(labels[1:][i])+((" & %.2f "*(len(datarow))+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data[1:])])
        elif ttype=="textGeral__":
            data="".join([str(labels[i])+((" & %d "*(len(datarow))+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif ttype=="kolmDiff2":
            data="".join([((str(labels[i])+" & %.3f "*len(datarow)+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif ttype=="kolmDiff":
            #data="".join([((str(labels[i])+" & %.3f "*16+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
            data="".join([((str(labels[i])+" & %.3f & %.3f & %.3f & %s & %s "+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif ttype=="kolmNull":
            try:
                data="".join([((str(labels[i])+" & %.3f & %.2f "+"& %d "*3+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
            except:
                try:
                    data="".join([((str(labels[i])+" & %.3f & %.2f "+"& %d "*4+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
                except:
                    data="".join([((str(labels[i])+" & %.3f & %.2f "+"& %d "*5+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        elif type(data[0][0])==type("astring"):
            #data="".join([((labels[i]+" & %s "+" & %.2f "*(len(datarow)-1)+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
            data="".join([((labels[i]+" & %s "+" & %.2f "*(len(datarow)-1)+"\\\\\\hline\n")%tuple(datarow)) if type(datarow[0])==type("astring") else ((labels[i]+" & %.2f "*len(datarow)+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data) ])
        else:
            data="".join([((str(labels[i])+" & %.2f "*len(datarow)+"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
    return data

def partialSums(labels, data, partials,partial_labels="",datarow_labels=""):
    """Returns a latex table with sums of data.

    Data is though to be unidimensional. Each row
    is transposed to a column to which partial sum
    are added.
    """

    lines=[]
    for label in labels:
        lines.append("{} ".format(label))
    for datarow in data:
        for partial in partials:
            for line_num in range(len(datarow)):
                if (line_num%partial)==0:
                    lines[line_num]+="& \\multirow{{{:d}}}{{*}}{{ {:.2f} }}  ".format(partial,sum(datarow[line_num:line_num+partial]))
                else:
                    lines[line_num]+="& "

    for line_num in range(len(lines)):
        cuts=[(0==(line_num+1)%partial) for partial in partials]
        i=0
        suffix=""
        for cut in cuts:
            if cut:
                for datarownum in range(len(data)):
                    num=i+(datarownum)*len(partials)
                    suffix+="\\cline{{{}-{}}}".format(num+2,num+2)
            i+=1
        lines[line_num]+="\\\\{}\n".format(suffix)
    
    ltable="".join(lines)

    if partial_labels:
        header=( (" & {}"*len(partial_labels)).format(*partial_labels) )*len(data)+" \\\\\\hline\n"
        ltable=header+ltable
    if datarow_labels:
        header=((" & \\multicolumn{{%i}}{{c|}}{{{}}}"%(len(partials),))*len(datarow_labels)).format(*datarow_labels)+" \\\\\\hline\n"
        ltable=header+ltable
    header="\\begin{center}\n\\begin{tabular}{| l ||"+" c |"*len(data)*len(partials)+"}\\hline\n"
    footer="\\hline\\end{tabular}\n\\end{center}"
    ltable=header+ltable+footer
    return ltable

def pcaTable(labels,vec_mean,vec_std,val_mean,val_std):
    """Make table with PCA formation mean and std"""

    header="\\begin{center}\n\\begin{tabular}{| l |"+" c |"*6+"}\\cline{2-7}\n"
    header+="\\multicolumn{1}{c|}{} & \\multicolumn{2}{c|}{PC1}          & \multicolumn{2}{c|}{PC2} & \multicolumn{2}{c|}{PC3}  \\\\\\cline{2-7}"
    header+="\\multicolumn{1}{c|}{} & $\mu$            & $\sigma$ & $\mu$         & $\sigma$ & $\mu$ & $\sigma$  \\\\\\hline\n"
    tt=n.zeros((vec_mean.shape[0],6))
    tt[:,::2]=vec_mean
    tt[:,1::2]=vec_std
    tt_=n.zeros(6)
    tt_[::2]=val_mean
    tt_[1::2]=val_std
    tab_data=n.vstack((tt,tt_))
    footer="\\hline\\end{tabular}\n\\end{center}"
    table=header + makeTables(labels,tab_data,True) + footer
    return table
def vstackTables_(fname1,fname2,fname3):
    s1=open(fname1+".tex").read()
    s2=open(fname2+".tex").read()
    s1_=re.split("\n\\\\end{tabular",s1)[0]
    s2_=re.split("tabular.*\\hline\n &.*g.*hline",s2)[1]
    writeTex(s1_+"\\hline\\hline"+s2_,fname3+".tex")

def vstackTables(fname1,fname2,fname3):
    s1=open(fname1+".tex").read()
    s2=open(fname2+".tex").read()
    s1_=re.split("\n\\\\end{tabular",s1)[0]
    s2_=re.split("tabular.*\\hline\n &.*g.*hline",s2)[1]
    writeTex(s1_+"\\hline"+s2_,fname3+".tex")
def writeTex(string,filename):
    with open(filename,"w") as f:
        f.write(string)
def dl(fname,hl,vl,hl_=[],over=1):
    fname+=".tex"
    foo=g.doubleLines(fname,hlines=hl,vlines=vl,hlines_=hl_)
    if not over:
        fname=fname.replace(".tex","_.tex")
    g.writeTex(foo,fname)
def me(fname,mark,locs,over=0):
    fn=fname+".tex"
    foo=g.markEntries_(fn,mark,locs)
    if not over:
        fn=fn.replace(".tex","_.tex")
    g.writeTex(foo,fn)


