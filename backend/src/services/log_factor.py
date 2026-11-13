"""Actual log-space factor product, evidence restriction and marginalization."""
from dataclasses import dataclass
import numpy as np
from scipy.special import logsumexp

@dataclass
class LogFactor:
 variables:tuple
 values:np.ndarray
 def restrict(self,evidence):
  index=tuple(evidence[v] if v in evidence else slice(None) for v in self.variables)
  return LogFactor(tuple(v for v in self.variables if v not in evidence),np.asarray(self.values[index],dtype=np.float64))
 def sum_out(self,variable):
  axis=self.variables.index(variable)
  return LogFactor(tuple(v for v in self.variables if v!=variable),np.asarray(logsumexp(self.values,axis=axis),dtype=np.float64))

def product(factors):
 variables=tuple(sorted({v for factor in factors for v in factor.variables}));values=np.zeros((2,)*len(variables),dtype=np.float64)
 for factor in factors:
  ordered=tuple(v for v in variables if v in factor.variables);axes=[factor.variables.index(v) for v in ordered]
  aligned=np.transpose(factor.values,axes) if axes else factor.values
  values=values+aligned.reshape(tuple(2 if v in ordered else 1 for v in variables))
 return LogFactor(variables,np.asarray(values,dtype=np.float64))

def cpt_factors(nodes,rows):
 factors=[]
 for node in nodes:
  variables=tuple(node['parents'])+(node['node_id'],);values=np.full((2,)*len(variables),-np.inf,dtype=np.float64)
  for row in rows:
   if row['node_id']==node['node_id']:
    for state in (0,1):
     p=row['p'+str(state)];values[tuple(row['parent_values'])+(state,)]=np.log(p) if p>0 else -np.inf
  factors.append(LogFactor(variables,values))
 return factors
