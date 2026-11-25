import json, calendar
from datetime import date
from schedule_2027 import rows
S={'龍':'味全','象':'兄弟','獅':'統一','悍將':'富邦','桃猿':'樂天','雄鷹':'台鋼'}
FULL={'味全':'味全龍','兄弟':'中信兄弟','統一':'統一7-ELEVEn獅','富邦':'富邦悍將','樂天':'樂天桃猿','台鋼':'台鋼雄鷹'}
P=[('味全','#F6C4C1','#7A1F1C'),('兄弟','#FFF0B3','#5E4B00'),('統一','#FDD5AE','#7A3E00'),('富邦','#C3D7F2','#173E73'),('樂天','#D9A3AC','#4A0A14'),('台鋼','#B7D6C4','#1E4D33')]
def rgb(h): h=h.lstrip('#'); return {k:round(int(h[i:i+2],16)/255,3) for k,i in (('red',0),('green',2),('blue',4))}
dnote={(6,4):'優先補賽日',(7,2):'下半季開賽'}
fnote={(4,22):'優先補賽日',(4,29):'優先補賽日',(6,30):'加賽保留日',(7,17):'明星賽',(7,18):'明星賽',(9,21):'優先補賽日',(9,22):'優先補賽日',(10,6):'加賽保留日'}
for d in (22,23,24,25,26,27,29): fnote[(6,d)]='補賽預備日'
for m,d in ((9,29),(9,30),(10,1),(10,2),(10,3),(10,4),(10,5)): fnote[(m,d)]='補賽預備日'
for d in (9,10,11,12): fnote[(10,d)]='季後賽預定'
for d in range(16,25): fnote[(10,d)]='總冠軍賽預定'
def build(team):
    g={}
    for d,a,h in rows:
        a,h=S[a],S[h]
        if h==team: g[d]=f'主 vs {a}'
        elif a==team: g[d]=f'客 @ {h}'
    grid=[[None]*16 for _ in range(80)]
    grid[0][1]=f'{team}｜{FULL[team]} 2027 例行賽賽程（底色為主場球隊）'
    grid[1][1]='主場底色：'
    for i,(s,_,_) in enumerate(P): grid[1][2+i]=s
    grid[1][9]='主場'; grid[1][10]='=COUNTIF(B4:P80,"主 *")'
    grid[1][11]='客場'; grid[1][12]='=COUNTIF(B4:P80,"客 *")'
    grid[1][13]='合計'; grid[1][14]='=K2+M2'
    lay={'title':[],'wk':[],'blocks':[]}
    r0=3
    for pair in ((3,4),(5,6),(7,8),(9,10)):
        ends=[]
        for side,m in enumerate(pair):
            c0=1+side*8; r=r0
            grid[r][c0]=f'{m}月'; lay['title'].append((r,c0)); r+=1
            for i,w in enumerate('一二三四五六日'): grid[r][c0+i]=w
            lay['wk'].append((r,c0)); r+=1
            for week in calendar.Calendar(0).monthdatescalendar(2027,m):
                for i,d in enumerate(week):
                    if d.month!=m: continue
                    t=str(d.day); n=dnote.get((m,d.day))
                    if n: t+=f' {n}'
                    grid[r][c0+i]=t
                    if d in g: grid[r+1][c0+i]=g[d]
                    elif (m,d.day) in fnote: grid[r+1][c0+i]='※'+fnote[(m,d.day)]
                r+=2
            lay['blocks'].append((r0,r,c0)); ends.append(r)
        r0=max(ends)+1
    return grid[:r0],lay,sum(1 for v in g.values())
grid,lay,n=build('味全'); print(len(grid),n)
for t in FULL:
    gg,_,n=build(t)
    h=sum(1 for row in gg for v in row if isinstance(v,str) and v.startswith('主 vs')); a=sum(1 for row in gg for v in row if isinstance(v,str) and v.startswith('客 @'))
    print(t,n,h,a)
    json.dump([[v for v in row] for row in gg],open(f't_{t}.json','w'),ensure_ascii=False)
last=len(grid)
SID=21
def gr(r1,r2,c1,c2): return {'sheetId':SID,'startRowIndex':r1,'endRowIndex':r2,'startColumnIndex':c1,'endColumnIndex':c2}
bc={'style':'SOLID','colorStyle':{'rgbColor':rgb('#C9CED6')}}
R=[{'addSheet':{'properties':{'sheetId':SID,'title':'味全龍','index':1,'gridProperties':{'rowCount':last+3,'columnCount':16,'hideGridlines':True,'frozenRowCount':2}}}},
 {'updateDimensionProperties':{'range':{'sheetId':SID,'dimension':'COLUMNS','startIndex':0,'endIndex':16},'properties':{'pixelSize':92},'fields':'pixelSize'}},
 {'updateDimensionProperties':{'range':{'sheetId':SID,'dimension':'COLUMNS','startIndex':0,'endIndex':1},'properties':{'pixelSize':16},'fields':'pixelSize'}},
 {'updateDimensionProperties':{'range':{'sheetId':SID,'dimension':'COLUMNS','startIndex':8,'endIndex':9},'properties':{'pixelSize':24},'fields':'pixelSize'}},
 {'repeatCell':{'range':gr(0,last+3,0,16),'cell':{'userEnteredFormat':{'textFormat':{'fontFamily':'Arial','fontSize':10},'horizontalAlignment':'CENTER','verticalAlignment':'MIDDLE'}},'fields':'userEnteredFormat.textFormat,userEnteredFormat.horizontalAlignment,userEnteredFormat.verticalAlignment'}},
 {'repeatCell':{'range':gr(0,1,1,16),'cell':{'userEnteredFormat':{'textFormat':{'fontFamily':'Arial','fontSize':14,'bold':True},'horizontalAlignment':'LEFT'}},'fields':'userEnteredFormat.textFormat,userEnteredFormat.horizontalAlignment'}},
 {'repeatCell':{'range':gr(1,2,1,2),'cell':{'userEnteredFormat':{'textFormat':{'bold':True},'horizontalAlignment':'RIGHT'}},'fields':'userEnteredFormat.textFormat.bold,userEnteredFormat.horizontalAlignment'}},
 {'repeatCell':{'range':gr(1,2,9,15),'cell':{'userEnteredFormat':{'textFormat':{'bold':True},'backgroundColorStyle':{'rgbColor':rgb('#EEF0F3')}}},'fields':'userEnteredFormat.textFormat.bold,userEnteredFormat.backgroundColorStyle'}},
 {'updateCells':{'start':{'sheetId':SID,'rowIndex':1,'columnIndex':2},'rows':[{'values':[{'userEnteredFormat':{'backgroundColorStyle':{'rgbColor':rgb(bg)},'textFormat':{'bold':True,'foregroundColorStyle':{'rgbColor':rgb(fg)}},'horizontalAlignment':'CENTER'}} for _,bg,fg in P]}],'fields':'userEnteredFormat.backgroundColorStyle,userEnteredFormat.textFormat.bold,userEnteredFormat.textFormat.foregroundColorStyle,userEnteredFormat.horizontalAlignment'}}]
for r,c in lay['title']:
    R.append({'mergeCells':{'range':gr(r,r+1,c,c+7),'mergeType':'MERGE_ALL'}})
    R.append({'repeatCell':{'range':gr(r,r+1,c,c+7),'cell':{'userEnteredFormat':{'backgroundColorStyle':{'rgbColor':rgb('#5B6470')},'textFormat':{'bold':True,'fontSize':12,'fontFamily':'Arial','foregroundColorStyle':{'rgbColor':rgb('#FFFFFF')}}}},'fields':'userEnteredFormat.backgroundColorStyle,userEnteredFormat.textFormat'}})
for r,c in lay['wk']:
    R.append({'repeatCell':{'range':gr(r,r+1,c,c+7),'cell':{'userEnteredFormat':{'backgroundColorStyle':{'rgbColor':rgb('#DDE1E6')},'textFormat':{'bold':True,'fontFamily':'Arial','fontSize':10}}},'fields':'userEnteredFormat.backgroundColorStyle,userEnteredFormat.textFormat'}})
for r1,r2,c in lay['blocks']:
    R.append({'updateBorders':{'range':gr(r1+1,r2,c,c+7),'top':bc,'bottom':bc,'left':bc,'right':bc,'innerVertical':bc}})
area=[gr(3,last,1,16)]
def cf(formula,bg=None,fg=None,bold=None,italic=None):
    f={}
    if bg: f['backgroundColor']=rgb(bg)
    tf={}
    if fg: tf['foregroundColor']=rgb(fg)
    if bold: tf['bold']=True
    if italic: tf['italic']=True
    if tf: f['textFormat']=tf
    return {'addConditionalFormatRule':{'rule':{'ranges':area,'booleanRule':{'condition':{'type':'CUSTOM_FORMULA','values':[{'userEnteredValue':formula}]},'format':f}}}}
R.append(cf('=REGEXMATCH(TO_TEXT(B4),"^[0-9]+($| )")','#EEF0F3','#555555',bold=True))
R.append(cf('=LEFT(TO_TEXT(B4),1)="※"',None,'#8A8A8A',italic=True))
for s,bg,fg in P:
    R.append(cf(f'=OR(REGEXMATCH(TO_TEXT(B4),"@ {s}$"),AND(LEFT(TO_TEXT(B4),2)="主 ",LEFT($B$1,2)="{s}"))',bg,fg))
for i,t in enumerate(['兄弟','統一','富邦','樂天','台鋼']):
    R.append({'duplicateSheet':{'sourceSheetId':SID,'insertSheetIndex':2+i,'newSheetId':22+i,'newSheetName':FULL[t]}})
s=json.dumps(R,ensure_ascii=False,separators=(',',':')); open('teamreq.json','w').write(s); print(len(R),len(s))
