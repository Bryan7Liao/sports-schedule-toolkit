import json, calendar
import os
os.makedirs('out/project', exist_ok=True)
from datetime import date
from schedule_2027 import rows
S={'龍':'味全','象':'兄弟','獅':'統一','悍將':'富邦','桃猿':'樂天','雄鷹':'台鋼'}
FULL={'味全':'味全龍','兄弟':'中信兄弟','統一':'統一7-ELEVEn獅','富邦':'富邦悍將','樂天':'樂天桃猿','台鋼':'台鋼雄鷹'}
# primary (solid) bg, text on primary ; pastel bg, pastel text
PRI={'味全':('#D7261E','#FFFFFF'),'兄弟':('#F5C400','#2B2400'),'統一':('#F08A24','#3A1C00'),'富邦':('#1E4FA0','#FFFFFF'),'樂天':('#8A1022','#FFFFFF'),'台鋼':('#0E5A3A','#FFFFFF')}
PAS={'味全':('#F6C4C1','#7A1F1C'),'兄弟':('#FFF0B3','#5E4B00'),'統一':('#FDD5AE','#7A3E00'),'富邦':('#C3D7F2','#173E73'),'樂天':('#D9A3AC','#4A0A14'),'台鋼':('#B7D6C4','#1E4D33')}
FILES={'味全':'Main','兄弟':'Brothers','統一':'Lions','富邦':'Guardians','樂天':'Monkeys','台鋼':'Hawks'}
note={(4,22):'補賽日',(4,29):'補賽日',(6,4):'補賽日',(6,30):'加賽保留',(7,2):'下半季開打',(7,17):'明星賽',(7,18):'明星賽',(9,21):'補賽日',(9,22):'補賽日',(10,6):'加賽保留'}
for d in (22,23,24,25,26,27,29): note[(6,d)]='補賽預備'
for m,d in ((9,29),(9,30),(10,1),(10,2),(10,3),(10,4),(10,5)): note[(m,d)]='補賽預備'
for d in (9,10,11,12): note[(10,d)]='季後賽'
for d in range(16,25): note[(10,d)]='總冠軍賽'
EN=['','','','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT']
def months(team):
    g={}
    for d,a,h in rows:
        a,h=S[a],S[h]
        if h==team: g[d]=('home',a)
        elif a==team: g[d]=('away',h)
    pb,pf=PRI[team]
    out=[]
    for m in range(3,11):
        cells=[]; cnt=0
        for week in calendar.Calendar(0).monthdatescalendar(2027,m):
            for d in week:
                if d.month!=m: cells.append({'d':'','l':'','n':'','s':'background:transparent','ds':'color:transparent'}); continue
                n=note.get((m,d.day),'')
                if d in g:
                    k,o=g[d]; cnt+=1
                    if k=='home': bg,fg,l=pb,pf,f'vs {o}'
                    else: bg,fg=PAS[o]; l=f'@ {o}'
                    cells.append({'d':str(d.day),'l':l,'n':'','s':f'background:{bg};color:{fg}','ds':f'color:{fg};opacity:.75'})
                else:
                    cells.append({'d':str(d.day),'l':'','n':n,'s':'background:#F3F2EE;color:#8A877F','ds':'color:#9C998F'})
        out.append({'m':f'{m}月','en':EN[m],'cnt':f'{cnt} 場','cells':cells})
    first=min(g); k,o=g[first]
    opener=f'{first.month}/{first.day} {"主場 vs" if k=="home" else "客場 @"} {o}'
    return out,opener
TPL=open('templates/poster_template.dc.html').read()
for t in FULL:
    ms,opener=months(t)
    pb,pf=PRI[t]
    legend=[{'n':f'@ {s}','s':f'background:{PAS[s][0]};color:{PAS[s][1]}'} for s in FULL if s!=t]
    html=(TPL.replace('__TEAM__',FULL[t]).replace('__SHORT__',t).replace('__PB__',pb).replace('__PF__',pf)
          .replace('__OPENER__',opener).replace('__DATA__',json.dumps(ms,ensure_ascii=False,separators=(',',':')).replace("'","&#39;"))
          .replace('__LEGEND__',json.dumps(legend,ensure_ascii=False,separators=(',',':'))))
    open(f'out/project/{FILES[t]}.dc.html','w').write(html)
    print(t,FILES[t],len(html),opener)
