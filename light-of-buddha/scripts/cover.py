from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import shutil
ROOT=Path(__file__).resolve().parents[1]
SERIF='/usr/share/fonts/opentype/urw-base35/NimbusRoman-Regular.otf'
SANS='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
source=ROOT/'cover/final/cover-art-source.png'
image=ImageOps.fit(Image.open(source).convert('RGB'),(1600,2560),method=Image.Resampling.LANCZOS)
d=ImageDraw.Draw(image)
def text(s,y,size,font=SERIF,fill='#193f43'):
 f=ImageFont.truetype(font,size); box=d.textbbox((0,0),s,font=f); w=box[2]-box[0]; d.text(((1600-w)/2,y),s,font=f,fill=fill)
text('THE LIGHT',215,133)
text('OF BUDDHA',355,151)
d.line((625,555,975,555),fill='#92723d',width=2)
text('30 Timeless Stories of Wisdom,',597,46,SANS)
text('Compassion & Inner Peace',662,46,SANS)
text('VOLUME ONE',770,35,SANS)
text('Compiled and Retold by Jaspal Singh',2393,49,SERIF,fill='#fff1d1')
image.save(ROOT/'release/kindle-cover.jpg',quality=96,subsampling=0,dpi=(300,300))
image.save(ROOT/'cover/final/kindle-cover.png')
image.resize((200,320)).save(ROOT/'cover/final/thumbnail.jpg')
trip=Image.open(ROOT/'cover/concepts/three-concepts-source.png')
for n,(left,right) in enumerate([(0,573),(580,1147),(1154,1716)],1):
 trip.crop((left,0,right,trip.height)).save(ROOT/f'cover/concepts/concept-{chr(64+n)}.png')
(ROOT/'cover/typography/cover-text.txt').write_text('THE LIGHT OF BUDDHA\n30 Timeless Stories of Wisdom, Compassion & Inner Peace\nVOLUME ONE\nCompiled and Retold by Jaspal Singh\n')
