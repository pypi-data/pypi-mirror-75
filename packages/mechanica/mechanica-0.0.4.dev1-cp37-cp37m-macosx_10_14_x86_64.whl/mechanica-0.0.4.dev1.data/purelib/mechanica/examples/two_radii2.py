import mechanica as m
import numpy as np

# potential cutoff distance
cutoff = 1

# dimensions of universe
dim=[10., 10., 10.]

# new simulator, don't load any example
m.Simulator(example="", dim=dim)

# create a particle type
# all new Particle derived types are automatically
# registered with the universe
class Big(m.Particle):
    mass = 100000            # make it heavy, so it doesn't move
    radius = 3               # large radius

class Small(m.Particle):
    mass = 10.
    radius = 0.3             # small particles

# create a soft sphere interation potential that goes between the
# large and small particle
# kappa is a measure of how compressible the particle is, i.e. how soft is it.
# epsilon is the depth of the attractive potential, i.e. how sticky it is.
pot = m.Potential.soft_sphere(kappa=10, epsilon=5)

# stick the large and small particles together with the potential
m.Universe.bind(pot, Big, Small)

# make the small particles stick to each other
m.Universe.bind(pot, Small, Small)

# make the random force act on the small particles
m.Universe.bind(Forces.random(), Small)

size = 10000

# create a single big particle in the middle of the domain
Big(pos=[5, 5, 5])

# make a 100 small particles in random locations, these should
# migrate to the srface of the large particle.
for i in range(100):
    Small()

# run the simulator interactive
m.Simulator.run()
