import pytest
from unittest import mock
import yaml

from deployment import deployment

class TestDeploymentConfig:
    def test_deployment_config_is_read(self):

        with pytest.raises(TypeError) as excinfo:
            with mock.patch('builtins.open', mock.mock_open(read_data='')) as m:
                result = deployment.read_config()
        assert "deployment.yaml" in str(excinfo.value)
        m.assert_called_once_with('deployment.yaml')

    def test_raises_FileNot_found_if_no_deploy_config(self):
        with pytest.raises(FileNotFoundError) as excinfo:
            with mock.patch('builtins.open', mock.mock_open(read_data='')) as m:
                m.side_effect = FileNotFoundError()

                result = deployment.read_config()


    def test_raises_KeyError_if_deployment_config_has_a_missing_key(self):
        data = yaml.dump({"job-id":"b", "experiment-path":"c"})
        with pytest.raises(KeyError) as excinfo:
            with mock.patch('builtins.open', mock.mock_open(read_data=data)) as m:

                result = deployment.read_config()
        assert "is not a valid key" in str(excinfo.value)


    def test_raises_TypeError_if_deployment_config_has_no_keys(self):

        with pytest.raises(TypeError) as excinfo:
            with mock.patch('builtins.open', mock.mock_open(read_data='')) as m:

                result = deployment.read_config()

    def test_deployment_config_is_validated(self):
        pass

