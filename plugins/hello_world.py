import re
from errbot import BotPlugin
from errbot.templating import tenv


class hello_world(BotPlugin):
    """
    The welcome message for the new users of the community.
    """

    def callback_message(self, msg):
        """
        Invite the user whose message includes the holy 'hello world'
        """
        if re.search(r'hello\s*,?\s*world', msg.body, flags=re.IGNORECASE):
            user = msg.frm.nick
            response = tenv().get_template(
                'hello-world.jinja2.md'
            ).render(
                target=user,
            )
            self.send(msg.frm, response)
