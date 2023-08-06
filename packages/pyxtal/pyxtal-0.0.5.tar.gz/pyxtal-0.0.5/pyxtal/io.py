"""
CIF in PyXtal format
"""
import numpy as np

def write_cif(struc, filename, header="", permission='w'):
    l_type = struc.group.lattice_type
    symbol = struc.group.symbol
    number = struc.group.number
    change_set = False
    G1 = struc.group[0].generators
    site1 = struc.mol_sites[0]
    if l_type == 'monoclinic':
        #G1 = struc.group[0].generators
        #G2 = struc.mol_generators[0].wp.generators
        if G1 != site1.wp.generators:
            symbol = symbol.replace('c','n')
            change_set = True

    with open(filename, permission) as f:
        f.write('data_' + header + '\n')
        if hasattr(struc, "energy"):
            f.write('#Energy: {:} eV/cell\n'.format(struc.energy/sum(struc.numMols)))

        f.write("\n_symmetry_space_group_name_H-M '{:s}'\n".format(symbol))
        f.write('_symmetry_Int_Tables_number      {:>15d}\n'.format(number))
        f.write('_symmetry_cell_setting           {:>15s}\n'.format(l_type))

        f.write('_cell_length_a        {:12.6f}\n'.format(struc.lattice.a))
        f.write('_cell_length_b        {:12.6f}\n'.format(struc.lattice.b))
        f.write('_cell_length_c        {:12.6f}\n'.format(struc.lattice.c))
        f.write('_cell_angle_alpha     {:12.6f}\n'.format(np.degrees(struc.lattice.alpha)))
        f.write('_cell_angle_beta      {:12.6f}\n'.format(np.degrees(struc.lattice.beta)))
        f.write('_cell_angle_gamma     {:12.6f}\n'.format(np.degrees(struc.lattice.gamma)))

        f.write('\nloop_\n')
        f.write(' _symmetry_equiv_pos_site_id\n')
        f.write(' _symmetry_equiv_pos_as_xyz\n')
        if not change_set:
            wps = G1
        else:
            wps = site1.wp.generators
        for i, op in enumerate(wps):
            f.write("{:d} '{:s}'\n".format(i+1, op.as_xyz_string()))
        f.write('\nloop_\n')
        f.write(' _atom_site_label\n')
        f.write(' _atom_site_fract_x\n')
        f.write(' _atom_site_fract_y\n')
        f.write(' _atom_site_fract_z\n')
        for site in struc.mol_sites:
            coords, species = site._get_coords_and_species(first=True)
            for specie, coord in zip(species, coords):
                f.write('{:6s}  {:12.6f}{:12.6f}{:12.6f}\n'.format(specie, *coord))
        f.write('#END\n\n')


