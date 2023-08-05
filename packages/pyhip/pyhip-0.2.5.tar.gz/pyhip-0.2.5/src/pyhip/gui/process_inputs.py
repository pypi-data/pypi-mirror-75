"""Module for the first tab."""
from nob import Nob
import os
from glob import glob
import h5py
from opentea.process_utils import process_tab
from opentea.noob.noob import unique_dict_key
from pyhip.gui.parser_utils import (
    get_patch_list_AVBP,
    parse_meshinfo,
    parse_versioninfo,
    parse_boundaries,
    parse_periodicities,
    )
from pyhip.commands.readers import read_mesh_files
from pyhip.commands.writers import (
    write_hdf5,
    dump_wired,
    )
from pyhip.commands.operations import (
    list_periodic,
    list_surface,
    generate_mesh_2d_3d,
    set_bctype,
    set_checklevel,
    hip_exit,
    )

def process_mesh(nob_in):
    """
    *Update mesh infos and show them in the IHM like this :*

    :param nob_in: A dict( ) with IHM's parameters

    :returns: A dict( ) with some update infos:

                - *patches_list*
    """
    nob_out = Nob(nob_in.copy())

    fallback = nob_out.fallback[:]
    if nob_out.checklvl[:]:
        set_checklevel(5, fallback=fallback)
    else:
        set_checklevel(0, fallback=fallback)

    if unique_dict_key(nob_out.input_mode[:]) == 'generate':
        val = lambda n, v: n[n.find(v)[0]][:] if n.find(v) else None
        if nob_out.generate.structure[:] == 'quad':
            convert2tri = False
        else:
            convert2tri = True
        generate_mesh_2d_3d(
            nob_out.lower_corner[:],
            nob_out.upper_corner[:],
            nob_out.resolution[:],
            convert2tri=convert2tri,
            extru_axis=val(nob_out, 'extru_axis'),
            extru_range=(val(nob_out, 'extru_min'), val(nob_out, 'extru_max')),
            extru_res=val(nob_out, 'extru_resolution'),
            fallback=fallback)

    elif unique_dict_key(nob_out.input_mode[:]) == 'read':
        input_case = unique_dict_key(nob_out.input_case[:])
        case_fmt = input_case.split('_')[0]

        # Reading of the mesh
        mesh_file = nob_out.read.meshfile[:]
        _ = read_mesh_files([mesh_file], case_fmt, fallback=fallback)

        # Listing of periodicities
        _ = list_periodic(fallback=fallback)

    _ = list_surface(fallback=fallback)

    root = 'tmp'
    # Writing of the mesh in hdf5 format
    _ = write_hdf5(root, fallback=fallback)

    # Récupération du filaire -> moteur 3D
    geo = 'geo_tmp'
    _ = dump_wired(geo, fallback=fallback)
    nob_out.inputs.geofile.set("./" + geo + ".geo")

    # Exit/Execute hip
    log, _ = hip_exit(fallback=fallback)

    # Setting of patch list
    if fallback:
        patch_dict = parse_boundaries(log)
        patch_list = list(patch_dict.keys())
    else:
        patch_list = get_patch_list_AVBP(root + ".mesh.h5")
    nob_out.input_mode.patch_list.set(patch_list)

    # Setting of version and mesh info
    if fallback:
        version_info = parse_versioninfo(log)
        mesh_info = parse_meshinfo(log)
        nob_out.inputs.meshinfo.set(version_info + mesh_info)
    else:
        nob_out.inputs.meshinfo.set("Mesh info parsing cython not implemented yet.")

    # Setting of existed periodicity
    if fallback:
        perio_list = parse_periodicities(log)
        nob_out.periodicity.bnd_patch.set(perio_list)
    else:
        print('Periodicities parsing cython not implemented yet')

    for root_file in glob(root + '*'):
        os.remove(root_file)

    return nob_out[:]

if __name__ == "__main__":
    process_tab(process_mesh)

