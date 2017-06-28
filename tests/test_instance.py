from atmosphere.main import AtmosphereApp
from atmosphere.instance import InstanceList


def test_instance_list_description():
    app = AtmosphereApp()
    instance_list = InstanceList(app, None)
    assert instance_list.get_description() == 'List instances for user.'
