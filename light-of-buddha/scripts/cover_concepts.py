from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];serif='/usr/share/fonts/opentype/urw-base35/NimbusRoman-Regular.otf';sans='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
for letter in ['A','C']:
 im=ImageOps.fit(Image.open(R/f'cover/concepts/concept-{letter}.png').convert('RGB'),(1600,2560),method=Image.Resampling.LANCZOS).convert('RGBA')
 # Typographic panel subtly consolidates negative space; artwork is retained separately.
 veil=Image.new('RGBA',im.size);v=ImageDraw.Draw(veil)
 for y in range(1100):v.line((0,y,1600,y),fill=(9,31,38,int(145*(1-y/1100))))
 im=Image.alpha_composite(im,veil);d=ImageDraw.Draw(im)
 def t(s,y,size,font=serif,color='#f7e9bd'):
  f=ImageFont.truetype(font,size);w=d.textlength(s,font=f);d.text(((1600-w)/2,y),s,font=f,fill=color)
 t('THE LIGHT',170,128);t('OF BUDDHA',310,142)
 d.line((610,515,990,515),fill='#d7bb78',width=2)
 t('30 Timeless Stories of Wisdom,',565,43,sans);t('Compassion & Inner Peace',628,43,sans)
 t('VOLUME ONE',740,35,sans)
 # A minimal dark footing makes the exact subordinate credit readable.
 foot=Image.new('RGBA',im.size);ImageDraw.Draw(foot).rectangle((0,2350,1600,2560),fill=(9,31,38,175));im=Image.alpha_composite(im,foot);d=ImageDraw.Draw(im)
 t('Compiled and Retold by Jaspal Singh',2410,49)
 im.convert('RGB').save(R/f'cover/concepts/cover-concept-{letter}.jpg',quality=95,subsampling=0)
Image.open(R/'release/kindle-cover.jpg').save(R/'cover/concepts/cover-concept-B.jpg',quality=95)
sheet=Image.new('RGB',(900,500),'#eee7da')
for i,l in enumerate('ABC'):
 im=Image.open(R/f'cover/concepts/cover-concept-{l}.jpg');im.thumbnail((290,465));sheet.paste(im,(i*300+5,5));ImageDraw.Draw(sheet).text((i*300+140,478),l,fill='black')
sheet.save(R/'cover/concepts/typographic-comparison.jpg')
