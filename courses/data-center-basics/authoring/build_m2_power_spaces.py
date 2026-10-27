"""Editable figures for facility zones and rack AC/DC power architecture."""
from pathlib import Path
from build_synced_media import txt,box,arrow,G,B,C,H,I
P=Path(__file__).resolve().parents[1]
def svg(name,body):
 (P/'figures/module2'/name).write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675"><style>text{font-family:Arial,sans-serif}</style><rect width="1200" height="675" fill="white"/>'+body+'</svg>')
def spaces():
 b=txt(195,65,'Black space',30,weight=700)+txt(600,65,'Grey space',30,weight=700)+txt(1005,65,'White space',30,weight=700)
 b+='<rect x="35" y="110" width="320" height="360" rx="18" fill="#243244"/><rect x="440" y="110" width="320" height="360" rx="18" fill="#EDF0F3" stroke="#9AA6B5" stroke-width="2"/><rect x="845" y="110" width="320" height="360" rx="18" fill="white" stroke="#8DC63F" stroke-width="2"/>'
 b+=txt(195,157,'Site / utility interface',24,fill='white',weight=700)+txt(600,157,'Power and cooling support',21,weight=700)+txt(1005,157,'IT equipment area',24,weight=700)
 # Transformer/substation symbol, illustrative rather than a switching schematic.
 b+='<g transform="translate(-10 0)"><path d="M130,225h150v75H130Z M155,210v15 M180,210v15 M205,210v15 M230,210v15 M255,210v15" fill="none" stroke="white" stroke-width="3"/>'
 for x in [165,205,245]:b+=f'<circle cx="{x}" cy="263" r="14" fill="none" stroke="white" stroke-width="2"/>'
 b+='</g>'
 b+=txt(195,342,'Substation',25,fill='white')+txt(195,389,'Site energy infrastructure',22,fill='white')
 b+=box('electrical',455,210,130,110,'Switchgear\nUPS',fill='white',stroke=B,size=20)+box('mechanical',615,210,130,110,'Pumps\ncooling',fill='white',stroke=C,size=21)
 b+=txt(600,389,'Electrical + mechanical plant',22)+txt(600,440,'Locations vary by project',19)
 for n,x in enumerate([865,965,1065]):
  b+=f'<rect x="{x}" y="205" width="80" height="130" rx="7" fill="#F0F6E7" stroke="#719E2F" stroke-width="2"/>'
  for j in range(4):b+=f'<rect x="{x+12}" y="{220+j*25}" width="56" height="14" rx="2" fill="white" stroke="#719E2F"/>'
 b+=txt(1005,389,'Servers · storage · networks',21)+txt(1005,440,'Local power / cooling can be here',18)
 b+=arrow('power-site',355,270,440,270,B)+txt(397.5,245,'Power',18,fill=B)+arrow('power-hall',760,270,845,270,B)+txt(802.5,245,'Power',18,fill=B)
 b+=arrow('heat-return',845,365,760,365,H)+txt(802.5,342,'Heat',18,fill=H)
 b+='<rect x="35" y="520" width="1130" height="105" rx="14" fill="#F7F9FB" stroke="#BCC6D0" stroke-width="2"/>'+txt(600,560,'Black space is not a universal category.',26,weight=700)+txt(600,598,'Other organizations use it for connectivity or wider support areas.',23)
 svg('facility-space-zones.svg',b)
def power():
 b=txt(35,43,'Rack DC busbar · Open Rack example',28,anchor='start',weight=700)
 b+=box('ac-in',35,125,150,110,'AC\nsupply',fill='#F0F1FA',stroke=B,size=25)
 b+=box('shelf',245,110,220,140,'Power shelf\nrectifiers\nAC → DC',fill='#F0F1FA',stroke=B,size=23)
 b+='<rect x="565" y="95" width="24" height="240" rx="4" fill="#343895"/>'+txt(577,72,'48 V DC',23,fill=B)+txt(577,364,'Rear rack busbar',22,fill=B)
 b+=arrow('ac-input',185,180,245,180,B)+arrow('shelf-dc',465,180,565,180,B)
 for i,y in enumerate([85,245]):
  b+=box('gear'+str(i),735,y,430,100,'Compatible IT gear\nDC–DC regulation',size=24)
  b+=arrow('tap'+str(i),589,y+50,735,y+50,B)
 b+=txt(883,215,'Blind-mate power contacts',21,fill=B)
 b+=txt(35,415,'Conventional AC-fed rack example',27,anchor='start',weight=700)
 b+=box('pdu',35,455,170,85,'Rack AC PDU',fill='#F0F1FA',stroke=B,size=21)+box('server-psu',315,455,260,85,'Server AC–DC PSU',fill='#F0F1FA',stroke=B,size=23)+box('regulation',735,455,430,85,'DC–DC → component voltages',size=23)
 b+=arrow('ac-cord',205,497.5,315,497.5,B)+txt(260,444,'AC cord',19,fill=B)+arrow('psu-out',575,497.5,735,497.5,B)+txt(655,479,'DC',20,fill=B)
 b+=txt(740,569,'Conversion and regulation inside each AC-input server',21)
 for i,label in enumerate(['Fewer server power cords','Front-access modular supplies','Pooled rectifier capacity']):b+=box('benefit'+str(i),35+i*385,595,360,60,label,fill='#F0F6E7',stroke=G,size=21)
 svg('rack-power-architectures.svg',b)
if __name__=='__main__':spaces();power();print('Built facility-zone and rack power figures.')
