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
    def __init__(self, type, left, right, rate):
        self.type = type
        self.left = left
        self.right = right
        self.rate = rate

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
                #m.add_species_attribute(sp)
                if row[4] != '':
                    sp.add_mol(int(row[4]))
                    #w.add_molecules(sp, int(row[4]))
                loglist.append(row[1])
            elif row[0] == "Reaction":
                if row[4] == '':
                    rlist.append(MyReaction("binding", [row[1], row[2]], [row[3]], row[5]))
                    # a = create_binding_reaction_rule(Species(row[1]), Species(row[2]), Species(row[3]), float(row[5]))
                    # m.add_reaction_rule(a)
                elif row[2] == '':
                    rlist.append(MyReaction("unbinding", [row[1]], [row[3], row[4]], row[5]))
                    # a = create_unbinding_reaction_rule(Species(row[1]), Species(row[3]), Species(row[4]), float(row[5]))
                    # m.add_reaction_rule(a)
            # elif row[0] == "Time":
            #     obs = FixedIntervalNumberObserver(float(row[2]), loglist)
            #     if row[1] == "Gillespie":
            #         sim = GillespieSimulator(m, w)
            #         sim.initialize()
            #         sim.run(float(row[3]), obs)
            #         a = pd.DataFrame(obs.data())
            #         a.to_csv("a.csv")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="read model csv and simulate it")
    parser.add_argument('-m',
                        help='model csv')
    args = parser.parse_args()
    main(args.m)
