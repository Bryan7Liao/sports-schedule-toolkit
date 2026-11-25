import json
from datetime import date
from schedule_2027 import rows
T={'龍':'味全龍','象':'中信兄弟','獅':'統一7-ELEVEn獅','悍將':'富邦悍將','桃猿':'樂天桃猿','雄鷹':'台鋼雄鷹'}
notes={(4,22):'上半季優先補賽日',(4,29):'上半季優先補賽日',(6,4):'上半季優先補賽日',
(6,22):'補賽預備日',(6,23):'補賽預備日',(6,24):'補賽預備日',(6,25):'補賽預備日',(6,26):'（假日）補賽預備日',(6,27):'（假日）補賽預備日',
(6,29):'上半季補賽週 補賽預備日',(6,30):'上半季加賽保留日',(7,2):'下半季開賽',(7,17):'明星賽',(7,18):'明星賽',
(9,21):'下半季優先補賽日',(9,22):'下半季優先補賽日',(9,29):'補賽預備日',(9,30):'補賽預備日',(10,1):'補賽預備日',
(10,2):'（假日）補賽預備日',(10,3):'（假日）補賽預備日',(10,4):'下半季補賽週 補賽預備日',(10,5):'下半季補賽週 補賽預備日',
(10,6):'下半季加賽保留日'}
for d in (9,10,11,12): notes[(10,d)]='季後賽預定'
for d in range(16,25): notes[(10,d)]='總冠軍賽預定'
months={m:[] for m in range(3,11)}
gd={}
for d,a,h in rows: gd.setdefault(d,[]).append((a,h))
alld=sorted(set(list(gd)+[date(2027,m,d) for (m,d) in notes]))
for d in alld:
    ds=d.strftime('%Y/%m/%d'); half='上半季' if d<date(2027,7,1) else '下半季'
    n=notes.get((d.month,d.day),'')
    if d in gd:
        for a,h in gd[d]: months[d.month].append([ds,None,T[a],T[h],half,n])
    else: months[d.month].append([ds,None,'','',half if d.month<10 or n.startswith(('補','（','下半')) else '',n])
for m,v in months.items():
    json.dump(v,open(f'm{m}.json','w'),ensure_ascii=False,separators=(',',':'))
    print(m,len(v),sum(1 for r in v if r[2]))
