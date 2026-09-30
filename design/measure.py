from PIL import ImageFont
P = {
 'display_bold': '/usr/share/fonts/X11/Type1/c0649bt_.pfb',   # Bitstream Charter Bold
 'display_reg' : '/usr/share/fonts/X11/Type1/c0648bt_.pfb',   # Charter Regular
 'display_ital': '/usr/share/fonts/X11/Type1/c0633bt_.pfb',   # Charter Bold Italic
 'body'        : '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
 'body_bold'   : '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
}
def w(key,size,txt):
    f=ImageFont.truetype(P[key],size)
    b=f.getbbox(txt)
    return b[2]-b[0]
if __name__=='__main__':
    tests=[('display_bold',72,"Vous avez scrollé."),
           ('display_bold',72,"Maintenant, on reprend"),
           ('display_bold',72,"par quoi ?"),
           ('display_bold',72,"« Vous avez scrollé. Maintenant,"),
           ('display_ital',72,"reprends par quoi ? »"),
           ('display_bold',64,"Reprendre le fil"),
           ('display_bold',52,"Faire le point"),
           ('display_bold',52,"Choisir une priorité"),
           ('display_bold',52,"Passer à l’action"),
           ('display_bold',40,"Trouver ma prochaine action"),
           ('display_ital',40,"On reprend par quoi ?"),
           ('display_ital',34,"Fil"),
           ('display_bold',34,"REPRENDRE LE FIL"),
           ('display_bold',26,"REPRENDRE LE FIL"),
           ('display_bold',22,"REPRENDRE LE FIL"),
           ('body',22,"Quelques questions suffisent."),
           ('body',22,"Vous obtenez une lecture claire de votre situation"),
           ('body',22,"et une seule prochaine action à faire aujourd’hui."),
           ('body',20,"à qui s’adresse ce produit, quel moment il aide à traverser,"),
           ('body_bold',22,"Faire le point maintenant"),
           ('body',18,"Vos réponses ne sont pas revendues et ne publient rien sur vos comptes."),
           ('body',18,"C’est vous qui décidez de la prochaine étape."),
           ('body',18,"Le temps que vous y passez dépend de vos réponses."),
           ('body',18,"Commencez gratuitement par quelques questions."),
          ]
    for k,s,t in tests:
        print(f"{k:12s} {s:3d} {w(k,s,t):5d}  {t}")
