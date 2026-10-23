"""Render the original VELVET STATIC demo with the same samples, notes and levels.
Default: 40 bars (4 intro / 8 hook / 8 verse / 4 break / 16 final hook).
With "street": 32 bars, eight final hook bars.
"""
import json,math,wave,struct,pathlib,array,sys
root=pathlib.Path(__file__).resolve().parents[1];street='street' in sys.argv[1:];slug='seitenstrasse' if street else 'velvet-static';bank='street' if street else 'nocturne';p=json.loads((root/f'public/demo/{slug}.json').read_text());sr=22050
step=60/p['bpm']/4;bars=32 if street else 40;duration=bars*16*step+3;size=round(sr*duration)
mix=array.array('f',[0])*size;room=array.array('f',[0])*size;buffers={}
for name in ['kick','snare','hat','bass','keys' if street else 'guitar']:
 with wave.open(str(root/f'public/sounds/{bank}-{name}.wav')) as w:
  raw=array.array('h');raw.frombytes(w.readframes(w.getnframes()));buffers[name]=[v/32768 for v in raw]
count=0
for bar in range(bars):
 section='intro' if bar<4 else 'verse' if 12<=bar<20 else 'break' if 20<=bar<24 else 'hook'
 rootclip=[0,1,2,3][bar%4]
 for r,track in enumerate(p['tracks']):
  if section=='intro' and (r in [0,3] or (r==1 and bar<3) or (r==2 and bar<2)):continue
  if section=='break' and r in [0,3]:continue
  clip=rootclip if r>=3 else (bar%4)
  for i,vel in enumerate(track['clips'][clip]):
   if not vel:continue
   count+=1;note=track['notes'][clip][i] if r>=3 else 0
   rate=2**((track['pitch']+note)/12);source=buffers[['kick','snare','hat','bass','keys' if street else 'guitar'][r]]
   dur=len(source)/sr/rate;end=min(3.8 if r==4 else dur,dur*((.2+track['decay']/110) if r>=3 else (.3+track['decay']/70)))
   swing=(step*p['swing']/150 if i%2 else 0);start=round((bar*16*step+i*step+swing)*sr)
   level=track['level']/100*vel*(.55 if r>=3 else .8)
   if section=='verse' and r==4:level*=.75
   if section=='break' and r==2:level*=.6
   bright=p.get('tone',24)/100;cutoff=[1000+bright*1600,2200+bright*3000,4200+bright*6500,400+bright*850,900+bright*1900][r] if street else [700+bright*700,1800+bright*1800,3500+bright*1800,200+bright*450,500+bright*900][r]
   alpha=1-math.exp(-2*math.pi*min(cutoff,sr*.45)/sr);last=0;hp=0;previous=0;hp_alpha=math.exp(-2*math.pi*25/sr)
   for j in range(min(round(end*sr),size-start)):
    pos=j*rate;k=int(pos)
    if k+1>=len(source):break
    x=source[k]+(source[k+1]-source[k])*(pos-k);last+=alpha*(x-last)
    hp=hp_alpha*(hp+last-previous);previous=last
    env=min(1,max(0,(end-j/sr)/.04));v=hp*level*env
    mix[start+j]+=v
    if r==4:room[start+j]+=v*(.12 if street else .45)
    elif r==1:room[start+j]+=v*.12
# Diffuse short echoes create a room tail without third-party effects.
for delay,gain in [(.071,.17),(.137,.14),(.239,.12),(.381,.1),(.613,.075),(.977,.05), (1.43,.025)]:
 offset=round(delay*sr)
 for i in range(size-offset):mix[i+offset]+=room[i]*gain
for i in range(size):
 mix[i]=math.tanh(mix[i]*.9)*min(1,(size-i)/(sr*2.5))
peak=max(abs(v) for v in mix) or 1;gain=.92/peak
rms=math.sqrt(sum(v*v for v in mix)/size)*gain
pcm=array.array('h',(round(v*gain*32767) for v in mix))
with wave.open(str(root/f'public/demo/{slug}.wav'),'wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(pcm.tobytes())
print(json.dumps({'duration_seconds':round(duration,2),'bars':bars,'events':count,'peak':.92,'rms':round(rms,4)}))
