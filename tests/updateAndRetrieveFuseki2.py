import percolation as P
mq=P.utils.mQuery
u= "http://200.144.255.210:8082/dsfoo/query"
u2="http://200.144.255.210:8082/dsfoo/update"
q="SELECT DISTINCT ?{} WHERE {{ GRAPH ?g {{ }} }}"
v="g"
r=mq(u,q,v)
