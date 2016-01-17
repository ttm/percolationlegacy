import networkx as x, pylab as p, numpy as n, os

import moviepy.editor as mpy, music as m
UT=m.Utils()
bt=m.BasicTables()
co=m.BasicConverter()
sy=m.Synth()
sy.adsrSetup(A=20,D=20,R=10)

class FSong:
    """Create song from undirected (friendship) network
    """
    def __init__(self, network,basedir="fsong/",clean=False,render_images=False,render_images2=False,make_video=False):
        os.system("mkdir {}".format(basedir))
        if clean:
            os.system("rm {}*".format(basedir))
        self.basedir=basedir
        self.network=network
        self.makePartitions()
        if render_images:
            self.makeImages()
        self.make_video=make_video
        self.makeSong()
        if render_images2:
            self.makeImages2()
            self.makeSong2()
    def makeSong2(self):
        pass
    def makePartitions(self):
        """Make partitions with gmane help.
        """
        class NetworkMeasures:
            pass
        self.nm=nm=NetworkMeasures()
        nm.degrees=self.network.degree()
        nm.nodes_= sorted(self.network.nodes(), key=lambda x : nm.degrees[x])
        nm.degrees_=[nm.degrees[i] for i in nm.nodes_]
        nm.edges=     self.network.edges(data=True)
        nm.E=self.network.number_of_edges()
        nm.N=self.network.number_of_nodes()
        self.np=g.NetworkPartitioning(nm,10,metric="g")
    def makeImages(self):
        """Make spiral images in sectors and steps.

        Plain, reversed,
        sectorialized, negative sectorialized
        outline, outline reversed, lonely
        only nodes, only edges, both
        """
        # make layout
        self.makeLayout()
        self.setAgraph()
        # make function that accepts a mode, a sector
        # and nodes and edges True and False
        self.plotGraph()
        self.plotGraph("reversed",filename="tgraphR.png")
        agents=n.concatenate(self.np.sectorialized_agents__)
        for i, sector in enumerate(self.np.sectorialized_agents__):
            self.plotGraph("plain",   sector,"sector{:02}.png".format(i))
            self.plotGraph("reversed",sector,"sector{:02}R.png".format(i))
            self.plotGraph("plain", n.setdiff1d(agents,sector),"sector{:02}N.png".format(i))
            self.plotGraph("reversed",n.setdiff1d(agents,sector),"sector{:02}RN.png".format(i))
        self.plotGraph("plain",   [],"BLANK.png")
    def makeImages2(self):
        for i, node in enumerate(self.nm.nodes_):
            self.plotGraph("plain",   [node],"lonely{:09}.png".format(i))
            self.plotGraph("reversed",[node],"lonely{:09}R.png".format(i))
            self.plotGraph("plain",   self.nm.nodes_[:i],"stair{:09}.png".format(i))
            self.plotGraph("reversed",self.nm.nodes_[:i],"stair{:09}R.png".format(i))
        # plotar novamente usando somente vertices e depois somente arestas

    def plotGraph(self,mode="plain",nodes=None,filename="tgraph.png"):
        """Plot graph with nodes (iterable) into filename
        """
        if nodes==None:
            nodes=self.nodes
        else:
            nodes=[i for i in self.nodes if i in nodes]
        for node in self.nodes:
            n_=self.A.get_node(node)
            if mode=="plain":
                nmode=1
            else:
                nmode=-1
            pos="{},{}".format(self.xi[::nmode][self.nm.nodes_.index(node)],self.yi[::nmode][self.nm.nodes_.index(node)])
            n_.attr["pos"]=pos
            n_.attr["pin"]=True
            color='#%02x%02x%02x' % tuple([255*i for i in self.cm[int(self.clustering[n_]*255)][:-1]])
            n_.attr['fillcolor']= color
            n_.attr['fixedsize']=True
            n_.attr['width']=  abs(.1*(self.nm.degrees[n_]+  .5))
            n_.attr['height']= abs(.1*(self.nm.degrees[n_]+.5))
            n_.attr["label"]=""
            if node not in nodes:
                n_.attr["style"]="invis"
            else:
                n_.attr["style"]="filled"
        for e in self.edges:
            e.attr['penwidth']=3.4
            e.attr["arrowsize"]=1.5
            e.attr["arrowhead"]="lteeoldiamond"
            e.attr["style"]=""
            if sum([i in nodes for i in (e[0],e[1])])==2:
                e.attr["style"]=""
            else:
                e.attr["style"]="invis"
        tname="{}{}".format(self.basedir,filename)
        print(tname)
        self.A.draw(tname,prog="neato")

    def setAgraph(self):
        self.A=x.to_agraph(self.network)
        self.A.graph_attr["viewport"]="500,500,.03"
        self.edges=self.A.edges()
        self.nodes=self.A.nodes()
        self.cm=p.cm.Reds(range(2**10)) # color table
        self.clustering=x.clustering(self.network)
    def makeLayout(self):
        ri=4
        rf=100
        nturns=3
        ii=n.linspace(0,nturns*2*n.pi,self.nm.N)
        rr=n.linspace(ri,rf,self.nm.N)
        self.xi=(rr*n.cos(ii))
        self.yi=(rr*n.sin(ii))

    def makeSong(self):
        """Render abstract animation
        """
        self.makeVisualSong()
        self.makeAudibleSong()
        if self.make_video:
            self.makeAnimation()
    def makeVisualSong(self):
        """Return a sequence of images and durations.
        """
        self.files=os.listdir(self.basedir)
        self.stairs=[i for i in self.files if ("stair" in i) and ("R" in i)]
        self.sectors=[i for i in self.files if "sector" in i]
        self.stairs.sort()
        self.sectors.sort()
        filenames=[self.basedir+i for i in self.sectors[:4]]
        self.iS0=mpy.ImageSequenceClip(filenames,durations=[1.5,2.5,.5,1.5])
        self.iS1=mpy.ImageSequenceClip(
                          [self.basedir+self.sectors[2],
                           self.basedir+self.sectors[3],
                           self.basedir+self.sectors[2],
                           self.basedir+self.sectors[3],
                           self.basedir+self.sectors[2],
                           self.basedir+self.sectors[3],
                           self.basedir+self.sectors[2],
                           self.basedir+self.sectors[3]],
                durations=[0.25]*8)
        self.iS2=mpy.ImageSequenceClip(
                          [self.basedir+self.sectors[2],
                           self.basedir+self.sectors[3],
                           self.basedir+self.sectors[2],
                           self.basedir+self.sectors[3],
                           self.basedir+self.sectors[0]],
                durations=[0.75,0.25,0.75,0.25,2.]) # cai para sensível

        self.iS3=mpy.ImageSequenceClip(
                          [self.basedir+"BLANK.png",
                           self.basedir+self.sectors[0],
                           self.basedir+self.sectors[1],
                           self.basedir+self.sectors[1],
                           self.basedir+self.sectors[1],
                           self.basedir+self.sectors[0],
                           self.basedir+self.sectors[0]],
                durations=[1,0.5,2.,.25,.25,1.75, 0.25]) # [-1,8]

        self.iS4=mpy.ImageSequenceClip(
                          [self.basedir+self.sectors[2], # 1
                           self.basedir+self.sectors[3], # .5
                           self.basedir+self.sectors[5], # .5
                           self.basedir+self.sectors[2], # .75
                           self.basedir+self.sectors[0], #.25
                           self.basedir+self.sectors[2], # 1
                           self.basedir+self.sectors[0], # 2 8
                           self.basedir+self.sectors[3], # 2 7
                           self.basedir+self.sectors[0], # 2 -1
                          self.basedir+"BLANK.png",# 2
                           ],
                durations=[1,0.5,0.5,.75,
                              .25,1., 2.,2.,2.,2.]) # [0,7,11,0]

        self.iS=mpy.concatenate_videoclips((
            self.iS0,self.iS1,self.iS2,self.iS3,self.iS4))
        # Clip with three first images3
        # each sector a sound
        # sweep from periphery to center
        # all, all inverted
        # sectors with inversions
    def makeAudibleSong(self):
        """Use mass to render wav soundtrack.
        """
        sound0=n.hstack((sy.render(220,d=1.5),
                        sy.render(220*(2**(7/12)),d=2.5),
                        sy.render(220*(2**(-5/12)),d=.5),
                        sy.render(220*(2**(0/12)),d=1.5),
                        ))
        sound1=n.hstack((sy.render(220*(2**(0/12)),d=.25),
                         sy.render(220*(2**(7/12)),d=.25),
                         sy.render(220*(2**(0/12)),d=.25),
                         sy.render(220*(2**(7/12)),d=.25),
                         sy.render(220*(2**(0/12)),d=.25),
                         sy.render(220*(2**(7/12)),d=.25),
                         sy.render(220*(2**(0/12)),d=.25),
                         sy.render(220*(2**(7/12)),d=.25),
                        ))
        sound2=n.hstack((sy.render(220*(2**(0/12)),d=.75),
                         sy.render(220*(2**(0/12)),d=.25),
                         sy.render(220*(2**(7/12)),d=.75),
                         sy.render(220*(2**(0/12)),d=.25),
                         sy.render(220*(2**(-1/12)),d=2.0),
                       ))
        sound3=n.hstack((n.zeros(44100),
                         sy.render(220*(2**(-1/12)),d=.5),
                         sy.render(220*(2**(8/12)),d=2.),
                         sy.render(220*(2**(8/12)),d=.25),
                         sy.render(220*(2**(8/12)),d=.25),
                         sy.render(220*(2**(-1/12)),d=1.75),
                         sy.render(220*(2**(-1/12)),d=.25),
                       ))
        sound4=n.hstack((
                         sy.render(220*(2**(0/12)),d=1.),
                         sy.render(220*(2**(7/12)),d=.5),
                         sy.render(220*(2**(11/12)),d=.5),
                         sy.render(220*(2**(12/12)),d=.75),
                         sy.render(220*(2**(11/12)),d=.25),
                         sy.render(220*(2**(12/12)),d=1.),
                         sy.render(220*(2**(8/12)),d=2.),
                         sy.render(220*(2**(7/12)),d=2.),
                         sy.render(220*(2**(-1/12)),d=2.),
                         n.zeros(2*44100)
                       ))

        sound=n.hstack((sound0,sound1,sound2,sound3,sound4))
        UT.write(sound,"sound.wav")
    def makeAnimation(self):
        """Use pymovie to render (visual+audio)+text overlays.
        """
        aclip=mpy.AudioFileClip("sound.wav")
        self.iS=self.iS.set_audio(aclip)
        self.iS.write_videofile("mixedVideo.webm",15,audio=True)
        print("wrote "+"mixedVideo.webm")
