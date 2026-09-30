import re
from PIL import ImageFont
F = {'display_bold':'/usr/share/fonts/X11/Type1/c0649bt_.pfb','display_reg':'/usr/share/fonts/X11/Type1/c0648bt_.pfb',
     'display_ital':'/usr/share/fonts/X11/Type1/c0633bt_.pfb','body':'/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
     'body_bold':'/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'}
c={}
def f(k,s):
    if (k,s) not in c: c[(k,s)]=ImageFont.truetype(F[k],int(s))
    return c[(k,s)]
svg=open('accueil.svg').read()
pat=re.compile(r"<text x=\"([-\d.]+)\" y=\"([-\d.]+)\" font-family=\"'(\w+)'\" font-size=\"(\d+)\"([^>]*)>(.*?)</text>",re.S)
bad=[];n=0
for m in pat.finditer(svg):
    n+=1
    x,y,k,s,attrs,t=float(m.group(1)),float(m.group(2)),m.group(3),m.group(4),m.group(5),m.group(6)
    t=t.replace('&amp;','&')
    ft=f(k,s); w=ft.getlength(t)
    mm=re.search(r'letter-spacing="([\d.]+)"',attrs)
    if mm: w+=float(mm.group(1))*max(0,len(t)-1)
    anchor='middle' if 'middle' in attrs else ('end' if '"end"' in attrs else 'start')
    x0=x if anchor=='start' else (x-w/2 if anchor=='middle' else x-w)
    asc,desc=ft.getmetrics()
    top,bot=y-asc,y+desc
    p=[]
    if x0<20 or x0+w>1580: p.append('X')
    if top<4 or bot>2556: p.append('Y')
    if p: bad.append((p,k,int(s),round(x0),round(x0+w),round(top),round(bot),t[:70]))
print('texts audits:',n)
for b in bad: print(b)
if not bad: print('>>> AUCUN DEBORDEMENT HORS-MARGE (x<20 ou x>1580 ou y hors 0-2560)')
