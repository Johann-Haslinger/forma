"""Original dry drums, rounded bass and muted minor keys for a 96 BPM rap pocket."""
import math,random,wave,struct,pathlib
root=pathlib.Path(__file__).resolve().parents[1]/'public/sounds';sr=22050
for name,duration in [('kick',.28),('snare',.17),('hat',.065),('bass',.8),('keys',1.05)]:
 rng=random.Random(961);phase=0;prev=0;low=0;data=[]
 for i in range(round(sr*duration)):
  t=i/sr;n=rng.uniform(-1,1);hp=n-prev;prev=n
  if name=='kick':
   phase+=2*math.pi*(49+100*math.exp(-t*65))/sr;x=math.sin(phase)*math.exp(-t*18)+hp*.1*math.exp(-t*260)
  elif name=='snare':x=hp*.4*math.exp(-t*45)+math.sin(2*math.pi*185*t)*.55*math.exp(-t*30)+math.sin(2*math.pi*310*t)*.12*math.exp(-t*60)
  elif name=='hat':x=hp*.25*math.exp(-t*95)+math.sin(2*math.pi*6100*t)*.04*math.exp(-t*120)
  elif name=='bass':
   phase+=2*math.pi*(65.406+4*math.exp(-t*80))/sr;x=(math.sin(phase)+.16*math.sin(2*phase)+.05*math.sin(3*phase))*math.exp(-t*5)*min(1,t/.006)
  else:
   x=0
   for f,amp in [(261.626,.6),(311.127,.28),(391.995,.2)]:x+=amp*(math.sin(2*math.pi*f*t)+.18*math.sin(2*math.pi*f*2*t)*math.exp(-t*12))
   x*=math.exp(-t*5.2)*min(1,t/.01)*(1+.06*math.sin(2*math.pi*4*t))
  low+=.35*(x-low);data.append(low*min(1,(duration-t)/.02))
 # Remove DC and normalize each original one-shot.
 alpha=math.exp(-2*math.pi*18/sr);last=0;state=0;filtered=[]
 for x in data:state=alpha*(state+x-last);last=x;filtered.append(state)
 peak=max(abs(v) for v in filtered) or 1
 with wave.open(str(root/f'street-{name}.wav'),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(b''.join(struct.pack('<h',round(v/peak*.85*32767)) for v in filtered))
