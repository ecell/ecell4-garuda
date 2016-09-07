from ecell4 import *
#from ecell4.egfrd import EGFRDWorld, EGFRDSimulator
from ecell4.gillespie import GillespieWorld, GillespieSimulator
import pandas as pd

import argparse
import csv

def main(rea, spe, step, runtime):
    m = NetworkModel()
    w = GillespieWorld()
    loglist = []

    with open(spe) as scsv:
        sreader = csv.reader(scsv)
        for row in sreader:
            sp = Species(row[0], row[1], row[2])
            m.add_species_attribute(sp)
            # print(row[3])
            if row[3] != '':
                w.add_molecules(sp, int(row[3]))
            loglist.append(row[0])

    with open(rea) as rcsv:
        rreader = csv.reader(rcsv)
        for row in rreader:
            if row[3] == '':
                a = create_binding_reaction_rule(Species(row[0]), Species(row[1]), Species(row[2]), float(row[4]))
                m.add_reaction_rule(a)

            elif row[1] == '':
                a = create_unbinding_reaction_rule(Species(row[0]), Species(row[2]), Species(row[3]), float(row[4]))
                m.add_reaction_rule(a)

    obs = FixedIntervalNumberObserver(float(step), loglist)
    sim = GillespieSimulator(m, w)
    sim.initialize()
    sim.run(float(runtime), obs)
    #print(obs.data())
    a = pd.DataFrame(obs.data())
    a.to_csv("aaa.csv")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="read model csvs and simulate it")
    parser.add_argument('--reactions',
                        help='reaction csv')
    parser.add_argument('--species',
                        help='species csv')
    parser.add_argument('--stepsize',
                        help='step size')
    parser.add_argument('--runtime',
                        help='run time')

    args = parser.parse_args()
    main(args.reactions, args.species, args.stepsize, args.runtime)
