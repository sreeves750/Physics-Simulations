Web VPython 3.2

scene = display(height=420, width=600, background=vec(0.15,0.15,0.15), autoscale = True)

#----------Define Constants----------#
epsilon0 = 8.85418782e-12
k = 1 / (4 * pi * epsilon0)
e = 1.60217663e-19

# Determined by percentiles from the 1s electron wave function for hydrogen
# https://www.desmos.com/calculator/6iuurwj6gh
probDist = [1.154e-11, 1.501e-11, 1.759e-11, 1.974e-11, 2.164e-11, 2.335e-11, 2.493e-11, 2.642e-11, 2.782e-11, 2.916e-11,
            3.045e-11, 3.169e-11, 3.289e-11, 3.406e-11, 3.521e-11, 3.633e-11, 3.742e-11, 3.851e-11, 3.957e-11, 4.062e-11,
            4.165e-11, 4.268e-11, 4.370e-11, 4.471e-11, 4.570e-11, 4.670e-11, 4.769e-11, 4.867e-11, 4.966e-11, 5.064e-11,
            5.162e-11, 5.260e-11, 5.357e-11, 5.455e-11, 5.553e-11, 5.651e-11, 5.749e-11, 5.848e-11, 5.947e-11, 6.046e-11,
            6.146e-11, 6.246e-11, 6.347e-11, 6.449e-11, 6.551e-11, 6.654e-11, 6.758e-11, 6.863e-11, 6.969e-11, 7.075e-11,
            7.184e-11, 7.293e-11, 7.403e-11, 7.514e-11, 7.627e-11, 7.742e-11, 7.858e-11, 7.976e-11, 8.095e-11, 8.217e-11,
            8.340e-11, 8.466e-11, 8.594e-11, 8.724e-11, 8.857e-11, 8.993e-11, 9.131e-11, 9.273e-11, 9.567e-11, 9.567e-11,
            9.719e-11, 9.876e-11, 10.037e-11, 10.203e-11, 10.373e-11, 10.550e-11, 10.732e-11, 10.921e-11, 11.118e-11, 11.321e-11,
            11.535e-11, 11.758e-11, 11.992e-11, 12.238e-11, 12.497e-11, 12.772e-11, 13.065e-11, 13.379e-11, 13.716e-11, 14.083e-11,
            14.484e-11, 14.928e-11, 15.426e-11, 15.994e-11, 16.658e-11, 17.460e-11, 18.479e-11, 19.888e-11, 22.242e-11, 27.506e-11]

#----------Initialize values----------#
number = 1200  # Subdivision of the electron
cloudRadius = 0.52918e-10 # Bohr's Radius
speedVar = 0.01 # Variance in orbital speed
frameSkip = 10 # Only display every 'frameSkip' frames

# External Efield
Eext = vec(0,0,0)
EextArrow = arrow(pos = vec(0,1.3e-10,0), axis = vec(0,0,0))

# Average for polarizability
polarizeTot = 0
polarizeAmt = 0

#----------Create Objects----------#
# Create reference points for the electron cloud
refcloud = sphere(pos=vec(0,0,0), radius = cloudRadius, color=color.white, opacity = 0.12)
avgCloud = sphere(pos=vec(0,0,0), radius = 3.5e-12, color=color.white)

# Widget for changing external electric field
Eslider = slider(max = 11, min = 2, step = 0.001 * (11-2), value = 2, bind=updateEext, top = 8, length = 500)
Edisplay = wtext(text = 0)
scene.append_to_caption('<br>')

Einput = winput(bind = updateEinput, prompt = "Input E-field:")
scene.append_to_caption('<br>')

# Widget for determining polarizability
PolCheck = checkbox(bind = togglePol)
PolDisplay = wtext(text = "Polarizability: 0")
scene.append_to_caption('<br>')

# Widget for showing time
TimeCheck = checkbox(bind = toggleTime)
TimeDisplay = wtext(text = "Stopwatch: 0")

# Create the proton
proton = sphere(pos = vec(0,0,0), radius = 4e-12, color = color.red)
proton.q = e
proton.p = vec(0,0,0)
proton.m = 1.67262192e-27
proton.E = vec(0,0,0)

# Create the electron cloud
electron = [sphere for i in range(number)]
for i in range(number):
  rho = probDist[round(random() * (len(probDist)-1) - 0.5)]
  tPos = rho * randVec()
  electron[i] = sphere(pos = tPos, radius = 1.8e-12, color = color.cyan, opacity = 0.4)
  electron[i].q = -e / number
  electron[i].m = 9.1093837e-31 / number
  electron[i].E = vec(0,0,0)

# Initialize momentum
tMom = vector(0,0,0)
aMom = vector(0,0,0)
loop = 0 # Debugging variable for how many loops it takes to determine the momentum
while loop < 200:
  tMom = vector(0,0,0)
  aMom = vector(0,0,0)
  for ePart in electron:
    radialVec = ePart.pos - proton.pos
    orthVec = vec(0,0,0)
    attempts = 0
    
    # Determine orbital speed
    E = k * proton.q * radialVec/ (mag(radialVec))**3
    speed = sqrt(mag(ePart.q * E) * mag(radialVec) / ePart.m) * (random() * speedVar + 1-speedVar/2)
    
    angleMom = 0
    while True:
      # Create a random vector orthogonal to the proton
      while True:
        orthVec = hat(cross(radialVec,randVec()))
        if orthVec != vec(0,0,0):
          break
      
      if ePart == electron[0]:
        break
      
      angleMom = acos(dot(orthVec, tMom)/(mag(orthVec) * mag(tMom)))
      attempts += 1
      
      # Have momentum initialize to decrease the current total momentum
      if attempts < 20:
        if angleMom > pi * 0.67:
          break
      else:
        break
    ePart.p = ePart.m * speed * orthVec
    tMom += ePart.p
    aMom += cross(ePart.pos - proton.pos, ePart.p)

  # Finish the loop when total momentum and angular momentum is low
  if (mag(tMom) < 1.8e-27 and mag(aMom) < 8e-37):
    break
  
  loop += 1

print("The Theoretical polarizability of Hydrogen is 1.646e-41")
# http://physicspages.com/pdf/Electrodynamics/Polarizability%20of%20hydrogen.pdf
print(f"Number: {number}")
print(f"Loops: {loop}")
print(f"Momentum: {formatOut(mag(tMom))}")
print(f"Angular Momentum: {formatOut(mag(aMom))}")

scene.autoscale = False

#----------Calculations----------#
deltat=2e-19
t=0
frame = 0
scene.pause() # wait for a click
while True:
  # Update time  
  t += deltat
  
  # Only update visuals every frameSkip frame
  if frame % frameSkip == 0:
    frame = 0
    rate(1e6)

    # Print Polarizability
    if mag(Eext) != 0 and PolCheck.checked:
      polarizability = polarizeTot / polarizeAmt
      PolDisplay.text = f"Polarizability: {formatOut(polarizability)}"
    else:
      PolDisplay.text = "Polarizability: 0"
    
    # Print Time
    if TimeCheck.checked:
      TimeDisplay.text = f"Stopwatch: {formatOut(t)}"
    else:
      TimeDisplay.text = "Stopwatch: 0"
  
  frame += 1
  
  resetE(proton, electron)
  updateE(proton, electron)
  update(proton, electron)
  
  # Update reference positions
  refcloud.pos = proton.pos
  avgPos = vec(0,0,0)
  for ePart in electron:
    avgPos += ePart.pos
  avgPos /= number
  avgCloud.pos = avgPos
  
  # Update polarizability
  if PolCheck.checked:
    polarize = e * (proton.pos.x - avgCloud.pos.x) / Eext.x
    polarizeTot += polarize
    polarizeAmt += 1
  
# Resets the E-field of the particles to the external E-field
def resetE(*args):
  for particle in args:
    if isinstance(particle, list):
      for piece in particle:
        piece.E = Eext
    else:
      particle.E = Eext
  
# Updates the E-field on the particle and on the sources from the particle
def updateE(*args):
  while len(args) > 1:
    if isinstance(args[0], list):
      for piece in args[0]:
        for source in args[1:]:
          if isinstance(source, list):
            for sourcePiece in source:
              applyEfield(piece, sourcePiece)
          else:
            applyEfield(piece, source)
    else:
      for source in args[1:]:
        if isinstance(source, list):
          for sourcePart in source:
            applyEfield(args[0], sourcePart)
        else:
          applyEfield(args[0], source)
    
    del args[0]

# Applies an E-field on the particle and on the source
def applyEfield(particle, source):
  r = particle.pos - source.pos
  tempEq = k * r / (mag(r))**3
  source.E += -tempEq * particle.q
  particle.E += tempEq * source.q
  
# Updates the positon of the particles
def update(*args):
  for particle in args:
    if isinstance(particle, list):
      for piece in particle:
        piece.p += piece.E * piece.q * deltat
        piece.pos += piece.p / piece.m * deltat
    else:
      particle.p += particle.E * particle.q * deltat
      particle.pos += particle.p / particle.m * deltat
  
# Update E-field variables
def updateEext():
  global Eext, polarizeTot, polarizeAmt, t
  polarizeTot = 0
  polarizeAmt = 0
  t = 0
  if Eslider.value == Eslider.min:
    Eext = vec(0,0,0)
    EextArrow.axis = vec(0,0,0)
    Edisplay.text = "0"
  else:
    Eext=vec(10**(Eslider.value),0,0)
    EextArrow.axis = vec(Eslider.value,0,0) * .18e-10
    Edisplay.text = formatOut(mag(Eext))
  
# Update E-field variables by text input
def updateEinput():
  Eslider.value = log10(Einput.text)
  Einput.text = ""
  updateEext()
  
# Toggle Polarizability
def togglePol():
  global t, polarizeTot, polarizeAmt
  polarizeTot = 0
  polarizeAmt = 0
  if PolCheck.checked:
    t = 0
    TimeCheck.checked = True
  
# Toggle Time
def toggleTime():
  global t
  t=0

# Generate a random unit vector
# Uses an equal-area projection of a sphere onto a rectangle
def randVec():
  theta = 2 * pi * random()
  z = 2 * random() - 1
  semiCircle = sqrt(1-z**2)
  return vec(semiCircle * cos(theta), semiCircle * sin(theta), z)
  
# Format output in scientific notation
def formatOut(input):
  orderMag = floor(log10(abs(input)))
  printIn = input*10**(-orderMag)
  return f"{printIn: 0.3f}e{orderMag}"
