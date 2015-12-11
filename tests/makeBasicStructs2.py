import rdflib as r, percolation as P
c=P.utils.check

#endpoint_url,relation_uri="200.144.255.210:8082/labMacambiraLaleniaLog2"
fname="AdornoNaoEhEnfeite29032013.gdf"
fname="PartidoPirata23032013.gdf"
fname="DemocraciaPura06042013.gdf"
fname="ComputerArt10032013.gdf"
fname="AtivistasDaInclusaoDigital09032013.gdf"
fname="RedeTranzmidias02032013.gdf"
fnames="AtivistasDaInclusaoDigital09032013.gdf","Coolmeia06032013.gdf","Economia14042013.gdf","DemocraciaDiretaJa14032013.gdf"
fnames="EconomiaCriativaDigital03032013.gdf","PoliticasCulturasBrasileiras08032013.gdf"

fnames=[i[0] for i in
[("Auricultura10042013.gdf","Auricultura10042013_interactions.gdf","373029202732392",0,0),
("CienciasComFronteiras29032013.gdf","CienciasComFronteiras29032013_interacoes.gdf",0,"contraaexclusao","https://www.facebook.com/groups/contraaexclusao/permalink/269103356558439/"),
("LivingBridgesPlanet29032013.gdf","LivingBridgesPlanet29032013_interactions.gdf",0,"livingbridgesplanet","https://www.facebook.com/groups/livingbridgesplanet/permalink/352950408144951/"),
("MobilizacoesCulturaisInteriorSP13032013.gdf","MobilizacoesCulturaisInteriorSP13032013_interacoes.gdf","131639147005593",0,"https://www.facebook.com/groups/131639147005593/permalink/144204529082388/"),
("PracaPopular16032013.gdf","PracaPopular16032013_interactions.gdf","215924991863921",0,"https://www.facebook.com/groups/215924991863921/permalink/319279541528465/"),
("SolidarityEconomy12042013.gdf","SolidarityEconomy12042013_interactions.gdf","9149038282",0,"https://www.facebook.com/groups/9149038282/permalink/10151461945623283/"),
("StudyGroupSNA05042013.gdf","StudyGroupSNA05042013_interactions.gdf","140630009439814",0,"https://www.facebook.com/groups/140630009439814/permalink/151470598355755/"),
("THackDay26032013.gdf","THackDay26032013_interacoes.gdf",0,"thackday",0),
("SiliconValleyGlobalNetwork27042013.gdf","SiliconValleyGlobalNetwork27042013_interactions.gdf","109971182359978",0,"https://www.facebook.com/groups/109971182359978/permalink/589326757757749/"),
("DemocraciaDiretaJa14072013.gdf","DemocraciaDiretaJa14072013_interacoes.gdf",0,"ddjbrasil","https://www.facebook.com/groups/ddjbrasil/permalink/347023325397298/"),
("Tecnoxamanismo08032014.gdf","Tecnoxamanismo08032014_interactions.gdf","505090906188661",0,["https://www.facebook.com/groups/505090906188661/permalink/733144993383250/","https://www.facebook.com/groups/505090906188661/permalink/733157380048678/"]),
("Tecnoxamanismo15032014.gdf","Tecnoxamanismo15032014_interactions.gdf","505090906188661",0,["https://www.facebook.com/groups/505090906188661/permalink/733144993383250/","https://www.facebook.com/groups/505090906188661/permalink/733157380048678/"]),
("Latesfip08032014.gdf","Latesfip08032014_interactions.gdf","183557128478424",0,"https://www.facebook.com/groups/183557128478424/permalink/266610616839741/"),]]
fnames_=[
        ("CalebLuporini25022014.gdf",     None,"1110305437","calebml"),
        ("DanielGonzales23022014.gdf",    None,"100002080034739","daniel.gonzalezxavier"),
        ("JoaoMekitarian23022014.gdf",    None,"100002080034739","joaopaulo.mekitarian"),
        ("MariliaPisani25022014.gdf",     None,"100000812625301","marilia.pisani"),
        ("RenatoFabbri22022014.gdf",      None,"781909429","renato.fabbri"),
        ("FelipeBrait23022014.gdf",       None,"1420435978","felipe.brait"),
        ("JulianaSouza23022014.gdf",      None,"520322516","juliana.desouza2"),
        ("NatachaRena22022014.gdf",       None,"665770837","natacha.rena"),
        ("SarahLuporini25022014.gdf",     None,"1528620900","sarah.cura"),
        ("CamilaBatista23022014.gdf",     None,"100001707143512","camila.batista.3382"),
        ("KarinaGomes22022014.gdf",       None,"100000176551181","karina.gomes.71"),
        ("OrlandoCoelho22022014.gdf",     None,"1060234340","orlando.coelho.98"),
        ("SatoBrasil25022014.gdf",        None,"1060234340","sato.dobrasil"),
        ("CarlosDiego25022014.gdf",       None,"689266676","cdiegosr"),
        ("PalomaKliss25022014.gdf",       None,"100008456088732",0),
        ("CristinaMekitarian23022014.gdf",None,"1771691370","cristina.mekitarian"),
        ("MarcelaLucatelli25022014.gdf",  None,"520656478","justinamoira"),
        ("PedroRocha25022014.gdf",None,"836944624","dpedropaulorocha"),
        ("JoaoMeirelles25022014.gdf",     None,"1194439813","joao.meirelles.10"),
        ("LucasOliveira26022014.gdf",     None,"1060987164",0),
        ]
fnames=[i[0] for i in fnames_]+["MassimoCanevacci19062013.gdf"]

for fname in fnames[-1:]:
    eurl="http://200.144.255.210:8082/dsfoo"
    path="/home/r/repos/social/tests/publishing/fb3/{}_fb/rdf/".format(fname.split(".")[0])
    P.utils.testRdfs(path,eurl,False)

#P.utils.testRdfs(path,eurl,False)
# write to the info, meta or discovery graph about the graphs created

# access this point to retrieve info from other graphs

# make derived structures
relation_uri=P.rdf.ns.fb.friend
#makeNetwork(endpoint_url,relation_uri,label_uri=None,rtype=1,directed=False):



