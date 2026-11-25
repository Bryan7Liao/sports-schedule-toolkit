import json, calendar
from datetime import date
from schedule_2027 import rows
S={'龍':'味全','象':'兄弟','獅':'統一','悍將':'富邦','桃猿':'樂天','雄鷹':'台鋼'}
# soft palette: full name, short, bg, text
P=[('味全龍','味全','#F6C4C1','#7A1F1C'),('中信兄弟','兄弟','#FFF0B3','#5E4B00'),('統一7-ELEVEn獅','統一','#FDD5AE','#7A3E00'),
   ('富邦悍將','富邦','#C3D7F2','#173E73'),('樂天桃猿','樂天','#D9A3AC','#4A0A14'),('台鋼雄鷹','台鋼','#B7D6C4','#1E4D33')]
def rgb(h): h=h.lstrip('#'); return {k:round(int(h[i:i+2],16)/255,3) for k,i in (('red',0),('green',2),('blue',4))}
games={}
for d,a,h in rows: games.setdefault(d,[]).append(f'{S[a]} vs {S[h]}')
dnote={(6,4):'優先補賽日',(7,2):'下半季開賽',(9,15):'',}
fnote={(4,22):'優先補賽日',(4,29):'優先補賽日',(6,30):'加賽保留日',(7,17):'明星賽',(7,18):'明星賽',(9,21):'優先補賽日',(9,22):'優先補賽日',(10,6):'加賽保留日'}
for d in (22,23,24,25,26,27,29): fnote[(6,d)]='補賽預備日'
for m,d in ((9,29),(9,30),(10,1),(10,2),(10,3),(10,4),(10,5)): fnote[(m,d)]='補賽預備日'
for d in (9,10,11,12): fnote[(10,d)]='季後賽預定'
for d in range(16,25): fnote[(10,d)]='總冠軍賽預定'
NR=120; grid=[[None]*16 for _ in range(NR)]
grid[0][1]='2027 中華職棒例行賽賽程（客隊 vs 主隊，底色為主場球隊）'
fmt={'title':[],'wk':[],'daterow':[],'blocks':[]}
r0=2
for pair in ((3,4),(5,6),(7,8),(9,10)):
    heights=[]
    for side,m in enumerate(pair):
        c0=1+side*8; r=r0
        grid[r][c0]=f'{m}月'; fmt['title'].append((r,c0))
        r+=1
        for i,w in enumerate('一二三四五六日'): grid[r][c0+i]=w
        fmt['wk'].append((r,c0)); r+=1
        for week in calendar.Calendar(0).monthdatescalendar(2027,m):
            fmt['daterow'].append((r,c0))
            for i,d in enumerate(week):
                if d.month!=m: continue
                t=str(d.day); n=dnote.get((m,d.day))
                if n: t+=f' {n}'
                grid[r][c0+i]=t
                gs=games.get(d,[])
                for k,g in enumerate(gs): grid[r+1+k][c0+i]=g
                f=fnote.get((m,d.day))
                if f and not gs: grid[r+1][c0+i]='※'+f
            r+=4
        fmt['blocks'].append((r0,r,c0)); heights.append(r)
    r0=max(heights)+1
last=r0
grid=grid[:last]
# check game count
cnt=sum(1 for row in grid for v in row if isinstance(v,str) and ' vs ' in v); print('games',cnt,'rows',last)
json.dump(grid,open('calgrid.json','w'),ensure_ascii=False)
SID=11
R=[{'addSheet':{'properties':{'sheetId':SID,'title':'2027日曆','index':0,'gridProperties':{'rowCount':last+5,'columnCount':16,'hideGridlines':True}}}}]
def gr(r1,r2,c1,c2): return {'sheetId':SID,'startRowIndex':r1,'endRowIndex':r2,'startColumnIndex':c1,'endColumnIndex':c2}
R.append({'repeatCell':{'range':gr(0,last+5,0,16),'cell':{'userEnteredFormat':{'textFormat':{'fontFamily':'Arial','fontSize':10},'horizontalAlignment':'CENTER','verticalAlignment':'MIDDLE'}},'fields':'userEnteredFormat.textFormat,userEnteredFormat.horizontalAlignment,userEnteredFormat.verticalAlignment'}})
R.append({'repeatCell':{'range':gr(0,1,1,16),'cell':{'userEnteredFormat':{'textFormat':{'fontFamily':'Arial','fontSize':14,'bold':True},'horizontalAlignment':'LEFT'}},'fields':'userEnteredFormat.textFormat,userEnteredFormat.horizontalAlignment'}})
for c,w in [(0,16),(8,24)]+[(c,104) for c in list(range(1,8))+list(range(9,16))]:
    R.append({'updateDimensionProperties':{'range':{'sheetId':SID,'dimension':'COLUMNS','startIndex':c,'endIndex':c+1},'properties':{'pixelSize':w},'fields':'pixelSize'}})
for r,c in fmt['title']:
    R.append({'mergeCells':{'range':gr(r,r+1,c,c+7),'mergeType':'MERGE_ALL'}})
    R.append({'repeatCell':{'range':gr(r,r+1,c,c+7),'cell':{'userEnteredFormat':{'backgroundColorStyle':{'rgbColor':rgb('#5B6470')},'textFormat':{'bold':True,'fontSize':12,'fontFamily':'Arial','foregroundColorStyle':{'rgbColor':rgb('#FFFFFF')}}}},'fields':'userEnteredFormat.backgroundColorStyle,userEnteredFormat.textFormat'}})
for r,c in fmt['wk']:
    R.append({'repeatCell':{'range':gr(r,r+1,c,c+7),'cell':{'userEnteredFormat':{'backgroundColorStyle':{'rgbColor':rgb('#DDE1E6')},'textFormat':{'bold':True,'fontFamily':'Arial','fontSize':10}}},'fields':'userEnteredFormat.backgroundColorStyle,userEnteredFormat.textFormat'}})
for r,c in fmt['daterow']:
    R.append({'repeatCell':{'range':gr(r,r+1,c,c+7),'cell':{'userEnteredFormat':{'backgroundColorStyle':{'rgbColor':rgb('#F4F5F7')},'textFormat':{'bold':True,'fontFamily':'Arial','fontSize':9,'foregroundColorStyle':{'rgbColor':rgb('#555555')}},'horizontalAlignment':'LEFT'}},'fields':'userEnteredFormat.backgroundColorStyle,userEnteredFormat.textFormat,userEnteredFormat.horizontalAlignment'}})
bc={'style':'SOLID','colorStyle':{'rgbColor':rgb('#C9CED6')}}
for r1,r2,c in fmt['blocks']:
    R.append({'updateBorders':{'range':gr(r1+1,r2,c,c+7),'top':bc,'bottom':bc,'left':bc,'right':bc,'innerVertical':bc}})
    for rr,cc in fmt['daterow']:
        if cc==c and r1<rr<r2: R.append({'updateBorders':{'range':gr(rr,rr+1,c,c+7),'top':bc}})
area=[gr(2,last,1,16)]
for full,short,bg,fg in P:
    R.append({'addConditionalFormatRule':{'rule':{'ranges':area,'booleanRule':{'condition':{'type':'CUSTOM_FORMULA','values':[{'userEnteredValue':f'=REGEXMATCH(TO_TEXT(B3),"vs {short}$")'}]},'format':{'backgroundColor':rgb(bg),'textFormat':{'foregroundColor':rgb(fg)}}}}}})
R.append({'addConditionalFormatRule':{'rule':{'ranges':area,'booleanRule':{'condition':{'type':'CUSTOM_FORMULA','values':[{'userEnteredValue':'=LEFT(TO_TEXT(B3),1)="※"'}]},'format':{'textFormat':{'foregroundColor':rgb('#8A8A8A'),'italic':True}}}}}})
# palette update on month sheets
for s in [0]+list(range(4,11)):
    for i,(full,short,bg,fg) in enumerate(P):
        R.append({'updateConditionalFormatRule':{'sheetId':s,'index':i,'rule':{'ranges':[{'sheetId':s,'startRowIndex':1,'startColumnIndex':0,'endColumnIndex':6}],'booleanRule':{'condition':{'type':'CUSTOM_FORMULA','values':[{'userEnteredValue':f'=$D2="{full}"'}]},'format':{'backgroundColor':rgb(bg),'textFormat':{'foregroundColor':rgb(fg)}}}}}})
    R.append({'updateCells':{'start':{'sheetId':s,'rowIndex':1,'columnIndex':7},'rows':[{'values':[{'userEnteredFormat':{'backgroundColorStyle':{'rgbColor':rgb(bg)},'textFormat':{'bold':True,'foregroundColorStyle':{'rgbColor':rgb(fg)}},'horizontalAlignment':'CENTER'}}]} for _,_,bg,fg in P],'fields':'userEnteredFormat.backgroundColorStyle,userEnteredFormat.textFormat.bold,userEnteredFormat.textFormat.foregroundColorStyle,userEnteredFormat.horizontalAlignment'}})
    R.append({'repeatCell':{'range':{'sheetId':s,'startRowIndex':0,'endRowIndex':1,'startColumnIndex':0,'endColumnIndex':8},'cell':{'userEnteredFormat':{'backgroundColorStyle':{'rgbColor':rgb('#5B6470')}}},'fields':'userEnteredFormat.backgroundColorStyle'}})
# legend on calendar: row 1 (index1) cols B..
leg=[{'values':[{'userEnteredValue':{'stringValue':'主場底色：'},'userEnteredFormat':{'textFormat':{'bold':True},'horizontalAlignment':'RIGHT'}}]+[{'userEnteredValue':{'stringValue':full},'userEnteredFormat':{'backgroundColorStyle':{'rgbColor':rgb(bg)},'textFormat':{'bold':True,'foregroundColorStyle':{'rgbColor':rgb(fg)}},'horizontalAlignment':'CENTER'}} for full,_,bg,fg in P]}]
R.append({'updateCells':{'start':{'sheetId':SID,'rowIndex':1,'columnIndex':1},'rows':leg,'fields':'userEnteredValue,userEnteredFormat.backgroundColorStyle,userEnteredFormat.textFormat.bold,userEnteredFormat.textFormat.foregroundColorStyle,userEnteredFormat.horizontalAlignment'}})
R.append({'updateSheetProperties':{'properties':{'sheetId':SID,'gridProperties':{'frozenRowCount':2}},'fields':'gridProperties.frozenRowCount'}})
s=json.dumps(R,ensure_ascii=False,separators=(',',':')); open('calreq.json','w').write(s); print(len(R),len(s))
