"""
Implementation of the reader for XYZ files using OpenBabel
"""

import seamm
import seamm_util
from read_structure_step.errors import XYZError
from read_structure_step.formats.registries import register_reader
from ..which import which

obabel_error_identifiers = ['0 molecules converted']


@register_reader('.xyz')
def load_xyz(file_name):

    obabel_exe = which('obabel')
    local = seamm.ExecLocal()

    result = local.run(
        cmd=[obabel_exe, '-f 1', '-l 1', '-ixyz', file_name, '-omol', '-x3']
    )
    for each_error in obabel_error_identifiers:
        if each_error in result['stderr']:
            raise XYZError('OpenBabel: Could not read input file. %s' % result)

    mol = result['stdout']

    structure = seamm_util.molfile.to_seamm(mol)

    return structure
