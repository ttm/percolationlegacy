__doc__="for finding Erdos sectors of a network"
def getErdosSectorsUsers(self,minimum_incidence=2):
    t=self.topm_dict
    max_degree_empirical=max(t["degrees_"])
    prob=t["nedges"]/(t["nnodes"]*(t["nnodes"]-1)) # edge probability
    self.max_degree_possible=2*(t["nnodes"]-1) # max d given N
    d_=list(set(t["degrees_"]))
    d_.sort()
    sectorialized_degrees__= self.newerSectorializeDegrees(
                                  self.makeEmpiricalDistribution(
                                    t["degrees_"], d_, t["nnodes"] ),
          stats.binom(self.max_degree_possible,prob),
          d_,
          max_degree_empirical,
          minimum_incidence,t["nnodes"])
    sectorialized_agents__= self.sectorializeAgents(
         sectorialized_degrees__, t["degrees"])
    sectorialized_nagents__=[len(i) for i in sectorialized_agents__]
    #mvars=("prob","max_degree_empirical","sectorialized_degrees__","sectorialized_agents__")
    del t
    self.topm_dict.update(locals())
def sectorializeAgents(self,sectorialized_degrees,agent_degrees):
    periphery=[x for x in agent_degrees
                 if agent_degrees[x] in sectorialized_degrees[0]]
    intermediary=[x for x in agent_degrees
                 if agent_degrees[x] in sectorialized_degrees[1]]
    hubs=[x for x in agent_degrees
                 if agent_degrees[x] in sectorialized_degrees[2]]
    return locals()
def newerSectorializeDegrees(self,empirical_distribution,binomial,incident_degrees_,max_degree_empirical,minimum_count,num_agents):
    # compute bins [start, end]
    prob_min=minimum_count/num_agents
    llimit=0
    rlimit=0
    self.bins=bins=[]
    self.empirical_probs=empirical_probs=[]
    while (rlimit < len(incident_degrees_)):
        if (sum(empirical_distribution[llimit:])>prob_min):
            prob_empirical=0
            while True:
                prob_empirical=sum(
                     empirical_distribution[llimit:rlimit+1] )
                if prob_empirical >= prob_min:
                    break
                else:
                    rlimit+=1
            bins.append((llimit,rlimit))
            empirical_probs.append(prob_empirical)
            rlimit+=1
            llimit=rlimit
        else: # last bin
            print("last bin less probable than prob_min")
            rlimit=len(incident_degrees_)-1
            bins.append((llimit,rlimit))
            prob_empirical=sum(
                 empirical_distribution[llimit:rlimit+1] )
            empirical_probs.append(prob_empirical)
            rlimit+=1

    binomial_probs=[]
    for i, bin_ in enumerate(bins):
        llimit=bin_[0]
        rlimit=bin_[1]
        ldegree=incident_degrees_[llimit]-1
        rdegree=incident_degrees_[rlimit]
        binomial_prob=binomial.cdf(rdegree)-binomial.cdf(ldegree)
        binomial_probs.append(binomial_prob)

    # calcula probabilidades em cada bin
    # compara as probabilidades
    distribution_compare = list(n.array(empirical_probs) < n.array(binomial_probs))
    self.binomial_probs=binomial_probs
    self.distribution_compare0=distribution_compare
    if sum(distribution_compare):
        tindex= distribution_compare.index(True)
        tindex2=distribution_compare[::-1].index(True)
        periphery_degrees=incident_degrees_[:tindex]
        intermediary_degrees=incident_degrees_[tindex:-tindex2]
        hub_degrees=         incident_degrees_[-tindex2:]
    else:
        periphery_degrees=incident_degrees_[:]
        intermediary_degrees=[]
        hub_degrees=[]

    return periphery_degrees, intermediary_degrees, hub_degrees

def makeEmpiricalDistribution(self, incident_degrees, incident_degrees_, N):
    empirical_distribution=[]
    for degree in incident_degrees_:
        empirical_distribution.append(incident_degrees.count(degree)/N)
    return empirical_distribution
