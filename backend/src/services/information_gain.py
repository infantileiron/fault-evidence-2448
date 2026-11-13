import math
from .network_validation import validate_evidence
from .variable_elimination import infer

def entropy(posterior):
 return -math.fsum(p['probability']*p['log_probability']/math.log(2) for p in posterior if p['probability']>0)

def information_gain(nodes,cpt,evidence,target,candidates=None,negative_tolerance=1e-10):
 if not math.isfinite(negative_tolerance) or not 0<=negative_tolerance<=1e-8:raise ValueError('IG微负容差须在0–1e-8')
 eligible=validate_evidence(nodes,evidence,target,candidates);baseline=infer(nodes,cpt,evidence,target);h=entropy(baseline['posterior']);items=[]
 for candidate in eligible:
  marginal=infer(nodes,cpt,evidence,candidate);branches=[];terms=[]
  for p in marginal['posterior']:
   if p['log_probability'] is None:
    branches.append({**p,'skipped_zero_probability':True,'conditional_entropy':None,'inference':None});continue
   # A finite log probability can exponentiate to zero. It is still a possible branch.
   conditional=infer(nodes,cpt,{**evidence,candidate:p['state']},target);branch_h=entropy(conditional['posterior']);terms.append(p['probability']*branch_h);branches.append({**p,'skipped_zero_probability':False,'conditional_entropy':branch_h,'inference':conditional})
  expected=math.fsum(terms);raw=h-expected
  if raw < -negative_tolerance:raise ValueError('信息增益出现严重负值，拒绝隐藏数值异常')
  items.append({'node_id':candidate,'prior_entropy':h,'expected_entropy':expected,'raw_information_gain':raw,'information_gain':max(0.,raw),'micro_negative_clipped':raw<0,'negative_tolerance':negative_tolerance,'marginal':marginal,'branches':branches})
 return {'baseline':baseline,'target_entropy':h,'candidates':sorted(items,key=lambda row:(-row['information_gain'],row['node_id'])),'entropy_base':2,'negative_tolerance':negative_tolerance,'method':'expected posterior entropy over binary candidate states','note':'IG=H(Q|E)−ΣP(X|E)H(Q|E,X)，仅未观测非目标节点。严格零概率分支跳过；指数下溢但log概率有限的分支仍计算，仅浮点权重可能为0。只按给定模型研修，不发现因果、不输出维修指令。'}
