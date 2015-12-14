import rdflib as r, percolation as P, os
c=P.utils.check
datadir="/disco/data/"
end_url="http://200.144.255.210:8082/dsfoo"
dirs=os.listdir(datadir)
for tdir in dirs:
    umbrelladir=datadir+tdir
    datasetdirs=os.listdir(umbrelladir)
    datasetdirs_=[i for i in datasetdirs if os.path.isdir("{}/{}".format(umbrelladir,i))]
    datasetdirs_=[i for i in datasetdirs_ if not i.startswith(".")]
    for datasetdir in datasetdirs_:
        rdfdir="{}/{}/rdf/".format(umbrelladir,datasetdir)
        files=os.listdir(rdfdir)
        for tfile in files:
            if tfile.endswith(".owl"):
                tfile_=rdfdir+tfile 
                c(tfile_)
                # pegar do Meta o nome do snapshot
                tgraph="http://{}".format(tfile.lower())
                cmd="s-put {} {} {}".format(end_url, tgraph, tfile_)

