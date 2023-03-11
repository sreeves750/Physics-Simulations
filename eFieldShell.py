GlowScript 3.2 VPython

scene = display(height=500, width=600, background=vec(0.15,0.15,0.15))
g1 = graph(height=200, title="E-Field at Center", xtitle="distance (m)", ytitle="Electric Field (N/C)")
ge = gcurve(color=color.red)

#Define Constants
k = 9e9
sec = 80
rad = 9
arwSpc = 3
outer = 3 * arwSpc
dz = 0.3
a = -rad - outer
b = -rad - outer
c = -rad - outer
dtheta = 2 * pi / sec
dphi = pi / sec

#Create Objects
shell = sphere(pos=vec(0,0,0), radius=rad, thickness=0.5, axis=vec(1,0,0), color=color.white, opacity= 0.4)
shell.q = 3e-8
shell.area = 4 * pi * rad**2

#Calculate
E = vec(0,0,0)
while a <= rad + outer:  
  while b <= rad + outer:
    while c <= rad + outer:
      Obslocation = vec(a, b, c)
      rt = Obslocation - shell.pos
      if (mag(rt)-rad > dz or mag(rt)-rad < -dz):
        Earrow = arrow(pos=Obslocation, axis=Esum(rt), color=color.cyan)
      c += arwSpc
    c = -rad - outer
    b += arwSpc
  b = -rad - outer
  a += arwSpc

# For the graph
a = -2 * rad
while a <= 2 * rad:
  Obslocation = vec(a,0,0)
  rt = Obslocation - shell.pos
  if mag(rt)-rad > dz or mag(rt)-rad < -dz:
    E = Esum(rt)
    ge.plot(a, mag(E))
  a += rad / 20
  
plotArea()

def Esum(rt):
  E = vec(0,0,0)
  theta = 0
  phi = dphi
  while phi < pi:
    while theta < 2 * pi:
      dq = shell.q * (rad**2 * sin(phi) * dtheta * dphi) / shell.area
      r = rt - rad * vec(cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi))
      E += k*(dq)/(mag(r)**2)*hat(r)
      theta += dtheta
    theta = 0
    phi += dphi
  return E
  
def plotArea():
  theta = 0
  phi = dphi
  while phi < pi:
    while theta < 2 * pi:
      r = shell.pos + rad * vec(cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi))
      point = points(pos=r, color=color.yellow)
      theta += dtheta
    theta = 0
    phi += dphi
