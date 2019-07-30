import queue
import github

from errbot.backends.base import Message
from unittest.mock import MagicMock, create_autospec, PropertyMock
from utils.backends import GitterRoomOccupant

import plugins.labhub
from plugins.labhub import LabHub

from tests.labhub_testcase import LabHubTestCase


class TestLabHub(LabHubTestCase):

    def setUp(self):
        super().setUp((plugins.labhub.LabHub,))
        self.global_mocks = {
            '_teams': self.teams,
        }
        configs = {
            'GH_TOKEN': None,
            'GH_ORG_NAME': 'codemute',
        }
        self.bot.sender._nick = 'batman'
        self.labhub = self.load_plugin('LabHub', self.global_mocks, configs)

    def test_is_room_member(self):
        msg = create_autospec(Message)
        msg.frm.room.occupants = PropertyMock()
        user1 = create_autospec(GitterRoomOccupant)
        user1.username = 'batman'
        user2 = create_autospec(GitterRoomOccupant)
        user2.username = 'superman'
        msg.frm.room.occupants = [user1, user2]
        self.assertTrue(LabHub.is_room_member('batman', msg))

    def test_invite_cmd(self):
        mock_team_contributors = create_autospec(github.Team.Team)
        mock_team_maintainers = create_autospec(github.Team.Team)

        self.teams['contributors'] = mock_team_contributors
        self.teams['maintainers'] = mock_team_maintainers

        mock_dict = {
            'TEAMS': self.teams,
            'is_room_member': MagicMock(),
        }
        self.inject_mocks('LabHub', mock_dict)
        testbot = self

        self.assertEqual(self.labhub.TEAMS, self.teams)

        mock_dict['is_room_member'].return_value = False
        testbot.assertCommand('!invite abhi to contributors',
                              '@abhi is not a member of this room.')

        mock_dict['is_room_member'].return_value = True

        mock_team_maintainers.has_in_members.return_value = False

        # invite me
        testbot.assertCommand('!invite me',
                              'To get started, please follow our [docs]')
        # once invited it should timeout the next time
        with self.assertRaises(queue.Empty):
            testbot.assertCommand('!invite me', 'To get started')

        # invite by maintainer
        mock_team_maintainers.has_in_members.return_value = True

        testbot.assertCommand(
            '!invite abhi to contributors',
            'To get started, please follow our [docs]')
        testbot.assertCommand('!invite abhi to maintainers',
                              '@abhi you seem to be awesome!')

        # invite by contributor
        mock_team_maintainers.has_in_members.return_value = False

        testbot.assertCommand('!invite abhi to maintainers',
                              ':poop:')

        # invite by newcomer
        mock_team_contributors.has_in_members.return_value = False

        testbot.assertCommand('!invite abhi to maintainers',
                              ':poop:')
        testbot.assertCommand('!invite abhi to contributors',
                              'To get started, please follow our [docs]')

        # invalid team
        testbot.assertCommand('!invite abhi to something',
                              'select from one of the valid')

        # invalid command
        testbot.assertCommand('!invite abhito contributors',
                              'Command "invite" / "invite abhito" not found.')

        self.bot.sender._nick = None
        testbot.assertCommand(
            '!invite abhi to contributors',
            'ERROR: The above command cannot be operated without nick.')

    def test_invalid_token(self):
        plugins.labhub.github.Github.return_value = None
        self.labhub.deactivate()
        with self.assertLogs() as cm:
            self.labhub.activate()
        self.assertIn(
            'ERROR:errbot.plugins.LabHub:Cannot create github object,'
            ' check GH_TOKEN',
            cm.output)
