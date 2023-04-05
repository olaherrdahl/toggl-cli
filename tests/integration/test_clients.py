import pytest

from toggl.api import Client
from toggl import exceptions


class TestClients:

    def test_add(self, cmd, fake):
        name = fake.name()
        result = cmd('clients add --name \'{}\''.format(name))
        assert result.obj.exit_code == 0

        # Duplicated names not allowed
        with pytest.raises(exceptions.TogglApiException):
            cmd('clients add --name \'{}\''.format(name))

        result = cmd('clients add --name \'{}\''.format(fake.name(), fake.sentence()))
        assert result.obj.exit_code == 0

    def test_ls(self, cmd):
        result = cmd('clients ls')
        parsed = result.parse_list()

#E       AssertionError: assert 3 == 2
#E        +  where 3 = len([['Name', 'Id'], ['Joseph Wolfe', '63086176'], ['Pamela Olson', '63086178']])

        assert len(parsed) == 2

    def test_get(self, cmd, fake):
        name = fake.name()
        result = cmd('clients add --name \'{}\''.format(name))
        assert result.obj.exit_code == 0

        result = cmd('clients get \'{}\''.format(result.created_id()))
        id_parsed = result.parse_detail()

        assert id_parsed['name'] == name

        result = cmd('clients get \'{}\''.format(name))
        name_parsed = result.parse_detail()

        assert name_parsed['id'] == id_parsed['id']
        assert name_parsed['name'] == name

    def test_update(self, cmd, fake, config):
        name = fake.name()
        result = cmd('clients add --name \'{}\''.format(name))
        assert result.obj.exit_code == 0
        created_id = result.created_id()

        assert Client.objects.get(created_id, config=config).name == name

        new_name = fake.name()
        result = cmd('clients update --name \'{}\' \'{}\''.format(new_name, name))
        assert result.obj.exit_code == 0

        client_obj = Client.objects.get(created_id, config=config)
        assert client_obj.name == new_name

    def test_delete(self, cmd, fake):
        result = cmd('clients add --name \'{}\''.format(fake.name()))
        assert result.obj.exit_code == 0
        created_id = result.created_id()

        result = cmd('clients rm --yes \'{}\''.format(created_id))
        assert result.obj.exit_code == 0

        result = cmd('clients rm  --yes \'{}\''.format(created_id))
        assert result.obj.exit_code == 44

        name = fake.name()
        result = cmd('clients add --name \'{}\''.format(name))
        assert result.obj.exit_code == 0

        result = cmd('clients rm --yes  \'{}\''.format(name))
        assert result.obj.exit_code == 0
