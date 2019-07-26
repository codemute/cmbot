import github
import plugins.labhub

from tests.cmbot_testcase import CmbotTestCase
from unittest.mock import create_autospec, PropertyMock


class LabHubTestCase(CmbotTestCase):

    def setUp(self, klasses=None):
        plugins.labhub.github = create_autospec(github)

        self.mock_org = create_autospec(github.Organization.Organization)
        self.mock_gh = create_autospec(github.Github)
        self.mock_team = create_autospec(github.Team.Team)
        self.mock_team.name = PropertyMock()
        self.mock_team.name = 'mocked team'
        self.teams = {
            'contributors': self.mock_team,
            'maintainers': self.mock_team,
        }

        plugins.labhub.github.Github.return_value = self.mock_gh
        self.mock_gh.get_organization.return_value = self.mock_org
        self.mock_org.get_teams.return_value = [self.mock_team]

        if klasses:
            super().setUp(klasses)
