# calibration accessibilite (WCAG) - appliquee a build_home.py via exec
import re
src = open('build_home.py').read()

new = {}
new["ACC   = '#E2552B'   # couleur d'action (unique)"] = "ACC   = '#C6431A'   # couleur d'action (unique, blanc 4.8:1)"
new["INK2  = '#5C615A'   # texte secondaire"]        = "INK2  = '#4E534C'   # texte secondaire"
src = src.replace("\n".join([]), "")
for k,v in new.items():
    assert k in src, k
    src = src.replace(k,v)

# --- corrections ciblables par marqueur de commentaire
def rep(old,new_,count=None):
    global src
    assert old in src, 'INTROUVABLE: '+old[:70]
    src = src.replace(old,new_)

# A. produit card : citation raccourcie + taille ok
rep("text(PX+66,PY+294,'« Ouvrir le document et écrire trois phrases. »','display_ital',17,INK2)",
    "text(PX+66,PY+294,'« Ouvrir le doc, écrire trois phrases. »','display_ital',18,'#3D423C')")
rep("text(PX+44,PY+386,'Écrire 3 phrases — maintenant','body_bold',17,INK)",
    "text(PX+44,PY+386,'Écrire 3 phrases — maintenant','body_bold',18,INK)")
rep("text(PX+340,PY+387,'›','body_bold',22,ACC)","text(PX+338,PY+388,'›','body_bold',24,ACC)")
rep("text(PX+52,yy,t,'body',19,'#4A4F48',op=op)","text(PX+52,yy,t,'body',19,'#4A4F48',op=max(op,.8))")
rep("circle(PX+34,yy-6,7,'#CFC4AC')","circle(PX+34,yy-6,7,'#B7AB92')")
rep("text(PX+26,PY+108,'Ce qui vous occupe vraiment','body',17,INK2)",
    "text(PX+26,PY+108,'Ce qui vous occupe vraiment','body',18,'#3D423C')")
rep("line(PX+52,yy+13,PX+52+W('body',19,t),yy+13,'#C9BFA9',1.6)",
    "line(PX+52,yy+13,PX+52+W('body',19,t),yy+13,'#A79B83',1.8)")

# B. hero : souligne sous "par quoi ?", spacing kicker, acquis en colonne
rep("""text(CL,214,'POUR LES SOIRÉES OÙ ON A BEAUCOUP DÉFILÉ AVANT DE COMMENCER','body_bold',15,GREEN,ls=2.2)
if W('body_bold',15,'POUR LES SOIRÉES OÙ ON A BEAUCOUP DÉFILÉ AVANT DE COMMENCER')+2*CL > 810:
    WARN.append('kicker trop large')""",
    """KICK='POUR LES SOIRÉES OÙ ON A BEAUCOUP DÉFILÉ AVANT DE COMMENCER'
text(CL,214,KICK,'body_bold',15,GREEN,ls=1.4)
if W('body_bold',15,KICK)+1.4*(len(KICK)-1) > CW:
    WARN.append('kicker trop large')""")
rep("path('M'+str(CL)+',478 C160,470 210,486 258,477 C292,471 316,481 330,477', stroke=ACC, sw=5, fill='none')",
    "path('M'+str(CL)+',486 C150,478 200,494 250,485 C286,479 312,489 332,485', stroke=ACC, sw=5, fill='none')")
rep("""gy = 916
labels = ['Une lecture de votre situation','Une seule priorité','Une prochaine action']
sub =    ['Ce qui vous tire aujourd’hui','Ce qui attend depuis trop longtemps','Le premier geste, à votre portée']
cx = CL
for i,(lb,sb) in enumerate(zip(labels,sub)):
    circle(cx+11, gy-6, 11, ACC)
    text(cx+30, gy, lb, 'body_bold', 20, INK)
    text(cx+30, gy+28, sb, 'body', 17, INK2)
    cx += 236""",
    """gy = 906
labels = ['Une lecture de votre situation','Une seule priorité retenue','Une prochaine action concrète']
sub =    ['ce qui vous tire aujourd’hui','ce qui attend depuis trop longtemps','le premier geste, à votre portée']
for i,(lb,sb) in enumerate(zip(labels,sub)):
    yy = gy + i*34
    circle(CL+9, yy-7, 9, ACC)
    path(f'M{CL+3},{yy-7} l4,5 l9,-10', stroke='#FFFFFF', sw=2.6, fill='none')
    text(CL+30, yy, lb, 'body_bold', 20, INK)
    text(CL+30+W('body_bold',20,lb)+14, yy, '— '+sb, 'body', 18, '#4E534C')""")
rep("text(CL, 996,'Pas de diagnostic médical. Pas de compte à remonter.', 'body', 17, INK2)",
    "text(CL, 996,'Pas de diagnostic médical. Pas de compte à remonter.', 'body', 18, '#4E534C')")
rep("text(CL, 1024,'Chaque étape est visible avant d’être engagée.', 'body', 17, INK2)",
    "text(CL, 1024,'Chaque étape vous est montrée avant que vous alliez plus loin.', 'body', 18, '#4E534C')")
rep("text(CL+BW+26, 790+42, '— c’est vous qui gardez le choix final', 'body', 19, INK2)",
    "text(CL+BW+26, 790+42, '— sans compte à créer pour voir le résultat', 'body', 19, '#4E534C')")

# C. scene : telephone pose (paire), fil vers la question
rep("""g_open('transform="translate(232,452) rotate(-14)"')
rect(0,0,44,84,'#2E3238',rx=9)
rect(4,6,36,68,'#3D434B',rx=5)
rect(14,78,16,3,'#4A5058',rx=1.5)
g_close()""",
    """g_open('transform="translate(228,486) rotate(96)"')
rect(0,0,44,84,'#2E3238',rx=9)
rect(4,6,36,66,'#454C55',rx=5)
rect(14,74,16,3,'#5A626C',rx=1.5)
g_close()""")
rep("ellipse(250,470,20,15,SKIN,transform='rotate(-16 250 470)')",
    "ellipse(246,470,21,14,SKIN,transform='rotate(-8 246 470)')")
rep("text(300,300,'pause','display_ital',22,GREEN,anchor='middle')",
    "text(298,296,'pause','display_ital',23,GREEN,anchor='middle')")
rep("# fleche vers la carte produit\npath('M600,268 L628,258 L612,288 Z', fill=ACC)",
    "# fleche vers la carte produit\npath('M600,268 L628,258 L612,288 Z', fill=ACC)\n# rappel du message au-dessus de la scene\ntext(338,44,'On reprend par quoi ?','display_ital',30,'#C6431A',anchor='middle')")

# D. bandeau reconnaissance
rep("cw = (1536-64-3*36)/4","cw = (1536-64-3*36)/4\nMAXW = cw-52")
rep("        if W('body',18,l1+wd+' ')<=cw-52 and not l2: l1+=wd+' '",
    "        if W('body',18,l1+wd+' ')<=MAXW and not l2: l1+=wd+' '")
rep("    if l2: text(x+26,BY+210,l2.strip(),'body',18,'#4A4F48')\n    if l2 and len(l2.split())>len(s.split())/2: WARN.append('bloc trop long: '+s[:30])",
    "    if l2: text(x+26,BY+210,l2.strip(),'body',18,'#4A4F48')\n    if len(l1.split())+len(l2.split()) < len(s.split()): WARN.append(' MOTS PERDUS: '+s)\n    if W('body',18,l1.strip())>MAXW or W('body',18,l2.strip())>MAXW: WARN.append(' LIGNE TROP LONGUE: '+s[:30])")
rep("text(x+26,BY+146,t,'display_bold',24,INK)",
    "text(x+26,BY+146,t,'display_bold',24,INK)\n    if W('display_bold',24,t)>MAXW: WARN.append('TITRE TROP LONG: '+t)")
rep("rect(x,BY+104,4,196,ACC if i==0 else '#CFC7B6')","rect(x,BY+104,4,196,ACC)")
rep("text(64,BY+344,'Si vous vous reconnaissez dans une seule de ces scènes, la suite vous concerne.','display_reg',23,INK2)",
    "text(64,BY+344,'Vous vous reconnaissez dans une seule de ces scènes ? Le point que nous proposons part de là.','display_reg',23,'#4E534C')")

# E. section "comment ca marche"
rep("text(64,SYK+70,'COMMENT ÇA SE PASSE','body_bold',15,'#9EC6AE',ls=2.4)",
    "text(64,SYK+70,'COMMENT ÇA SE PASSE','body_bold',15,'#8FBBA3',ls=1.8)")
rep("text(64, SYK+492,'Chaque écran vous montre ce qui va suivre avant que vous alliez plus loin.',\n     'body',19,'#A9CBB6')",
    "text(64, SYK+492,'Chaque écran vous montre ce qui vient ensuite, avant que vous alliez plus loin.',\n     'body',19,'#A9CBB6')")
rep("        if W('body',19,cur+wd+' ') <= sw_-90: cur+=wd+' '\n        else: lines.append(cur.strip()); cur=wd+' '",
    "        if W('body',19,cur+wd+' ') <= MAXW2: cur+=wd+' '\n        else: lines.append(cur.strip()); cur=wd+' '")
rep("sw_ = 452; gap = 40; sx0 = 64","sw_ = 452; gap = 40; sx0 = 64\nMAXW2 = sw_-96")
rep("    for j,ln in enumerate(lines[:3]):\n        text(x+2, SYK+306+j*30, ln, 'body', 19, '#CFE0D4')",
    "    if len(lines)>3: WARN.append('ETAP3 TROP DE LIGNES: '+t)\n    if any(W('body',19,l)>MAXW2 for l in lines): WARN.append('ETAP2 TROP LONGUE: '+t)\n    for j,ln in enumerate(lines[:3]):\n        text(x+2, SYK+306+j*30, ln, 'body', 19, '#CFE0D4')")
rep("text(x+70, SYK+252, t, 'display_bold', 32, '#FFFFFF')",
    "text(x+70, SYK+252, t, 'display_bold', 32, '#FFFFFF')\n    if x+70+W('display_bold',32,t) > x+sw_: WARN.append('TITRE ETAPE LARGE: '+t)")

# F. confiance
rep("text(64,TY+52,'CE SUR QUOI ON PEUT VOUS ATTESTER DÈS AUJOURD’HUI','body_bold',15,GREEN,ls=2.2)",
    "text(64,TY+52,'CE QUE NOUS POUVONS VOUS PROMETTRE ICI, MAINTENANT','body_bold',15,GREEN,ls=1.6)")
rep("pw = (1536-64-2*44)/3","pw = (1536-64-2*44)/3\nMAXW3 = pw-46")
rep("        if W('body',18,cur+wd+' ')<=pw-40: cur+=wd+' '\n        else: lines.append(cur.strip()); cur=wd+' '\n    lines.append(cur.strip())\n    for j,ln in enumerate(lines[:3]):\n        text(x+28,TY+160+j*28,ln,'body',18,'#4A4F48')",
    "        if W('body',18,cur+wd+' ')<=MAXW3: cur+=wd+' '\n        else: lines.append(cur.strip()); cur=wd+' '\n    lines.append(cur.strip())\n    if len(lines)>3: WARN.append('CONFIANCE TROP DE LIGNES: '+t)\n    if any(W('body',18,l)>MAXW3 for l in lines): WARN.append('CONFIANCE TROP LONGUE: '+t)\n    if W('display_bold',23,t)>MAXW3: WARN.append('TITRE CONFIANCE LARGE: '+t)\n    for j,ln in enumerate(lines[:3]):\n        text(x+28,TY+160+j*28,ln,'body',18,'#4A4F48')")

# G. CTA final
rep("text(64,CY+118,'Commencez par répondre à quelques questions — vous verrez le résultat avant de décider de la suite.',\n     'body',20,'#B9D4C2')",
    "text(64,CY+118,'Commencez par répondre à quelques questions. Vous verrez le résultat avant de décider de la suite.',\n     'body',20,'#B9D4C2')")
rep("text(64+BW2+26,CY+146+40,'Accès gratuit au premier point — sans engagement.',\n     'body',18,'#B9D4C2')",
    "text(64+BW2+26,CY+146+40,'Le premier point est accessible sans payer, sans engagement.',\n     'body',18,'#B9D4C2')")
rep("text(1536,CY+206,'Reprendre le fil · nom provisoire, disponibilité non vérifiée','body',16,'#7FA88F',anchor='end')",
    "text(1536,CY+206,'« Reprendre le fil » : symbole provisoire — nom et domaines à vérifier avant publication','body',16,'#8FBBA3',anchor='end')")
rep("text(116+wlogo+14,56,'nom provisoire','body',15,INK2)",
    "text(116+wlogo+14,56,'· symbole provisoire','body',15,'#4E534C')")

open('build_home_v2.py','w').write(src)
print('v2 ecrite,', len(src), 'octets')
