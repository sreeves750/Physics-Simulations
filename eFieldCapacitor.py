GlowScript 3.2 VPython

scene = display(height=500, width=600, background=vec(0.15,0.15,0.15))
g1 = graph(height=200, title="E-Field at Center", xtitle="distance (m)", ytitle="Electric Field (N/C)")
ge = gcurve(color=color.red)

#Define Constants
k = 9e9
sec = 70
sep = 2
size = 30
outer = 3
arwSpc = 3
offset = 0
a = -size/2 - sep - outer - 2
b = -size/2 - outer - offset
c = -size/2 - outer - offset

#Create Objects
panel1 = box(pos=vec(-sep,-offset,-offset), size=vec(0.1,size,size), color=color.red)
panel1.q = 2e-8
panel2 = box(pos=vec(sep,offset,offset), size=vec(0.1,size,size), color=color.blue)
panel2.q = -2e-8


#Calculate
E = vec(0,0,0)
while a <= size/2 + sep + outer:  
  while b <= size/2 + outer + offset:
    while c <= size/2 + outer + offset:
      Obslocation = vec(a, b, c)
      rt1 = Obslocation - panel1.pos
      rt2 = Obslocation - panel2.pos
      # Long conditional that can probably be simplified
      if ((rt1.x > 0.1 or rt1.x < -0.1) or ((rt1.y > size/2 or rt1.y < -size/2) or (rt1.z > size/2 or rt1.z < -size/2))):
        if (rt2.x > 0.1 or rt2.x < -0.1) or ((rt2.y > size/2 or rt2.y < -size/2) or (rt2.z > size/2 or rt2.z < -size/2)):
          Earrow = arrow(pos=Obslocation, axis=Esum(rt1, rt2), color=color.cyan)
      c += arwSpc
    c = -size/2 - outer - offset
    b += arwSpc
  b = -size/2 - outer - offset
  a += arwSpc
  
# For Center of the Capacitor
if (offset==0):
  a = -size/2 - sep - outer 
  while a <= size/2 + sep + outer:
    Obslocation = vec(a, 0, 0)
    rt1 = Obslocation - panel1.pos
    rt2 = Obslocation - panel2.pos
    if ((rt1.x > 0.01 or rt1.x < -0.01) or ((rt1.y > size/2 or rt1.y < -size/2) or (rt1.z > size/2 or rt1.z < -size/2))):
      if (rt2.x > 0.01 or rt2.x < -0.01) or ((rt2.y > size/2 or rt2.y < -size/2) or (rt2.z > size/2 or rt2.z < -size/2)):
        E = Esum(rt1, rt2)
        ge.plot(a, mag(E))
    a += 1/42 * arwSpc

plotArea()

def Esum(rt1, rt2):
  E = vec(0,0,0)
  for z in range(sec):
    for y in range(sec):
      ry = size * (1/2 - 1/(2*sec) - y/sec)
      rz = size * (1/2 - 1/(2*sec) - z/sec)
      r1 = rt1 - vec(0,ry, rz)
      r2 = rt2 - vec(0,ry, rz)
      E += k*(panel1.q/(sec**2))/(mag(r1)**2)*hat(r1)
      E += k*(panel2.q/(sec**2))/(mag(r2)**2)*hat(r2)
  return E
  
def plotArea():
  for z in range(sec):
    for y in range(sec):
      ry = size * (1/2 - 1/(2*sec) - y/sec)
      rz = size * (1/2 - 1/(2*sec) - z/sec)
      r1 = panel1.pos + vec(0,ry, rz)
      r2 = panel2.pos + vec(0,ry, rz)
      point = points(pos=[r1, r2], color=color.yellow)

