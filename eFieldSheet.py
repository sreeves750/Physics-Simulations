GlowScript 3.2 VPython

scene = display(height=500, width=600, background=vec(0.15,0.15,0.15))
g1 = graph(height=200, title="E-Field at Center", xtitle="distance (m)", ytitle="Electric Field (N/C)")
ge = gcurve(color=color.red)

#Define Constants
k = 9e9
sec = 50
size = 18
outer = 3
arwSpc = 3
a = -size/2 - outer
b = -size/2 - outer
c = -size/2 - outer

#Create Objects
panel = box(pos=vec(0,0,0), size=vec(0.1,size,size), color=color.white)
panel.q = 2e-8

#Calculate
while a <= size/2 + outer:  
  while b <= size/2 + outer:
    while c <= size/2 + outer:
      Obslocation = vec(a, b, c)
      rt = Obslocation - panel.pos
      if (rt.x > 0.1 or rt.x < -0.1) or ((rt.y > size/2 or rt.y < -size/2) or (rt.z > size/2 or rt.z < -size/2)):
        if b!=0 or c!=0:
          Earrow = arrow(pos=Obslocation, axis=Esum(rt), color=color.cyan)
      c += arwSpc
    c = -size/2 - outer
    b += arwSpc
  b = -size/2 - outer
  a += arwSpc
  
#For Center of the Sheet
a = -size/2 - outer
while a <= size/2 + outer:
  Obslocation = vec(a, 0, 0)
  rt = Obslocation - panel.pos
  E = Esum(rt)
  Earrow = arrow(pos=Obslocation, axis=E, color=color.red)
  ge.plot(a, mag(E))
  a += 2/3 * arwSpc

plotArea()

def Esum(rt):
  E = vec(0,0,0)
  for z in range(sec):
    for y in range(sec):
      ry = size * (1/2 - 1/(2*sec) - y/sec)
      rz = size * (1/2 - 1/(2*sec) - z/sec)
      r = rt - vec(0,ry, rz)
      E += k*(panel.q/(sec**2))/(mag(r)**2)*hat(r)
  return E

def plotArea():
  for z in range(sec):
    for y in range(sec):
      ry = size * (1/2 - 1/(2*sec) - y/sec)
      rz = size * (1/2 - 1/(2*sec) - z/sec)
      r = panel.pos + vec(0,ry, rz)
      point = points(pos=r, color=color.yellow)
