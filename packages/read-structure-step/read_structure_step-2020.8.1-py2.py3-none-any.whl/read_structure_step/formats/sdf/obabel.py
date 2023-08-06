"""
Implementation of the reader for SDF files using OpenBabel
"""

import seamm
import seamm_util
from read_structure_step.errors import SDFError
from read_structure_step.formats.registries import register_reader
from ..which import which

obabel_error_identifiers = ['0 molecules converted']


@register_reader('.sdf')
def load_sdf(file_name):
    obabel_exe = which('obabel')
    local = seamm.ExecLocal()

    result = local.run(
        cmd=[obabel_exe, '-f 1', '-l 1', '-isdf', file_name, '-omol', '-x3']
    )
    for each_error in obabel_error_identifiers:
        if each_error in result['stderr']:
            raise SDFError('OpenBabel: Could not read input file. %s' % result)

    mol = result['stdout']

    structure = seamm_util.molfile.to_seamm(mol)

    return structure
