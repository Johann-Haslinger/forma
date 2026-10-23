"""Generate original, deterministic percussion one-shots. No external samples."""
import math, random, wave, struct, pathlib
root=pathlib.Path(__file__).resolve().parents[1]/'public/sounds'
root.mkdir(parents=True,exist_ok=True)
sr=22050
for ki,kit in enumerate(['classic','dream','rage','melodic']):
 for inst in ['kick','snare','hat']:
  rng=random.Random(ki*100+len(inst)); duration={'kick':[.48,.85,.36,.3],'snare':[.22,.6,.26,.4],'hat':[.09,.42,.05,.2]}[inst][ki]
  samples=[];phase=0;prev=0;low=0
  for i in range(int(sr*duration)):
   t=i/sr;n=rng.uniform(-1,1);hp=n-prev;prev=n;low+=.13*(n-low)
   if inst=='kick':
    start=[150,90,235,115][ki];end=[47,33,52,65][ki];freq=end+(start-end)*math.exp(-t*[32,18,55,45][ki]);phase+=2*math.pi*freq/sr
    x=math.sin(phase)*math.exp(-t*[12,6,17,19][ki]);x+=hp*math.exp(-t*220)*[.08,.01,.35,.13][ki]
    if ki==2:x=math.tanh(x*3)*.8
    if ki==3:x+=math.sin(phase*1.5)*math.exp(-t*32)*.25
   elif inst=='snare':
    if ki==0:x=.65*hp*math.exp(-t*28)+.4*math.sin(2*math.pi*190*t)*math.exp(-t*35)
    elif ki==1:x=.7*low*math.exp(-t*9)+.2*math.sin(2*math.pi*780*t)*math.exp(-t*20)
    elif ki==2:
     env=sum(math.exp(-(t-a)*65) for a in [0,.013,.029,.047] if t>=a)
     x=math.tanh(hp*env*1.3)*math.exp(-t*9)+.12*math.sin(2*math.pi*260*t)*math.exp(-t*40)
    else:x=(math.sin(2*math.pi*330*t)+.5*math.sin(2*math.pi*520*t))*math.exp(-t*18)*.45+hp*math.exp(-t*25)*.25
   else:
    if ki==0:x=hp*math.exp(-t*65)*.4
    elif ki==1:x=(n-low)*math.exp(-t*12)*.22+math.sin(2*math.pi*9700*t)*math.exp(-t*22)*.07
    elif ki==2:x=sum((1 if math.sin(2*math.pi*f*t)>0 else -1) for f in [3443,4891,6151,8039])*math.exp(-t*105)*.1+hp*math.exp(-t*140)*.15
    else:x=sum(math.sin(2*math.pi*f*t) for f in [2450,3713,5281])*math.exp(-t*26)*.13
   x*=min(1,t/.0015);samples.append(x)
  peak=max(abs(v) for v in samples) or 1
  with wave.open(str(root/f'{kit}-{inst}.wav'),'wb') as w:
   w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(b''.join(struct.pack('<h',int(v/peak*.85*32767)) for v in samples))
