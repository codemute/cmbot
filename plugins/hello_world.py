import re
from errbot import BotPlugin
from errbot.templating import tenv


class hello_world(BotPlugin):
    """
    The welcome message for the new users of the community.
    """

    def activate(self):
        super().activate()
        self.hello_world_users = set()

    def callback_message(self, msg):
        """
        Invite the user whose message includes the holy 'hello world'
        """
        if re.search(r'hello\s*,?\s*world', msg.body, flags=re.IGNORECASE):
            user = msg.frm.nick
            if user not in self.hello_world_users:
                response = tenv().get_template(
                    'hello-world.jinja2.md'
                ).render(
                    target=user,
                )
                self.send(msg.frm, response)
                self.hello_world_users.add(user)
                print(self.hello_world_users)
