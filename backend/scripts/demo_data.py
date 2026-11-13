DEMO_NODES=[{'node_id':'Fault','label':'故障假设','parents':[]},{'node_id':'Power','label':'供给异常假设','parents':[]},{'node_id':'Heat','label':'温升表征','parents':['Fault','Power']},{'node_id':'Vibration','label':'振动表征','parents':['Fault']},{'node_id':'Alarm','label':'告警表征','parents':['Heat','Vibration']},{'node_id':'Indicator','label':'弱指示表征','parents':['Power']},{'node_id':'Lock','label':'演练确定标记','parents':['Fault']}]
DEMO_CPT=[]
for node,values,probability in [('Fault',[],.15),('Power',[],.08),('Heat',[0,0],.05),('Heat',[0,1],.45),('Heat',[1,0],.75),('Heat',[1,1],.9),('Vibration',[0],.08),('Vibration',[1],.8),('Alarm',[0,0],.02),('Alarm',[0,1],.6),('Alarm',[1,0],.75),('Alarm',[1,1],.95),('Indicator',[0],.45),('Indicator',[1],.55),('Lock',[0],0),('Lock',[1],1)]:DEMO_CPT.append({'node_id':node,'parent_values':values,'p0':1-probability,'p1':probability})
HAND_NODES=[{'node_id':'F','label':'手算故障','parents':[]},{'node_id':'S','label':'手算表征','parents':['F']}]
HAND_CPT=[{'node_id':'F','parent_values':[],'p0':.8,'p1':.2},{'node_id':'S','parent_values':[0],'p0':.9,'p1':.1},{'node_id':'S','parent_values':[1],'p0':.2,'p1':.8}]
TINY_NODES=[{'node_id':n,'label':n,'parents':[]} for n in ['A','B','Q']]
TINY_CPT=[{'node_id':n,'parent_values':[],'p0':1. if n!='Q' else .8,'p1':1e-200 if n!='Q' else .2} for n in ['A','B','Q']]
