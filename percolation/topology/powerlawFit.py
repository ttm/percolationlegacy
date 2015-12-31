__doc__="fit of arbitrary data to a power-law distribution"
def fitData(data):
    powerlaw_fit=powerlaw.Fit(data,discrete=True)

    data=[powerlaw_fit.alpha,powerlaw_fit.xmin,powerlaw_fit.D,powerlaw_fit.sigma,powerlaw_fit.noise_flag]
    dcomp=[]

    dists=list(self.aa[0].power_res.supported_distributions.keys())
    dists.remove("power_law")
    for dist in dists:
        c("plaw compare: "+ dist)
        dcomp+=list(powerlaw_fit.distribution_compare("power_law",dist))
    data+=dcomp
    del dist,dcomp
    return locals

