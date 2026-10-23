"""Original physical-model strings, sub bass and percussion for the Nocturne bank."""
import math,random,wave,struct,pathlib
root=pathlib.Path(__file__).resolve().parents[1]/'public/sounds';sr=22050

def string(freq,duration,seed):
 rng=random.Random(seed);size=round(sr/freq);ring=[rng.uniform(-1,1) for _ in range(size)];data=[]
 for i in range(round(duration*sr)):
  k=i%size;v=ring[k];ring[k]=.4985*(ring[k]+ring[(k+1)%size]);data.append(v)
 return data

def save(name,data):
 # Remove the physical-model string's DC component before normalization.
 alpha=math.exp(-2*math.pi*(55 if name=='guitar' else 15)/sr);previous=0;state=0;filtered=[]
 for x in data:
  state=alpha*(state+x-previous);previous=x;filtered.append(state)
 data=filtered
 peak=max(abs(x) for x in data) or 1
 with wave.open(str(root/f'nocturne-{name}.wav'),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(b''.join(struct.pack('<h',round(max(-1,min(1,x/peak*.86))*32767)) for x in data))

length=3.2;guitar=[0.] * round(sr*length)
for j,(freq,amp) in enumerate([(261.626,.9),(262.4,.3),(392.439,.1)]):
 a=string(freq,length,71+j)
 for i,x in enumerate(a):guitar[i]+=x*amp
# Amp saturation, dark cabinet, gentle chorus/double tracking.
low=0;dry=[]
for i,x in enumerate(guitar):
 low+=.11*(math.tanh(x*2.2)-low);dry.append(low*min(1,i/(sr*.045))*min(1,(len(guitar)-i)/(sr*.1)))
for i,x in enumerate(dry):
 delay=round(sr*(.017+.0015*math.sin(2*math.pi*.8*i/sr)));guitar[i]=x+(.28*dry[i-delay] if i>=delay else 0)
save('guitar',guitar)
for name,duration in [('bass',2.1),('kick',.42),('snare',.32),('hat',.12)]:
 rng=random.Random(303);data=[];phase=0;prev=0
 for i in range(round(sr*duration)):
  t=i/sr;n=rng.uniform(-1,1);hp=n-prev;prev=n
  if name=='bass':
   phase+=2*math.pi*(65.406+7*math.exp(-t*65))/sr;x=math.tanh((math.sin(phase)+.07*math.sin(phase*2))*1.7)*math.exp(-t*2.5)*min(1,t/.008)
  elif name=='kick':
   phase+=2*math.pi*(43+135*math.exp(-t*46))/sr;x=math.tanh(math.sin(phase)*1.8)*math.exp(-t*14)+hp*.12*math.exp(-t*240)
  elif name=='snare':
   env=sum(math.exp(-(t-a)*47) for a in [0,.011,.026] if t>=a);x=hp*.17*env+math.sin(2*math.pi*175*t)*.35*math.exp(-t*30)
  else:x=hp*math.exp(-t*65)*.17
  x*=min(1,t/.001);x*=min(1,(duration-t)/.015);data.append(x)
 save(name,data)
