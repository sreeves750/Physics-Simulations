GlowScript 3.2 VPython

scene = display(height=500, width=600, background=vec(0.15,0.15,0.15))
g1 = graph(height=200, title="E-Field at Center", xtitle="distance (m)", ytitle="Electric Field (N/C)")
ge = gcurve(color=color.red)

#Define Constants
k = 9e9
tsec = 80
psec = 30
rad = 9
outer = 3
dz = 2
arwSpc = 3
a = -2*rad
b = -rad - outer
c = -rad - outer
dtheta = 2*pi/tsec
drho = rad/psec

#Create Objects
disk = cylinder(pos=vec(0,0,0), axis=vec(0.5,0,0), radius=rad, color=color.white)
disk.q = 1.6e-8
disk.area = pi * rad**2

#Calculate
while a <= 2*rad:  
  while b <= rad + outer:
    while c <= rad + outer:
      Obslocation = vec(a, b, c)
      rt = Obslocation - disk.pos
      if ((rt.x > dz or rt.x < -dz) or mag(rt)-rad > dz) and not (b==0 and c==0):
        Earrow = arrow(pos=Obslocation, axis=Esum(rt), color=color.cyan)
      c += arwSpc
    c = -rad - outer
    b += arwSpc
  b = -rad - outer
  a += rad/4

# For center of Disk
a = -2*rad
while a <= 2*rad:
  Obslocation = vec(a,0,0)
  rt = Obslocation - disk.pos
  if (rt.x > dz or rt.x < -dz):
    E = Esum(rt)
    Earrow = arrow(pos=Obslocation, axis=E, color=color.red)
    ge.plot(a, mag(E))
  a += rad/4
  
plotArea()

def Esum(rt):
  E = vec(0,0,0)
  rho = drho
  theta = 0
  while rho <= rad:
    while theta < 2 * pi:
      dq = disk.q * (rho * drho * dtheta) / disk.area
      r = rt - vec(0,rho * sin(theta), rho * cos(theta))
      E += k*(dq)/(mag(r)**2)*hat(r)
      theta += dtheta
    theta = 0
    rho += drho
  return E
  
def plotArea():
  rho = drho
  theta = 0
  while rho <= rad:
    while theta < 2 * pi:
      r = disk.pos + vec(0,rho * sin(theta), rho * cos(theta))
      point = points(pos=r, color=color.yellow)
      theta += dtheta
    theta = 0
    rho += drho
