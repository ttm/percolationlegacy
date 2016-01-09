__doc__="fit of arbitrary data to a power-law distribution"
def fitData(data):
    c("plaw fit start: "+ dist)
    fit=powerlaw.Fit(data,discrete=True)
    c("plaw fit end: "+ dist)

    dists=list(self.aa[0].power_res.supported_distributions.keys())
    dists.remove("power_law")
    for dist in dists:
        c("plaw compare start: "+ dist)
        comp=powerlaw_fit.distribution_compare("power_law",dist)
        exec("fit.{}_R=comp[0]".format(dist)
        exec("fit.{}_p=comp[1]".format(dist)
        c("plaw compare end: "+ dist)

    del dist,comp
    return locals

