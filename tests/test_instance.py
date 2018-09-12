import json
import responses
from .mock_server import get_free_port, start_mock_server
from atmosphere.api import AtmosphereAPI
from atmosphere.main import AtmosphereApp
from atmosphere.instance import InstanceList


class TestInstances(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        cls.mock_users_base_url = 'http://localhost:{port}'.format(port=cls.mock_server_port)
        cls.mock_users_bad_base_url = 'http://localhosty:{port}'.format(port=cls.mock_server_port)
        start_mock_server(cls.mock_server_port)

    def test_instance_list_description(self):
        app = AtmosphereApp()
        instance_list = InstanceList(app, None)
        assert instance_list.get_description() == 'List instances for user.'

    def test_getting_instances_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_instances()
        assert not response.ok

    def test_getting_instances_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_instances()
        assert response.ok
        assert response.message['count'] == 1 and response.message['results'][0]['name'] == 'BioLinux 8'

    def test_getting_instance_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_instance(1)
        assert not response.ok

    def test_getting_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_instance(1)
        assert response.ok
        assert response.message['id'] == 21752 and response.message['name'] == 'BioLinux 8'

    def test_getting_instance_actions_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_instance_actions(1)
        assert not response.ok

    def test_getting_instance_actions_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_instance_actions(1)
        assert response.ok
        assert response.message[4]['key'] == 'Reboot' and response.message[4]['description'] == 'Reboots an instance when it is in ANY State'

    def test_creating_instance_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        payload = {
            "identity": "a5a6140d-1122-4581-87dc-bd9704fa07ec",
            "name": "myfirstinstance",
            "project": "7c8d34b1-1b2d-4f7f-bd62-4e0929295fd4",
            "size_alias": "100",
            "source_alias": "ec4fb434-a7b7-4c57-b882-0a1bf34506df",
            "scripts": [],
            "deploy": True,
            "extra": {}
        }
        response = api.create_instance(json.dumps(payload))
        assert not response.ok
        assert response.message['errors'][0]['code'] == 400
        assert response.message['errors'][0]['message']['allocation_source_id'] == 'This field is required.'

    def test_creating_instance_when_size_is_invalid(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        payload = {
            "identity": "a5a6140d-1122-4581-87dc-bd9704fa07ec",
            "name": "myfirstinstance",
            "project": "7c8d34b1-1b2d-4f7f-bd62-4e0929295fd4",
            "size_alias": "-1",
            "source_alias": "ec4fb434-a7b7-4c57-b882-0a1bf34506df",
            "allocation_source_id": "f4cca788-e039-4f82-bc77-9fb92141eca6",
            "scripts": [],
            "deploy": True,
            "extra": {}
        }
        response = api.create_instance(json.dumps(payload))
        assert not response.ok
        assert response.message['errors'][0]['code'] == 413
        assert response.message['errors'][0]['message'] == 'Size Not Available. Disk is 8 but image requires at least 20'

    def test_creating_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        payload = {
            "identity": "a5a6140d-1122-4581-87dc-bd9704fa07ec",
            "name": "myfirstinstance",
            "project": "7c8d34b1-1b2d-4f7f-bd62-4e0929295fd4",
            "size_alias": "100",
            "source_alias": "ec4fb434-a7b7-4c57-b882-0a1bf34506df",
            "allocation_source_id": "f4cca788-e039-4f82-bc77-9fb92141eca6",
            "scripts": [],
            "deploy": True,
            "extra": {}
        }
        response = api.create_instance(json.dumps(payload))
        assert response.ok
        assert response.message['id'] == 1 and response.message['name'] == 'myfirstinstance'

    def test_suspending_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.do_instance_action('suspend', 1)
        assert response.ok
        assert response.message['result'] == 'success' and response.message['message'] == 'The requested action <suspend> was run successfully'

    @responses.activate
    def test_suspending_instance_when_response_is_not_ok(self):
        responses.add(responses.GET,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=200,
                      json=[{"description": "Suspends an instance when it is in the 'active' State", "key": "Suspend"}])
        responses.add(responses.POST,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=409,
                      json={"errors": [{"code": 409, "message": "409 Conflict Cannot 'suspend' instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 while it is in vm_state suspended"}]})
        api = AtmosphereAPI('token')
        response = api.do_instance_action('suspend', 'ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822')
        assert not response.ok
        assert response.message['errors'][0]['message'] == "409 Conflict Cannot 'suspend' instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 while it is in vm_state suspended"

    def test_resuming_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.do_instance_action('resume', 1)
        assert response.ok
        assert response.message['result'] == 'success' and response.message['message'] == 'The requested action <resume> was run successfully'

    @responses.activate
    def test_resuming_instance_when_response_is_not_ok(self):
        responses.add(responses.GET,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=200,
                      json=[{"description": "Resumes an instance when it is not in the 'active' State", "key": "Resume"}])
        responses.add(responses.POST,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=409,
                      json={"errors": [{"code": 409, "message": "409 Conflict Cannot 'resume' instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 while it is in vm_state active"}]})
        api = AtmosphereAPI('token')
        response = api.do_instance_action('resume', 'ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822')
        assert not response.ok
        assert response.message['errors'][0]['message'] == "409 Conflict Cannot 'resume' instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 while it is in vm_state active"

    def test_starting_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.do_instance_action('start', 1)
        assert response.ok
        assert response.message['result'] == 'success' and response.message['message'] == 'The requested action <start> was run successfully'

    @responses.activate
    def test_starting_instance_when_response_is_not_ok(self):
        responses.add(responses.GET,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=200,
                      json=[{"description": "Starts an instance when it is not in the 'active' State", "key": "Start"}])
        responses.add(responses.POST,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=409,
                      json={"errors": [{"code": 409, "message": "409 Conflict Cannot 'start' instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 while it is in vm_state active"}]})
        api = AtmosphereAPI('token')
        response = api.do_instance_action('start', 'ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822')
        assert not response.ok
        assert response.message['errors'][0]['message'] == "409 Conflict Cannot 'start' instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 while it is in vm_state active"

    def test_stopping_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.do_instance_action('stop', 1)
        assert response.ok
        assert response.message['result'] == 'success' and response.message['message'] == 'The requested action <stop> was run successfully'

    @responses.activate
    def test_stopping_instance_when_response_is_not_ok(self):
        responses.add(responses.GET,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=200,
                      json=[{"description": "Stops an instance when it is in the 'active' State", "key": "Stop"}])
        responses.add(responses.POST,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=409,
                      json={"errors": [{"code": 409, "message": "409 Conflict Cannot 'stop' instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 while it is in vm_state stopped"}]})
        api = AtmosphereAPI('token')
        response = api.do_instance_action('stop', 'ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822')
        assert not response.ok
        assert response.message['errors'][0]['message'] == "409 Conflict Cannot 'stop' instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 while it is in vm_state stopped"

    def test_rebooting_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.do_instance_action('reboot', 1)
        assert response.ok
        assert response.message['result'] == 'success' and response.message['message'] == 'The requested action <reboot> was run successfully'

    @responses.activate
    def test_rebooting_instance_when_response_is_not_ok(self):
        responses.add(responses.GET,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=200,
                      json=[{"description": "Reboots an instance when it is in ANY State", "key": "Reboot"}])
        responses.add(responses.POST,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=403,
                      json={"errors": [{"code": 403, "message": "The requested action reboot encountered an irrecoverable exception: message"}]})
        api = AtmosphereAPI('token')
        response = api.do_instance_action('reboot', 'ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822')
        assert not response.ok
        assert response.message['errors'][0]['message'] == "The requested action reboot encountered an irrecoverable exception: message"

    def test_redeploying_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.do_instance_action('redeploy', 1)
        assert response.ok
        assert response.message['result'] == 'success' and response.message['message'] == 'The requested action <redeploy> was run successfully'

    @responses.activate
    def test_redeploying_instance_when_response_is_not_ok(self):
        responses.add(responses.GET,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=200,
                      json=[{"description": "Redeploy to an instance when it is in ANY active state", "key": "Redeploy"}])
        responses.add(responses.POST,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=403,
                      json={"errors": [{"code": 403, "message": "The requested action reboot encountered an irrecoverable exception: message"}]})
        api = AtmosphereAPI('token')
        response = api.do_instance_action('redeploy', 'ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822')
        assert not response.ok
        assert response.message['errors'][0]['message'] == "The requested action reboot encountered an irrecoverable exception: message"

    def test_shelving_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.do_instance_action('shelve', 1)
        assert response.ok
        assert response.message['result'] == 'success' and response.message['message'] == 'The requested action <shelve> was run successfully'

    @responses.activate
    def test_shelving_instance_when_response_is_not_ok(self):
        responses.add(responses.GET,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=200,
                      json=[{"description": "Shelves an instance when it is in the 'active' State", "key": "Shelve"}])
        responses.add(responses.POST,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=403,
                      json={"errors": [{"code": 403, "message": "The requested action reboot encountered an irrecoverable exception: message"}]})
        api = AtmosphereAPI('token')
        response = api.do_instance_action('shelve', 'ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822')
        assert not response.ok
        assert response.message['errors'][0]['message'] == "The requested action reboot encountered an irrecoverable exception: message"

    def test_unshelving_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.do_instance_action('unshelve', 1)
        assert response.ok
        assert response.message['result'] == 'success' and response.message['message'] == 'The requested action <unshelve> was run successfully'

    @responses.activate
    def test_unshelving_instance_when_response_is_not_ok(self):
        responses.add(responses.GET,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=200,
                      json=[{"description": "Unshelves an instance when it is in the 'shelved' State", "key": "Unshelve"}])
        responses.add(responses.POST,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=409,
                      json={"errors": [{"code": 409, "message": "409 Conflict Cannot 'unshelve' instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 while it is in vm_state stopped"}]})
        api = AtmosphereAPI('token')
        response = api.do_instance_action('unshelve', 'ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822')
        assert not response.ok
        assert response.message['errors'][0]['message'] == "409 Conflict Cannot 'unshelve' instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 while it is in vm_state stopped"

    def test_attaching_volume_to_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        options = {'volume_id': 'b94a0146-10d3-4c91-8482-3c9758c81ddf'}
        response = api.do_instance_volume_action('attach_volume', 'ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822', options=options)
        assert response.ok
        assert response.message['result'] == 'success' and response.message['message'] == 'The requested action <attach_volume> was run successfully'

    @responses.activate
    def test_attaching_volume_to_instance_when_response_is_not_ok(self):
        responses.add(responses.POST,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=403,
                      json={"errors": [{"code": 403, "message": "Instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 must be active before attaching a volume. (Current: shutoff) Retry request when instance is active."}]})
        api = AtmosphereAPI('token')
        options = {'volume_id': 'b94a0146-10d3-4c91-8482-3c9758c81ddf'}
        response = api.do_instance_volume_action('attach_volume', 'ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822', options=options)
        assert not response.ok
        assert response.message['errors'][0]['message'] == "Instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 must be active before attaching a volume. (Current: shutoff) Retry request when instance is active."

    def test_detaching_volume_to_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        options = {'volume_id': 'b94a0146-10d3-4c91-8482-3c9758c81ddf'}
        response = api.do_instance_volume_action('detach_volume', 'ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822', options=options)
        assert response.ok
        assert response.message['result'] == 'success' and response.message['message'] == 'The requested action <detach_volume> was run successfully'

    @responses.activate
    def test_detaching_volume_to_instance_when_response_is_not_ok(self):
        responses.add(responses.POST,
                      'https://local.atmo.cloud/api/v2/instances/ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822/actions',
                      status=403,
                      json={"errors": [{"code": 403, "message": "Instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 must be active, suspended, or stopped before detaching a volume. (Current: shelved_offloaded) Retry request when instance is active."}]})
        api = AtmosphereAPI('token')
        options = {'volume_id': 'b94a0146-10d3-4c91-8482-3c9758c81ddf'}
        response = api.do_instance_volume_action('detach_volume', 'ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822', options=options)
        assert not response.ok
        assert response.message['errors'][0]['message'] == "Instance ecdcdd9e-cf0e-42c4-9a7c-a950c6d8b822 must be active, suspended, or stopped before detaching a volume. (Current: shelved_offloaded) Retry request when instance is active."

    def test_getting_instance_history_when_response_is_not_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_bad_base_url)
        response = api.get_instance_history('eb95b7e9-9c56-479b-9d81-b93292a9078a')
        assert not response.ok

    def test_getting_instance_history_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.get_instance_history('eb95b7e9-9c56-479b-9d81-b93292a9078a')
        assert response.ok
        assert response.message['count'] == 23 and response.message['results'][0]['status'] == 'build'

    def test_deleting_instance_when_response_is_ok(self):
        api = AtmosphereAPI('token', base_url=self.mock_users_base_url)
        response = api.delete_instance(1)
        assert response.ok
