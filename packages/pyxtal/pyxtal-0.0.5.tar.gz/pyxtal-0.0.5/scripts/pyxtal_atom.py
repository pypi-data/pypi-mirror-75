#!/usr/bin/env  python
# encoding: utf-8

import os
from pyxtal import print_logo
from pyxtal.crystal import (
    random_crystal,
    random_crystal_1D,
    random_crystal_2D,
    random_cluster,
)
from pyxtal.symmetry import get_symbol_and_number
from pymatgen.io.cif import CifWriter
from pymatgen.symmetry.analyzer import PointGroupAnalyzer
from time import time
from spglib import get_symmetry_dataset
import numpy as np

from argparse import ArgumentParser

if __name__ == "__main__":
    # -------------------------------- Options -------------------------
    parser = ArgumentParser()
    parser.add_argument(
        "-s",
        "--symmetry",
        dest="sg",
        metavar="sg",
        default=36,
        type=str,
        help="desired symmetry, number or string, e.g., 36, Pbca, Ih",
    )
    parser.add_argument(
        "-e",
        "--element",
        dest="element",
        default="Li",
        help="desired elements: e.g., Li",
        metavar="element",
    )
    parser.add_argument(
        "-n",
        "--numIons",
        dest="numIons",
        default=16,
        help="desired numbers of atoms: 16",
        metavar="numIons",
    )
    parser.add_argument(
        "-f",
        "--factor",
        dest="factor",
        default=1.0,
        type=float,
        help="volume factor: default 1.0",
        metavar="factor",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        dest="verbosity",
        default=0,
        type=int,
        help="verbosity: default 0; higher values print more information",
        metavar="verbosity",
    )
    parser.add_argument(
        "-a",
        "--attempts",
        dest="attempts",
        default=1,
        type=int,
        help="number of crystals to generate: default 1",
        metavar="attempts",
    )
    parser.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        default="out",
        type=str,
        help="Directory for storing output cif files: default 'out'",
        metavar="outdir",
    )
    parser.add_argument(
        "-d",
        "--dimension",
        dest="dimension",
        metavar="dimension",
        default=3,
        type=int,
        help="desired dimension: (3, 2, 1, 0): default 3",
    )
    parser.add_argument(
        "-t",
        "--thickness",
        dest="thickness",
        metavar="thickness",
        default=None,
        type=float,
        help="Thickness, in Angstroms, of a 2D crystal, or area of a 1D crystal, None generates a value automatically: default None",
    )

    print_logo()
    options = parser.parse_args()
    sg = options.sg
    dimension = options.dimension
    if isinstance(sg, str) and sg.isnumeric():
        sg = int(sg)
    symbol, sg = get_symbol_and_number(sg, dimension)

    element = options.element
    number = options.numIons
    numIons = []
    if element.find(",") > 0:
        system = element.split(",")
        for x in number.split(","):
            numIons.append(int(x))
    else:
        system = [element]
        numIons = [int(number)]

    factor = options.factor
    if factor < 0:
        raise ValueError("Volume factor {:.2f} must be greater than 0.".format(factor))

    verbosity = options.verbosity
    attempts = options.attempts
    outdir = options.outdir
    dimension = options.dimension
    thickness = options.thickness

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    for i in range(attempts):
        numIons0 = np.array(numIons)
        start = time()
        if dimension == 3:
            rand_crystal = random_crystal(sg, system, numIons0, factor)
        elif dimension == 2:
            rand_crystal = random_crystal_2D(sg, system, numIons0, thickness, factor)
        elif dimension == 1:
            rand_crystal = random_crystal_1D(sg, system, numIons0, thickness, factor)
        if dimension == 0:
            rand_crystal = random_cluster(sg, system, numIons0, factor)
        end = time()
        timespent = np.around((end - start), decimals=2)

        if rand_crystal.valid:
            # Output a cif or xyz file
            comp = str(rand_crystal.struct.composition)
            comp = comp.replace(" ", "")
            if dimension > 0:
                outpath = outdir + "/" + comp + ".cif"
                CifWriter(rand_crystal.struct, symprec=0.1).write_file(filename=outpath)
            else:
                outpath = outdir + "/" + comp + ".xyz"
                rand_crystal.to_file(filename=outpath, fmt="xyz")

            if dimension > 0:
                ans = get_symmetry_dataset(rand_crystal.spg_struct, symprec=1e-1)[
                    "international"
                ]
            else:
                ans = PointGroupAnalyzer(rand_crystal.molecule).sch_symbol

            print(
                "Symmetry requested: {:d}({:s}), generated: {:s}".format(sg, symbol, ans)
            )
            print("Output to " + outpath)

            if dimension > 0:
                try:
                    from ase import Atoms

                    cell, pos, numbers = rand_crystal.spg_struct
                    ase_struc = Atoms(
                        numbers=numbers, positions=pos, cell=cell, pbc=[1, 1, 1]
                    )
                    xyz_path = outdir + "/" + comp + ".xyz"
                    ase_struc.write(xyz_path, format="extxyz")
                    print("Output to " + xyz_path)
                except:
                    print(
                        "Warning: ASE is required to export the crystal in extxyz format"
                    )

            # Print additional information about the structure
            if verbosity > 0:
                print("Time required for generation: " + str(timespent) + "s")
                print(rand_crystal.struct)

        # If generation fails
        else:
            print("something is wrong")
            print("Time spent during generation attempt: " + str(timespent) + "s")
