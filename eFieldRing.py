GlowScript 3.2 VPython

scene = display(height=500, width=600, background=vec(0.15,0.15,0.15))
g1 = graph(height=200, title="E-Field at Center", xtitle="distance (m)", ytitle="Electric Field (N/C)")
ge = gcurve(color=color.red)

#Define Constants
k = 9e9
sec = 200
rad = 9
outer = 3
dz = 3
arwSpc = 3
a = -2*rad
b = -rad - outer
c = -rad - outer

#Create Objects
hoop = ring(pos=vec(0,0,0), radius=rad, thickness=0.5, axis=vec(1,0,0), color=color.white)
hoop.q = 3.5e-8

#Calculate
E = vec(0,0,0)
while a <= 2*rad:  
  while b <= rad + outer:
    while c <= rad + outer:
      Obslocation = vec(a, b, c)
      rt = Obslocation - hoop.pos
      if ((rt.x > dz or rt.x < -dz) or (mag(rt)-rad > dz or mag(rt)-rad < -dz)) and not (b==0 and c==0):
        Earrow = arrow(pos=Obslocation, axis=Esum(rt), color=color.cyan)
      c += arwSpc
    c = -rad - outer
    b += arwSpc
  b = -rad - outer
  a += rad/4

# For center of Hoop
a = -2*rad
while a <= 2*rad:
  Obslocation = vec(a,0,0)
  rt = Obslocation - hoop.pos
  E = Esum(rt)
  Earrow = arrow(pos=Obslocation, axis=E, color=color.red)
  a += rad/6
  
#For the Graph
a = -2*rad
while a <= 2*rad:
  Obslocation = vec(a,0,0)
  rt = Obslocation - hoop.pos
  E = Esum(rt)
  ge.plot(a, mag(E))
  a += rad/24
  
plotArea()

def Esum(rt):
  E = vec(0,0,0)
  theta = 0
  while theta < 2 * pi:
    r = rt - vec(0,rad * sin(theta), rad * cos(theta))
    E += k*(hoop.q/sec)/(mag(r)**2)*hat(r)
    theta += 2 * pi / sec
  return E
  
def plotArea():
  theta = 0
  while theta < 2 * pi:
    r = hoop.pos + vec(0,rad * sin(theta), rad * cos(theta))
    point = points(pos=r, color=color.yellow)
    theta += 2 * pi / sec
