def L(hexs):
    hexs=hexs.lstrip('#'); r,g,b=[int(hexs[i:i+2],16)/255 for i in (0,2,4)]
    def t(c): return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    r,g,b=t(r),t(g),t(b); return 0.2126*r+0.7152*g+0.0722*b
def CR(a,b):
    la,lb=L(a),L(b)
    hi,lo=max(la,lb),min(la,lb); return (hi+0.05)/(lo+0.05)
pairs = [
 ('INK on PAPER','#22261F','#FBF8F1'),
 ('#3D423C on PAPER','#3D423C','#FBF8F1'),
 ('INK2 on PAPER','#5C615A','#FBF8F1'),
 ('GREEN on PAPER','#155C46','#FBF8F1'),
 ('white on ACC','#FFFFFF','#E2552B'),
 ('white on GREEN','#FFFFFF','#155C46'),
 ('#F6EFE0 on GREEN','#F6EFE0','#155C46'),
 ('#CFE0D4 on GREEN','#CFE0D4','#155C46'),
 ('#A9CBB6 on GREEN','#A9CBB6','#155C46'),
 ('#F6EFE0 on GREEN2','#F6EFE0','#0E4535'),
 ('#B9D4C2 on GREEN2','#B9D4C2','#0E4535'),
 ('#7FA88F on GREEN2','#7FA88F','#0E4535'),
 ('INK on CANV','#22261F','#F3EFE4'),
 ('INK2 on CANV','#5C615A','#F3EFE4'),
 ('#4A4F48 on #FAF7EF','#4A4F48','#FAF7EF'),
 ('INK on #FAF7EF','#22261F','#FAF7EF'),
 ('ACC on PAPER','#E2552B','#FBF8F1'),
]
for n,a,b in pairs: print(f'{n:24s} {CR(a,b):5.2f}')
