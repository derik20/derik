# -*- coding: utf-8 -*-
"""Génère l'image de la proposition visuelle (page d'accueil) -> accueil.png"""
from PIL import ImageFont
import cairosvg, os

F = {
 'display_bold': '/usr/share/fonts/X11/Type1/c0649bt_.pfb',   # Bitstream Charter Bold
 'display_reg' : '/usr/share/fonts/X11/Type1/c0648bt_.pfb',   # Charter Regular
 'display_ital': '/usr/share/fonts/X11/Type1/c0633bt_.pfb',   # Charter Bold Italic
 'body'        : '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
 'body_bold'   : '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
}
_cache = {}
def _f(key,size):
    k=(key,size)
    if k not in _cache: _cache[k]=ImageFont.truetype(F[key],size)
    return _cache[k]
def W(key,size,txt):
    b=_f(key,size).getbbox(txt)
    return b[2]-b[0]

S=[]           # svg fragments
WARN=[]        # overflow warnings

def esc(t):
    return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def text(x,y,s,key='body',size=22,fill='#2A2E2B',anchor='start',ls=None,op=None):
    w=W(key,size,s)
    x0 = x if anchor=='start' else (x-w/2 if anchor=='middle' else x-w)
    limit = 1576
    if x0 < 24 or x0+w > limit:
        WARN.append(f"OVERFLOW [{key} {size}] x0={x0:.0f} x1={x0+w:.0f} :: {s[:60]}")
    a = f' text-anchor="{anchor}"' if anchor!='start' else ''
    l = f' letter-spacing="{ls}"' if ls else ''
    o = f' opacity="{op}"' if op is not None else ''
    S.append(f'<text x="{x:.1f}" y="{y}" font-family="\'{key}\'" font-size="{size}"'
             f' fill="{fill}"{a}{l}{o}>{esc(s)}</text>')
    return w

def rect(x,y,w,h,fill,rx=0,op=None,stroke=None,sw=1,dash=None):
    o=f' opacity="{op}"' if op is not None else ''
    st=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    d=f' stroke-dasharray="{dash}"' if dash else ''
    S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{o}{st}{d}/>')

def line(x1,y1,x2,y2,stroke='#D3CCBC',sw=1,dash=None,op=None,cap='butt'):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    o=f' opacity="{op}"' if op is not None else ''
    S.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
             f'stroke-width="{sw}" stroke-linecap="{cap}"{d}{o}/>')

def circle(cx,cy,r,fill,op=None,stroke=None,sw=1):
    o=f' opacity="{op}"' if op is not None else ''
    st=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    S.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{o}{st}/>')

def path(d,fill='none',stroke=None,sw=1,op=None,cap='round',join='round',dash=None):
    st='' if stroke is None else f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="{join}"'
    dd=f' stroke-dasharray="{dash}"' if dash else ''
    o='' if op is None else f' opacity="{op}"'
    S.append(f'<path d="{d}" fill="{fill}"{st}{dd}{o}/>')

def ellipse(cx,cy,rx,ry,fill,op=None,transform=None):
    o=f' opacity="{op}"' if op is not None else ''
    t=f' transform="{transform}"' if transform else ''
    S.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"{o}{t}/>')

def g_open(attrs): S.append(f'<g {attrs}>')
def g_close(): S.append('</g>')

# ---------------------------------------------------------------- palette
INK   = '#22261F'   # texte principal
INK2  = '#4E534C'   # texte secondaire
PAPER = '#FBF8F1'   # fond carte
CANV  = '#F3EFE4'   # fond page
LINE  = '#DCD5C6'   # filets
GREEN = '#155C46'   # vert profond (sections sombres)
GREEN2= '#0E4535'
ACC   = '#C6431A'   # couleur d'action (unique, blanc 4.8:1)
CREAM = '#F5EFE1'
SKIN  = '#E7BA98'
SKIND = '#D3A182'
HAIR  = '#332A24'
SHELL = '#EFE6D5'   # canape
SHELL2= '#E1D6BF'
SWEAT = '#7E9AA6'   # pull
SWEAT2= '#6B8794'
JEANS = '#3E4E63'
TILES = ['#E7DECB','#DCE4DD','#EADFC8','#D9DDD3']

W_PAGE, H_PAGE = 1600, 2560

# ================================================================ 1. NAV
rect(0,0,W_PAGE,92,CREAM)
line(0,92,W_PAGE,92,LINE,2)
# logo provisoire : un fil qui se renoue + marque "provisoire"
g_open('transform="translate(64,30)"')
path('M0,16 C8,-6 26,-6 30,10 C33,22 20,26 16,17 C12,8 24,4 34,8', stroke=INK, sw=3.4, fill='none')
circle(38,9,4.6,ACC)
g_close()
text(116,57,'Reprendre le fil','display_bold',26,INK)
wlogo = W('display_bold',26,'Reprendre le fil')
text(116+wlogo+14,56,'· symbole provisoire','body',15,'#4E534C')
navitems = ["Comment ça marche", "Pour qui", "Confidentialité"]
xnav = 1536
for it in reversed(navitems):
    w = W('body',20,it)
    text(xnav-w, 56, it, 'body', 20, INK)
    xnav -= (w+46)
rect(xnav-16, 26, W('body',20,'Faire le point')+32+22, 42, ACC, rx=21)
text(xnav+16, 53, 'Faire le point', 'body_bold', 19, '#FFFFFF')

# ================================================================ 2. HERO
rect(0,92,W_PAGE,1036,CANV)
rect(44,132,1512,968,PAPER,rx=6)
rect(44,132,1512,968,'none',rx=6,stroke='#E4DDCD',sw=2)
# colonne editorial
CL, CW = 104, 700          # left, width
KICK='POUR LES SOIRÉES OÙ ON A BEAUCOUP DÉFILÉ AVANT DE COMMENCER'
text(CL,214,KICK,'body_bold',15,GREEN,ls=1.4)
if W('body_bold',15,KICK)+1.4*(len(KICK)-1) > CW:
    WARN.append('kicker trop large')
text(CL,300,'Vous avez scrollé.','display_bold',72,INK)
text(CL,382,'Maintenant, on reprend','display_bold',72,INK)
text(CL+0,464,'par quoi ?','display_bold',72,INK)
# souligné "main" de la couleur d'action, léger et volontairement imparfait
path('M'+str(CL)+',486 C150,478 200,494 250,485 C286,479 312,489 332,485', stroke=ACC, sw=5, fill='none')
text(CL,538,'C’est la question que l’on garde pour vous.','display_reg',27,INK2)
text(CL,618,'Quand un fil nous emporte plus loin que prévu, il reste souvent',
     'body',22,'#3D423C')
text(CL,650,'une soirée en suspens et dix choses à reprendre. On vous aide à',
     'body',22,'#3D423C')
text(CL,682,'faire le point avec quelques questions simples, à choisir une',
     'body',22,'#3D423C')
text(CL,714,'seule priorité, puis à retrouver une première action claire —',
     'body',22,'#3D423C')
text(CL,746,'à votre rythme.', 'body',22,'#3D423C')
# bouton principal
BW = W('body_bold',22,'Faire le point')+ 2*34
BH = 66
rect(CL,790,BW,BH,ACC,rx=8)
text(CL+34, 790+42, 'Faire le point', 'body_bold', 22, '#FFFFFF')
text(CL+BW+26, 790+42, '— aucune donnée publiée sur vos comptes', 'body', 19, '#4E534C')
# les 3 acquis
gy = 906
labels = ['Une lecture de votre situation','Une seule priorité retenue','Une prochaine action concrète']
sub =    ['ce qui vous tire aujourd’hui','ce qui attend depuis trop longtemps','le premier geste, à votre portée']
for i,(lb,sb) in enumerate(zip(labels,sub)):
    yy = gy + i*34
    circle(CL+9, yy-7, 9, ACC)
    path(f'M{CL+3},{yy-7} l4,5 l9,-10', stroke='#FFFFFF', sw=2.6, fill='none')
    text(CL+30, yy, lb, 'body_bold', 20, INK)
    text(CL+30+W('body_bold',20,lb)+14, yy, '— '+sb, 'body', 18, '#4E534C')
line(CL, 962, CL+CW, 962, LINE, 1)
text(CL, 996,'Pas de diagnostic médical. Pas de compte à remonter.', 'body', 18, '#4E534C')
text(CL, 1024,'Chaque étape vous est montrée avant que vous alliez plus loin.', 'body', 18, '#4E534C')

# ================================================================ 3. SCENE ILLUSTREE (droite du hero)
SX, SY = 852, 168          # origine de la scene
SW_, SH_ = 676, 900        # taille
g_open(f'transform="translate({SX},{SY})"')
rect(0,0,SW_,SH_, '#F1EADA', rx=4)
# mur + sol
rect(0,0,SW_,560,'#F1EADA')
rect(0,560,SW_,340,'#E7DCC6')
line(0,560,SW_,560,'#DBCFB6',2)
# fenetre : lumiere du soir
rect(392,64,224,268,'#EFE3CB',rx=4,stroke='#DACDB2',sw=3)
rect(400,72,208,252,'#F6E7C8')
path('M400,72 L608,72 L608,324 Z', fill='#FBF2DA')
line(504,72,504,324,'#DACDB2',3); line(400,198,608,198,'#DACDB2',3)
# plante pres de la fenetre (simple, non decoratif-productivite)
path('M366,470 C356,430 358,404 372,384', stroke='#5F7A5A', sw=4, fill='none')
path('M366,470 C378,438 392,424 404,418', stroke='#5F7A5A', sw=4, fill='none')
ellipse(366,382,13,20,'#6E8C63',transform='rotate(-18 366 382)')
ellipse(404,416,12,17,'#7E9C70',transform='rotate(28 404 416)')
rect(348,470,44,42,'#C98C63',rx=4)
# canape
rect(60,300,470,90,'#E3D8C1',rx=26)             # dossier
rect(30,368,530,180,'#EFE6D5',rx=22)            # assise
rect(30,368,530,26,'#E6DBC5',rx=13)             # coussin haut
rect(30,470,530,78,'#E1D6BF',rx=18)             # coussin bas
rect(20,330,64,230,'#EDE3D1',rx=24)             # accoudoir gauche
rect(506,330,64,230,'#EDE3D1',rx=24)            # accoudoir droit
rect(60,556,16,44,'#C9B995',rx=4); rect(470,556,16,44,'#C9B995',rx=4)
# OMBRE au sol
ellipse(300,614,240,26,'#D8CBAD',op=.75)
# ---- PERSONNE (assis, de trois quarts vers la gauche)
# jambes en tailleur sur le canape
path('M180,520 C150,470 168,432 226,428 C286,424 320,452 316,500 C312,540 250,556 208,548 Z', fill=JEANS)
path('M214,430 C262,410 316,424 336,462 C352,494 332,528 300,530', fill='#33415A')
# pieds / chaussettes
ellipse(196,540,26,17,'#C9705A'); ellipse(322,536,24,16,'#C9705A')
# torse (pull)
path('M212,432 C196,372 206,306 246,272 C286,240 344,252 366,300 C384,340 372,404 350,442 C316,462 246,462 212,432 Z', fill=SWEAT)
path('M212,432 C196,372 206,306 246,272 C268,258 296,254 318,262 C288,278 262,320 254,372 C248,410 252,436 260,452 C236,452 220,446 212,432 Z', fill=SWEAT2)
# bras gauche qui descend tenir le telephone
path('M232,300 C206,336 196,392 206,438 C212,462 232,470 246,462 C258,454 256,436 248,424 C238,410 238,376 250,346 Z', fill=SWEAT)
# main
ellipse(246,470,21,14,SKIN,transform='rotate(-8 246 470)')
# TELEPHONE (indice secondaire, ecran eteint)
g_open('transform="translate(430,506) rotate(-6)"')
ellipse(22,44,44,17,'#DCCFB4',op=.55)
rect(0,0,44,84,'#2E3238',rx=9)
rect(4,6,36,66,'#4B535D',rx=5)
rect(14,74,16,3,'#5F6772',rx=1.5)
g_close()
# bras droit releve vers la tempe
path('M330,286 C362,282 386,262 392,232 C396,210 384,196 368,198 C354,200 348,216 350,232 C352,250 342,262 322,266 Z', fill=SWEAT)
ellipse(366,206,17,13,SKIN,transform='rotate(24 366 206)')
# tete + nuque
path('M300,254 C296,232 300,214 312,204 L344,206 C352,224 350,244 342,258 Z', fill=SKIND)
ellipse(322,176,50,54,SKIN,transform='rotate(-6 322 176)')
# oreille
ellipse(366,186,10,13,SKIND)
# cheveux (chignon flou)
path('M272,168 C268,120 300,96 336,100 C374,104 388,136 380,168 C374,146 356,128 330,126 C300,124 280,140 272,168 Z', fill=HAIR)
path('M276,150 C286,116 320,102 350,112 C332,110 300,120 288,150 Z', fill='#463A31')
circle(382,112,22,HAIR)
# meche detachee
path('M282,152 C272,176 274,196 284,208', stroke=HAIR, sw=4, fill='none')
# yeux baisses
path('M292,182 C298,190 308,190 314,183', stroke='#4A3F36', sw=3.4, fill='none')
path('M336,180 C342,188 352,188 357,181', stroke='#4A3F36', sw=3.4, fill='none')
# sourcils + bouche reposee
path('M290,168 C298,163 308,163 315,167', stroke='#4A3F36', sw=3, fill='none')
path('M335,166 C342,162 351,162 357,166', stroke='#4A3F36', sw=3, fill='none')
path('M312,214 C318,219 326,219 331,214', stroke='#A9705C', sw=3.2, fill='none')
ellipse(296,202,10,6,'#E9A88F',op=.5); ellipse(346,200,10,6,'#E9A88F',op=.5)

# ---- LE FIL : dispersion -> pause -> choix
# brouillon de boucles a gauche (dispersion)
d = 'M-10,300 C40,250 -4,206 46,180 C92,156 40,110 92,96 C132,86 150,120 128,140 C108,158 84,140 96,118'
path(d, stroke='#B9AE97', sw=3, fill='none')
path('M60,330 C96,300 70,262 108,244', stroke='#B9AE97', sw=3, fill='none')
# petites cartes flotantes (taches en suspens)
cards = [(24,246,'#E6DAC2'),(78,300,'#DFE6DC'),(30,352,'#EADFC8')]
for cx_,cy,c in cards:
    rect(cx_,cy,54,38,c,rx=5,stroke='#CFC3A9',sw=1.6)
    line(cx_+9,cy+13,cx_+45,cy+13,'#BCAF95',2.4)
    line(cx_+9,cy+25,cx_+34,cy+25,'#CBC0A6',2.4)
# fil principal : vient du brouillon, traverse la poitrine, fait une PAUSE nette, puis file a droite
main = ('M128,140 C170,150 196,206 214,262 C228,308 236,346 262,372 '
        'C292,402 336,392 352,360 C366,332 350,300 322,296 '
        'C300,293 288,312 296,328 C306,346 336,344 372,330 '
        'C420,312 470,296 520,286 C560,278 596,272 624,262')
path(main, stroke=ACC, sw=4.4, fill='none')
# point de pause (= la ou on respire)
circle(300,326,9,PAPER,stroke=ACC,sw=4)
text(298,296,'pause','display_ital',23,GREEN,anchor='middle')
# fleche vers la carte produit
path('M600,268 L628,258 L612,288 Z', fill=ACC)
# (rappel du message volontairement retire : le titre suffit)
g_close()

# ---- CARTE PRODUIT qui deborde de la scene (soutient l'histoire)
PX, PY = 1176, 430
rect(PX-8,PY-8,392,452,'#E9E0CD',rx=14)      # ombre plate
rect(PX,PY,376,436,PAPER,rx=12)
rect(PX,PY,376,436,'none',rx=12,stroke='#DDD3BE',sw=2)
text(PX+26,PY+44,'À PARTIR DE VOS RÉPONSES','body_bold',14,GREEN,ls=1.8)
line(PX+26,PY+64,PX+350,PY+64,LINE,2)
text(PX+26,PY+108,'Ce qui vous occupe vraiment','body',18,'#3D423C')
for i,(t,op) in enumerate([('Le rapport à rendre vendredi',1),('Les messages à ne pas oublier',.9),('Le sport laissé de côté',.75)]):
    yy = PY+142+i*38
    circle(PX+34,yy-6,7,'#B7AB92')
    text(PX+52,yy,t,'body',19,'#4A4F48',op=max(op,.8))
    if i<2: line(PX+52,yy+13,PX+52+W('body',19,t),yy+13,'#A79B83',1.8)
# priorite choisie
rect(PX+20,PY+246,336,62,'#EAF1EA',rx=8)
circle(PX+46,PY+277,13,ACC)
path('M'+str(PX+39)+','+str(PY+277)+' l5,6 l12,-13', stroke='#FFFFFF', sw=3.4, fill='none')
text(PX+66,PY+270,'Priorité choisie avec vous','body_bold',18,INK)
text(PX+66,PY+294,'« Ouvrir le doc, écrire trois phrases. »','display_ital',18,'#3D423C')
# question ouverte -> puis une seule action proposee
text(PX+26,PY+336,'On reprend par quoi ?','display_ital',22,'#C6431A')
text(PX+26,PY+362,'PROCHAINE ACTION PROPOSÉE','body_bold',12,INK2,ls=1.6)
rect(PX+26,PY+372,300,40,PAPER,rx=7,stroke=ACC,sw=2.4)
text(PX+42,PY+398,'Écrire 3 phrases — maintenant','body_bold',17,INK)
text(PX+336,PY+399,'›','body_bold',22,ACC)

# ================================================================ 4. BANDEAU RECONNAISSANCE
BY = 1128
rect(0,BY,W_PAGE,372,'#FFFFFF')
text(64,BY+56,'CE MOMENT-LÀ','body_bold',15,GREEN,ls=2.4)
line(64,BY+76,1536,BY+76,LINE,1)
items = [
 ("22 h 41","Le fil défile encore, la soirée passe sans que rien n’avance."),
 ("« Je commence à quoi, là ? »","Dix choses attendent, aucune ne prend la première place."),
 ("Un onglet ouvert depuis trois jours","On le ferme, on le rouvre, on remet à demain."),
 ("La même liste, chaque soir","Elle grossit au lieu de se trier toute seule."),
]
cw = (1536-64-3*36)/4
MAXW = cw-52
for i,(t,s) in enumerate(items):
    x = 64+i*(cw+36)
    rect(x,BY+104,cw,196,'#FAF7EF',rx=6)
    line(x,BY+104,x,BY+300,ACC if False else LINE,1)
    rect(x,BY+104,4,196,ACC)
    ts=24
    while W('display_bold',ts,t)>MAXW and ts>18: ts-=1
    if W('display_bold',ts,t)>MAXW: WARN.append('TITRE TROP LONG: '+t)
    text(x+26,BY+146,t,'display_bold',ts,INK)
    # wrap simple sur 2 lignes max
    words=s.split(); l1=''; l2=''
    for wd in words:
        if W('body',18,l1+wd+' ')<=MAXW and not l2: l1+=wd+' '
        else: l2+=wd+' '
    text(x+26,BY+182,l1.strip(),'body',18,'#4A4F48')
    if l2: text(x+26,BY+210,l2.strip(),'body',18,'#4A4F48')
    if len(l1.split())+len(l2.split()) < len(s.split()): WARN.append(' MOTS PERDUS: '+s)
    if W('body',18,l1.strip())>MAXW or W('body',18,l2.strip())>MAXW: WARN.append(' LIGNE TROP LONGUE: '+s[:30])
text(64,BY+344,'Vous vous reconnaissez dans une seule de ces scènes ? Le point que nous proposons part de là.','display_reg',23,'#4E534C')

# ================================================================ 5. COMMENT ÇA MARCHE (vert profond)
SYK = 1500
rect(0,SYK,W_PAGE,556,GREEN)
text(64,SYK+70,'COMMENT ÇA SE PASSE','body_bold',15,'#8FBBA3',ls=1.8)
text(64,SYK+128,'Trois mouvements, pas un système à apprendre.','display_bold',40,'#F6EFE0')
steps = [
 ("1","Faire le point","Quelques questions simples sur ce qui vous occupe en ce moment. Vous répondez avec vos mots."),
 ("2","Choisir une priorité","Nous vous proposons ce qui semble tenir le plus. Vous gardez le dernier mot."),
 ("3","Passer à l’action","Vous repartez avec une première étape assez petite pour être faite tout de suite."),
]
sw_ = 452; gap = 40; sx0 = 64
MAXW2 = sw_-96
# fil continu entre les etapes
path(f'M{sx0+sw_+8},{SYK+250} C{sx0+sw_+30},{SYK+230} {sx0+sw_+gap-30},{SYK+270} {sx0+sw_+gap-8},{SYK+250}',
     stroke='#3E7F63', sw=3, fill='none')
path(f'M{sx0+2*sw_+gap+8},{SYK+250} C{sx0+2*sw_+gap+30},{SYK+270} {sx0+2*sw_+2*gap-30},{SYK+230} {sx0+2*sw_+2*gap-8},{SYK+250}',
     stroke='#3E7F63', sw=3, fill='none')
for i,(n,t,d) in enumerate(steps):
    x = sx0 + i*(sw_+gap)
    circle(x+26, SYK+240, 26, ACC)
    text(x+26, SYK+250, n, 'display_bold', 28, '#FFFFFF', anchor='middle')
    text(x+70, SYK+252, t, 'display_bold', 32, '#FFFFFF')
    if x+70+W('display_bold',32,t) > x+sw_: WARN.append('TITRE ETAPE LARGE: '+t)
    words=d.split(); lines=[]; cur=''
    for wd in words:
        if W('body',19,cur+wd+' ') <= MAXW2: cur+=wd+' '
        else: lines.append(cur.strip()); cur=wd+' '
    lines.append(cur.strip())
    if len(lines)>3: WARN.append('ETAP3 TROP DE LIGNES: '+t)
    if any(W('body',19,l)>MAXW2 for l in lines): WARN.append('ETAP2 TROP LONGUE: '+t)
    for j,ln in enumerate(lines[:3]):
        text(x+2, SYK+306+j*30, ln, 'body', 19, '#CFE0D4')
text(64, SYK+492,'Chaque écran vous montre ce qui vient ensuite, avant que vous alliez plus loin.',
     'body',19,'#A9CBB6')

# ================================================================ 6. CONFIANCE
TY = 2056
rect(0,TY,W_PAGE,268,'#FFFFFF')
text(64,TY+52,'CE QUE NOUS POUVONS VOUS PROMETTRE ICI, MAINTENANT','body_bold',15,GREEN,ls=1.6)
promises = [
 ("Vos réponses restent les vôtres","Aucune publication sur vos réseaux, aucune revente de vos réponses."),
 ("Vous pouvez vous arrêter quand vous voulez","Rien ne vous retient sur une étape ; vous reprenez où vous vous êtes arrêté."),
 ("Les durées dépendent de vos réponses","Nous n’affichons pas de minute annoncée tant que le parcours n’est pas mesuré."),
]
pw = (1536-64-2*44)/3
MAXW3 = pw-46
for i,(t,d) in enumerate(promises):
    x=64+i*(pw+44)
    line(x,TY+96,x,TY+228,LINE,2)
    ts2=23
    while W('display_bold',ts2,t)>MAXW3 and ts2>18: ts2-=1
    if W('display_bold',ts2,t)>MAXW3: WARN.append('TITRE CONFIANCE LARGE: '+t)
    text(x+28,TY+126,t,'display_bold',ts2,INK)
    words=d.split(); lines=[]; cur=''
    for wd in words:
        if W('body',18,cur+wd+' ')<=MAXW3: cur+=wd+' '
        else: lines.append(cur.strip()); cur=wd+' '
    lines.append(cur.strip())
    if len(lines)>3: WARN.append('CONFIANCE TROP DE LIGNES: '+t)
    if any(W('body',18,l)>MAXW3 for l in lines): WARN.append('CONFIANCE TROP LONGUE: '+t)
    for j,ln in enumerate(lines[:3]):
        text(x+28,TY+160+j*28,ln,'body',18,'#4A4F48')

# ================================================================ 7. CTA FINAL
CY = 2324
rect(0,CY,W_PAGE,236,GREEN2)
text(64,CY+78,'Le fil est encore là. Il suffit de le reprendre quelque part.','display_bold',36,'#F6EFE0')
text(64,CY+118,'Commencez par répondre à quelques questions. Vous verrez le résultat avant de décider de la suite.',
     'body',20,'#B9D4C2')
BW2 = W('body_bold',22,'Trouver ma prochaine action')+2*32
rect(64,CY+146,BW2,62,ACC,rx=8)
text(64+32,CY+146+40,'Trouver ma prochaine action','body_bold',22,'#FFFFFF')
text(64+BW2+26,CY+146+40,'Le premier point est accessible sans payer, sans engagement.',
     'body',18,'#B9D4C2')
text(1536,CY+206,'« Reprendre le fil » : symbole provisoire — nom et domaines à vérifier avant publication','body',17,'#A9CBB6',anchor='end')

# ================================================================ ASSEMBLE
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_PAGE}" height="{H_PAGE}" '
       f'viewBox="0 0 {W_PAGE} {H_PAGE}">'
       '<defs><style>@font-face{font-family:"display_bold";src:url("file:///usr/share/fonts/X11/Type1/c0649bt_.pfb");font-weight:bold}'
       '@font-face{font-family:"display_reg";src:url("file:///usr/share/fonts/X11/Type1/c0648bt_.pfb")}'
       '@font-face{font-family:"display_ital";src:url("file:///usr/share/fonts/X11/Type1/c0633bt_.pfb");font-style:italic;font-weight:bold}'
       '@font-face{font-family:"body";src:url("file:///usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf")}'
       '@font-face{font-family:"body_bold";src:url("file:///usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf");font-weight:bold}'
       '</style></defs>'
       f'<rect width="{W_PAGE}" height="{H_PAGE}" fill="{CANV}"/>'
       + "\n".join(S) + '</svg>')
open('accueil.svg','w').write(svg)
cairosvg.svg2png(bytestring=svg.encode(), write_to='accueil.png', output_width=W_PAGE, output_height=H_PAGE)
print('OK -> accueil.png', os.path.getsize('accueil.png'))
if WARN:
    print('--- ALERTES ---'); [print(w) for w in WARN]
else:
    print('aucun debordement detecte')
