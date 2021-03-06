from ecell4 import *
from ecell4.gillespie import GillespieWorld, GillespieSimulator
import pandas as pd

import argparse
import csv

class MySpecies:
    def __init__(self, name, d, radius):
        self.name = name
        self.d = d
        self.radius = radius
    def add_mol(self, mol):
        self.mol = mol

class MyReaction:
    def __init__(self, rtype, left, right, rate):
        self.rtype = rtype
        self.left = left
        self.right = right
        self.rate = rate

class MyTime:
    def __init__(self, stepsize, time):
        self.stepsize = stepsize
        self.time = time

class MySim:
    def __init__(self, sim):
        self.sim = sim

def main(csvfile):
    m = NetworkModel()
    w = GillespieWorld()
    loglist = []
    slist = []
    rlist = []

    with open(csvfile) as mcsv:
        r = csv.reader(mcsv)
        for row in r:
            if row[0] == "Species":
                sp = MySpecies(row[1], row[2], row[3])
                slist.append(sp)
                if row[4] != '':
                    sp.add_mol(int(row[4]))
            elif row[0] == "Reaction":
                if row[4] == '':
                    rlist.append(MyReaction("binding", [row[1], row[2]], [row[3]], row[5]))
                elif row[2] == '':
                    rlist.append(MyReaction("unbinding", [row[1]], [row[3], row[4]], row[5]))
            elif row[0] == "Time":
                mytime = MyTime(row[2], row[3])
                mysim = MySim(row[1])
                #obs = FixedIntervalNumberObserver(float(row[2]), loglist)
                # if row[1] == "Gillespie":
                #     sim = GillespieSimulator(m, w)
                #     sim.initialize()
                #     sim.run(float(row[3]), obs)
                #     a = pd.DataFrame(obs.data())
                #     a.to_csv("a.csv")

    for sp in slist:
        tmp = Species(sp.name, sp.d, sp.radius)
        m.add_species_attribute(tmp)
        if hasattr(sp, 'mol'):
            w.add_molecules(tmp, int(sp.mol))
        loglist.append(sp.name)
    
    for r in rlist:
        if r.rtype == "binding":
            m.add_reaction_rule(create_binding_reaction_rule(Species(r.left[0]), Species(r.left[1]), Species(r.right[0]), float(r.rate)))
        elif r.rtype == "unbinding":
            m.add_reaction_rule(create_unbinding_reaction_rule(Species(r.left[0]), Species(r.right[0]), Species(r.right[1]), float(r.rate)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="read model csv and simulate it")
    parser.add_argument('-m',
                        help='model csv')
    args = parser.parse_args()
    main(args.m)
