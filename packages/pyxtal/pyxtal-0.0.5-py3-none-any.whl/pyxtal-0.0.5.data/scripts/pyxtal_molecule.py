#!python
# encoding: utf-8

import os
from time import time
from spglib import get_symmetry_dataset
from pyxtal.molecular_crystal import molecular_crystal, molecular_crystal_2D
from pyxtal.symmetry import get_symbol_and_number
from pymatgen.io.cif import CifWriter
import numpy as np
from pyxtal import print_logo

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
        help="desired symmetry, number or string, e.g., 36, Pbca",
    )
    parser.add_argument(
        "-e",
        "--molecule",
        dest="molecule",
        default="H2O",
        help="desired molecules: e.g., H2O",
        metavar="molecule",
    )
    parser.add_argument(
        "-n",
        "--numMols",
        dest="numMols",
        default=4,
        help="desired numbers of molecules: 4",
        metavar="numMols",
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
        help="Directory for storing output cif/xyz files: default 'out'",
        metavar="outdir",
    )
    parser.add_argument(
        "-c",
        "--checkatoms",
        dest="checkatoms",
        default="True",
        type=str,
        help="Whether to check inter-atomic distances at each step: default True",
        metavar="outdir",
    )
    parser.add_argument(
        "-i",
        "--allowinversion",
        dest="allowinversion",
        default="False",
        type=str,
        help="Whether to allow inversion of chiral molecules: default False",
        metavar="outdir",
    )
    parser.add_argument(
        "-d",
        "--dimension",
        dest="dimension",
        metavar="dimension",
        default=3,
        type=int,
        help="desired dimension: (3 or 2 for 3d or 2d, respectively): default 3",
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

    molecule = options.molecule
    number = options.numMols
    verbosity = options.verbosity
    attempts = options.attempts
    outdir = options.outdir
    factor = options.factor
    thickness = options.thickness

    if options.checkatoms == "True" or options.checkatoms == "False":
        checkatoms = eval(options.checkatoms)
    else:
        print("Invalid value for -c (--checkatoms): must be 'True' or 'False'.")
        checkatoms = True

    if options.allowinversion == "True" or options.allowinversion == "False":
        allowinversion = eval(options.allowinversion)
    else:
        print("Invalid value for -i (--allowinversion): must be 'True' or 'False'.")
        allowinversion = False

    numMols = []
    if molecule.find(",") > 0:
        strings = molecule.split(",")
        system = []
        for mol in strings:
            system.append(mol)
        for x in number.split(","):
            numMols.append(int(x))
    else:
        system = [molecule]
        numMols = [int(number)]
    orientations = None

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    for i in range(attempts):
        start = time()
        numMols0 = np.array(numMols)
        if dimension == 3:
            rand_crystal = molecular_crystal(
                sg,
                system,
                numMols0,
                factor,
                check_atomic_distances=checkatoms,
                allow_inversion=allowinversion,
            )
        elif dimension == 2:
            rand_crystal = molecular_crystal_2D(
                sg,
                system,
                numMols0,
                thickness,
                factor,
                allow_inversion=allowinversion,
                check_atomic_distances=checkatoms,
            )
        end = time()
        timespent = np.around((end - start), decimals=2)
        if rand_crystal.valid:
            comp = str(rand_crystal.struct.composition)
            comp = comp.replace(" ", "")
            cifpath = outdir + "/" + comp + ".cif"
            CifWriter(rand_crystal.struct, symprec=0.1).write_file(filename=cifpath)
            ans = get_symmetry_dataset(rand_crystal.spg_struct, symprec=1e-1)[
                "international"
            ]
            print(
                "Symmetry requested: {:d} ({:s}), generated: {:s}, vol: {:.2f} A^3".format(
                    sg, symbol, ans, rand_crystal.volume
                )
            )
            print("Output to " + cifpath)
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
                print("Warning: ASE is required to export the crystal in extxyz format")

            # Print additional information about the structure
            if verbosity > 0:
                print("Time required for generation: " + str(timespent) + "s")
                print("Molecular Wyckoff positions:")
                for ms in rand_crystal.mol_generators:
                    print(
                        str(ms.mol.composition)
                        + ": "
                        + str(ms.multiplicity)
                        + str(ms.letter)
                        + " "
                        + str(ms.position)
                    )
            if verbosity > 1:
                print(rand_crystal.struct)

        # If generation fails
        else:
            print("something is wrong")
            print("Time spent during generation attempt: " + str(timespent) + "s")

