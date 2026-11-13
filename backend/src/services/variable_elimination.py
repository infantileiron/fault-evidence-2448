import math
import numpy as np
from scipy.special import logsumexp
from .network_validation import validate_network,validate_cpt,validate_evidence
from .log_factor import cpt_factors,product

def infer(nodes,cpt,evidence,target):
 graph=validate_network(nodes);nodes=graph['nodes'];rows=validate_cpt(nodes,cpt);validate_evidence(nodes,evidence,target)
 factors=[factor.restrict(evidence) for factor in cpt_factors(nodes,rows)];order=sorted({n['node_id'] for n in nodes}-set(evidence)-{target});trace=[]
 for variable in order:
  bucket=[f for f in factors if variable in f.variables];factors=[f for f in factors if variable not in f.variables]
  joined=product(bucket);reduced=joined.sum_out(variable);factors.append(reduced)
  trace.append({'variable':variable,'input_scopes':[list(f.variables) for f in bucket],'product_scope':list(joined.variables),'product_cells':int(joined.values.size),'output_scope':list(reduced.variables),'output_cells':int(reduced.values.size)})
 final=product(factors);log_z=float(logsumexp(final.values))
 if log_z==-math.inf:raise ValueError('不可能证据：logZ=-inf，给定模型下证据概率严格为0')
 if not math.isfinite(log_z):raise ValueError('log证据概率非有限，推理失败')
 z=math.exp(log_z);underflow=z==0
 if target in evidence:log_probabilities=[0. if state==evidence[target] else -math.inf for state in (0,1)]
 else:
  if final.variables!=(target,):raise ValueError('消元后目标作用域异常')
  log_probabilities=(final.values-log_z).tolist()
 posterior=[]
 for state,log_p in enumerate(log_probabilities):
  probability=0. if log_p==-math.inf else math.exp(log_p)
  posterior.append({'state':state,'probability':probability,'log_probability':None if log_p==-math.inf else log_p,'probability_underflow':log_p!=-math.inf and probability==0})
 return {'target':target,'evidence':dict(evidence),'posterior':posterior,'log_evidence':log_z,'evidence_probability':z,'evidence_probability_underflow':underflow,'evidence_possible':True,'elimination_order':order,'trace':trace,'method':'exact variable elimination / log factors + logsumexp','log_base':'natural','probability_sum':math.fsum(p['probability'] for p in posterior),'normalizer':'logZ','note':'exp(logZ)下溢单独标注；只有logZ=-inf为不可能证据。查询已观测时先核对Z再给one-hot。'}
