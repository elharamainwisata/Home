# Membuat kolase hotel 1000x520 (gedung kiri + 2 foto kamar kanan) dari ekspor brosur Canva & foto situs resmi hotel.
# Path S menunjuk folder kerja berisi ekspor Canva (canva/*.png) dan unduhan situs hotel (off/).
from PIL import Image
import os
S='/tmp/claude-501/-Users-macbookairm1-Desktop-elharamainwisata/49132d0e-f282-4662-8ec9-4ead4fd0d1a5/scratchpad/'
C=S+'canva/'; O=S+'off/'
pages={}
def page(n):
    if n not in pages: pages[n]=Image.open(C+n).convert('RGB')
    return pages[n]
def bro(n,x,y,w,h,ins=(5,5,9,11)):
    im=page(n); s=im.width/794
    return im.crop((round((x+ins[0])*s),round((y+ins[1])*s),round((x+w-ins[2])*s),round((y+h-ins[3])*s)))
def f(p): return Image.open(p).convert('RGB')
def fit(im,W,H,ay=.5):
    r=W/H; w,h=im.size
    if w/h>r: nw=h*r; x=(w-nw)/2; im=im.crop((round(x),0,round(x+nw),h))
    else: nh=w/r; y=(h-nh)*ay; im=im.crop((0,round(y),w,round(y+nh)))
    return im.resize((W,H),Image.LANCZOS)
def kolase(name,ext,in1,in2,ay=.5):
    W,H,g=1000,520,6; L=600
    c=Image.new('RGB',(W,H),'white')
    c.paste(fit(ext,L-g//2,H,ay),(0,0))
    rw=W-L-g//2; rh=(H-g)//2
    c.paste(fit(in1,rw,rh),(L+g//2,0)); c.paste(fit(in2,rw,H-rh-g),(L+g//2,rh+g))
    c.save(S+'kolase/'+name+'.jpg',quality=85,optimize=True,progressive=True); print(name)
row=lambda n,y,col,yy=None:bro(n,[39,290,540][col],y,236,161)
kolase('kolase-hotel-anjum',f(O+'c2/anj.jpg'),f(O+'anj_2280519.jpg'),f(O+'anj_2280521.jpg'))
kolase('kolase-hotel-marwa-rotana',f(O+'c2/rot_rc_175465242665_653.jpg'),f(O+'c2/rot_rc_175440065181_655.jpg'),row('jan10.png',409,1))
kolase('kolase-hotel-movenpick-hajar',f(O+'out/hotel-movenpick-hajar-makkah.jpg'),f(O+'c2/mv_HCM_P_4550835.jpg'),f(O+'c2/mv_HCM_P_6560434.jpg'))
kolase('kolase-hotel-fairmont',f(O+'c2/fm_a104-04.jpg'),f(O+'c2/fmr_met_p_a104-41.jpg'),f(O+'c2/fmr_met_p_a104-42.jpg'),ay=.6)
kolase('kolase-hotel-prestige',bro('dec9.png',61,788,170,290,(2,2,4,4)),bro('dec9.png',244,779,216,147,(3,3,5,5)),bro('dec9.png',473,779,216,147,(3,3,5,5)),ay=.3)
kolase('kolase-hotel-al-shohada',row('ram7.png',400,0),row('ram7.png',400,1),row('ram7.png',400,2))
kolase('kolase-hotel-royal-majestic',row('ram8.png',400,0),row('ram8.png',400,1),row('ram8.png',400,2))
kolase('kolase-hotel-royal-andalus',row('ram8.png',169,0),row('ram8.png',169,1),row('ram8.png',169,2))
kolase('kolase-hotel-al-aqeeq',row('jan10.png',870,0),row('jan10.png',870,1),row('jan10.png',870,2))
kolase('kolase-hotel-peninsula-worth',row('dec10.png',640,0),row('dec10.png',640,1),row('dec10.png',640,2))
kolase('kolase-hotel-movenpick-madinah',f(O+'c2/mv_HCM_P_1064748.jpg'),f(O+'c2/mv_HCM_P_9591914.jpg'),row('jan10.png',640,1))
