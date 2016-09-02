from ecell4 import *
#from ecell4.egfrd import EGFRDWorld, EGFRDSimulator
from ecell4.gillespie import GillespieWorld, GillespieSimulator
import pandas as pd

#w = EGFRDWorld()
w = GillespieWorld()

sp1 = Species("A")
sp2 = Species("B")
sp3 = Species("C")

sp1.set_attribute("radius", "0.005")
sp2.set_attribute("radius", "0.005")
sp3.set_attribute("radius", "0.005")

sp1.set_attribute("D", "1")
sp2.set_attribute("D", "1")
sp3.set_attribute("D", "1")

# rr1 = ReactionRule()
# rr1.add_reactant(sp1)
# rr1.add_reactant(sp2)
# rr1.add_product(sp3)
# rr1.set_k(0.01)

# rr2 = ReactionRule()
# rr2.add_reactant(sp3)
# rr2.add_product(sp1)
# rr2.add_product(sp2)
# rr2.set_k(0.3)

m = NetworkModel()
# m.add_reaction_rules([rr1, rr2])
m.add_reaction_rule(create_binding_reaction_rule(sp1, sp2, sp3, 0.01))
m.add_reaction_rule(create_unbinding_reaction_rule(sp3, sp1, sp2, 0.3))

w.add_molecules(sp3, 60)

obs = FixedIntervalNumberObserver(0.01, ["A", "B", "C"])

#sim = EGFRDSimulator(m, w)
sim = GillespieSimulator(m, w)
sim.initialize()
sim.run(10.0, obs)
print(obs.data())
a = pd.DataFrame(obs.data())
a.to_csv("aaa.csv")
#sim.step(0.001)
 
