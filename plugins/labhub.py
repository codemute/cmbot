import github

from errbot import BotPlugin, re_botcmd
from errbot.templating import tenv
from utils.mixin import DefaultConfigMixin


class LabHub(DefaultConfigMixin, BotPlugin):
    """
    All of the GitHub utilities
    """

    CONFIG_TEMPLATE = {
        'GH_ORG_NAME': None,
        'GH_TOKEN': None,
    }

    def activate(self):
        super().activate()
        teams = dict()
        gh_org = None
        try:
            gh = github.Github(self.config['GH_TOKEN'])
            assert gh is not None
        except AssertionError:
            self.log.error('Cannot create github object, check GH_TOKEN')
        else:
            gh_org = gh.get_organization(self.config['GH_ORG_NAME'])
            for team in gh_org.get_teams():
                teams[team.name] = team

        self._gh_org = gh_org
        self._teams = teams
        self._gh = gh

    @property
    def GH_ORG_NAME(self):
        return self.config['GH_ORG_NAME']

    @property
    def TEAMS(self):
        return self._teams

    @TEAMS.setter
    def TEAMS(self, new):
        self._teams = new

    def team_mapping(self):
        return {
            'contributors': self.TEAMS['contributors'],
            'maintainers': self.TEAMS['maintainers'],
        }

    def is_team_member(self, user, team):
        teams = self.team_mapping()
        return teams[team].has_in_members(self._gh.get_user(user))

    @staticmethod
    def is_room_member(invitee, msg):
        members = [mem.username for mem in msg.frm.room.occupants]
        return invitee in members

    # Ignore LineLengthBear, PycodestyleBear
    @re_botcmd(pattern=r'^(?:(?:welcome)|(?:inv)|(?:invite))\s+@?([\w-]+)(?:\s+(?:to)\s+(\w+))?$',
               re_cmd_name_help='invite ([@]<username> [to <team>]|me)')
    def invite_cmd(self, msg, match):
        """
        Invite given user to given team. By default it invites to
        "contributors" team.
        """
        invitee = match.group(1)
        inviter = msg.frm.nick
        if not inviter:
            yield 'ERROR: The above command cannot be operated without nick.'
            return

        team = 'contributors' if match.group(2) is None else match.group(2)
        team = team.lower()

        is_maintainer = self.is_team_member(inviter, 'maintainers')

        self.log.info('{} invited {} to {}'.format(inviter, invitee, team))

        valid_teams = self.team_mapping()
        if team not in valid_teams:
            yield 'Please select from one of the valid teams: ' + ', '.join(
                   valid_teams)
            return

        def invite(invitee, team):
            self.team_mapping()[team].add_membership(self._gh.get_user(invitee))

        if not self.is_room_member(invitee, msg):
            yield '@{} is not a member of this room.'.format(invitee)
            return

        if is_maintainer:
            invite(invitee, team)
            yield tenv().get_template(
                '{}.jinja2.md'.format(team)
            ).render(
                target=invitee,
            )
        elif team == 'contributors':
            invite(invitee, team)
            yield tenv().get_template(
                '{}.jinja2.md'.format(team)
            ).render(
                target=invitee,
            )
        else:
            yield tenv().get_template(
                'not-eligible-invite.jinja2.md'
            ).render(
                action='invite someone to maintainers',
                designation='maintainer',
                target=inviter,
            )
