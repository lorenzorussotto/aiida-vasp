"""Custom INCAR tags declared in `settings['unsupported_parameters']` are accepted by `VaspWorkChain`."""

from aiida import orm
from aiida.plugins import WorkflowFactory

from aiida_vasp.common import validate_incar_tags


def test_validate_incar_tags(aiida_profile):
    """Undeclared custom tags and typos are rejected; declared custom tags are accepted."""
    parameters = orm.Dict({'incar': {'encut': 500, 'lmytag': True}})

    assert 'lmytag' in validate_incar_tags({'parameters': parameters}, {})

    settings = orm.Dict({'unsupported_parameters': {'lmytag': 'my custom tag'}})
    assert validate_incar_tags({'parameters': parameters, 'settings': settings}, {}) is None

    # the workchain's own default declaration is used when settings declare nothing
    assert validate_incar_tags({'parameters': parameters}, {'lmytag': 'default tag'}) is None

    typo = orm.Dict({'incar': {'encutt': 500, 'lmytag': True}})
    assert 'encutt' in validate_incar_tags({'parameters': typo, 'settings': settings}, {})

    skip = orm.Dict({'skip_parameters_validation': True})
    assert validate_incar_tags({'parameters': parameters, 'settings': skip}, {}) is None


def test_parameters_port_accepts_custom_tags(aiida_profile):
    """Assigning parameters with a custom tag to the builder no longer fails before `settings` is known."""
    builder = WorkflowFactory('vasp.v2.vasp').get_builder()
    builder.parameters = orm.Dict({'incar': {'encut': 500, 'lmytag': True}})
    assert builder.parameters['incar']['lmytag'] is True
