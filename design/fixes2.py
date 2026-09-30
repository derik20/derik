src = open('build_home_v2.py').read()
def rep(old,new):
    global src
    assert old in src, 'INTROUVABLE: '+old[:60]
    src = src.replace(old,new)

# 1. bandeau reconnaissance : titres auto-dimensionnes + libelle court
rep('("Un onglet ouvert depuis trois jours","On le ferme, on le rouvre, on remet à demain."),',
    '("Un onglet ouvert depuis trois jours","On le ferme, on le rouvre, on remet à demain."),')
rep("""    text(x+26,BY+146,t,'display_bold',24,INK)
    if W('display_bold',24,t)>MAXW: WARN.append('TITRE TROP LONG: '+t)""",
    """    ts=24
    while W('display_bold',ts,t)>MAXW and ts>18: ts-=1
    if W('display_bold',ts,t)>MAXW: WARN.append('TITRE TROP LONG: '+t)
    text(x+26,BY+146,t,'display_bold',ts,INK)""")
# 2. confiance : titres auto-dimensionnes
rep("""    text(x+28,TY+126,t,'display_bold',23,INK)""",
    """    ts2=23
    while W('display_bold',ts2,t)>MAXW3 and ts2>18: ts2-=1
    if W('display_bold',ts2,t)>MAXW3: WARN.append('TITRE CONFIANCE LARGE: '+t)
    text(x+28,TY+126,t,'display_bold',ts2,INK)""")
rep("""    if W('display_bold',23,t)>MAXW3: WARN.append('TITRE CONFIANCE LARGE: '+t)\n""","")
# 3. rappel manuscrit : en bas de scene, sous le fil de dispersion (zone libre)
rep("# rappel du message au-dessus de la scene\ntext(338,44,'On reprend par quoi ?','display_ital',30,'#C6431A',anchor='middle')",
    "# rappel manuscrit dans une zone libre de la scene\ntext(352,700,'On reprend par quoi ?','display_ital',30,'#C6431A',anchor='middle')\npath('M212,712 C260,704 330,718 400,708 C460,700 490,712 500,708', stroke='#C6431A', sw=3, fill='none', op=.55)")
# 4. pied de page plus lisible sur vert sombre
rep("'body',16,'#8FBBA3',anchor='end'","'body',17,'#A9CBB6',anchor='end'")
# 5. audit geometrique : correction getmetrics
open('audit.py','w').write(open('audit.py').read().replace("asc,desc=f(k,s).getmetrics(t)[:2]","asc,desc=f(k,s).getmetrics()"))
open('build_home_v2.py','w').write(src)
print('fixes2 appliques')
