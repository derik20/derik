src=open('build_home_v2.py').read()
def rep(old,new):
    global src
    assert old in src,'INTROUVABLE: '+old[:60]
    src=src.replace(old,new)

# --- 1. suppression du rappel manuscrit redondant dans la scene
rep("# rappel manuscrit dans une zone libre de la scene\ntext(352,700,'On reprend par quoi ?','display_ital',30,'#C6431A',anchor='middle')\npath('M212,712 C260,704 330,718 400,708 C460,700 490,712 500,708', stroke='#C6431A', sw=3, fill='none', op=.55)",
    "# (rappel du message volontairement retire : le titre suffit)")

# --- 2. telephone pose a cote de la personne (ecran eteint = fil ferme)
rep("""g_open('transform="translate(228,486) rotate(96)"')
rect(0,0,44,84,'#2E3238',rx=9)
rect(4,6,36,66,'#454C55',rx=5)
rect(14,74,16,3,'#5A626C',rx=1.5)
g_close()""",
    """g_open('transform="translate(430,506) rotate(-6)"')
ellipse(22,44,44,17,'#DCCFB4',op=.55)
rect(0,0,44,84,'#2E3238',rx=9)
rect(4,6,36,66,'#4B535D',rx=5)
rect(14,74,16,3,'#5F6772',rx=1.5)
g_close()""")

# --- 3. fin du fil = question ouverte avant l'interface
rep("text(PX+26,PY+44,'CE QUE VOUS OBTENEZ','body_bold',14,GREEN,ls=2)",
    "text(PX+26,PY+44,'À PARTIR DE VOS RÉPONSES','body_bold',14,GREEN,ls=1.8)")
rep("# prochaine action\ntext(PX+26,PY+344,'PROCHAINE ACTION','body_bold',13,INK2,ls=2)\nrect(PX+26,PY+358,300,44,PAPER,rx=7,stroke=ACC,sw=2.4)\ntext(PX+44,PY+386,'Écrire 3 phrases — maintenant','body_bold',18,INK)\ntext(PX+338,PY+388,'›','body_bold',24,ACC)",
    "# question ouverte -> puis une seule action proposee\ntext(PX+26,PY+336,'On reprend par quoi ?','display_ital',22,'#C6431A')\ntext(PX+26,PY+362,'PROCHAINE ACTION PROPOSÉE','body_bold',12,INK2,ls=1.6)\nrect(PX+26,PY+372,300,40,PAPER,rx=7,stroke=ACC,sw=2.4)\ntext(PX+42,PY+398,'Écrire 3 phrases — maintenant','body_bold',17,INK)\ntext(PX+336,PY+399,'›','body_bold',22,ACC)")

# --- 4. carte produit plus haute, sans chevauchement avec le bandeau
rep("PX, PY = 1176, 470","PX, PY = 1176, 430")
rep("rect(PX-8,PY-8,392,438,'#E9E0CD',rx=14)","rect(PX-8,PY-8,392,452,'#E9E0CD',rx=14)")
rep("rect(PX,PY,376,420,PAPER,rx=12)","rect(PX,PY,376,436,PAPER,rx=12)")
rep("rect(PX,PY,376,420,'none',rx=12,stroke='#DDD3BE',sw=2)","rect(PX,PY,376,436,'none',rx=12,stroke='#DDD3BE',sw=2)")

# --- 5. micro-copie honnete sur la gratuité (a verifier avant publication)
rep("'— sans compte à créer pour voir le résultat'","'— aucune donnée publiée sur vos comptes'")

open('build_home_v3.py','w').write(src)
print('v3 ok')
