import logging
import os

BOT_ROOT = os.environ.get('BOT_ROOT', os.getcwd())

_BOT_IDENTITY_KEYS = (
    'endpoint',
    'nickname',
    'password',
    'port',
    'server',
    'ssl',
    'token',
    'username',
)

BOT_IDENTITY = {}

for _key in _BOT_IDENTITY_KEYS:
    if os.environ.get('BOT_' + _key.upper()):
        BOT_IDENTITY[_key] = os.environ.get('BOT_' + _key.upper())

if 'server' in BOT_IDENTITY and ':' in BOT_IDENTITY['server']:
    server, port = os.environ['BOT_SERVER'].split(':')
    BOT_IDENTITY['server'] = (server, int(port))

BACKEND = os.environ.get('BACKEND')
if not BACKEND:
    if BOT_IDENTITY['token']:
        BACKEND = 'Gitter'
    else:
        BACKEND = 'Text'

if BACKEND == 'Gitter':
    BOT_EXTRA_BACKEND_DIR = os.path.join(BOT_ROOT, 'err-backend-gitter')
else:
    BOT_EXTRA_BACKEND_DIR = None

if BOT_EXTRA_BACKEND_DIR:
    plug_file = BACKEND.lower() + '.plug'
    if not os.path.exists(os.path.join(BOT_EXTRA_BACKEND_DIR, plug_file)):
        raise SystemExit('Directory %s not initialised' %
                         BOT_EXTRA_BACKEND_DIR)

HIDE_RESTRICTED_COMMANDS = True

BOT_DATA_DIR = os.path.join(BOT_ROOT, 'data')
if not os.path.isdir(BOT_DATA_DIR):
    # create an empty data directory
    os.mkdir(BOT_DATA_DIR)

BOT_EXTRA_PLUGIN_DIR = BOT_ROOT

BOT_LOG_FILE = os.path.join(BOT_ROOT, 'errbot.log')
BOT_LOG_LEVEL = logging.DEBUG

if not os.environ.get('BOT_PREFIX'):
    raise SystemExit("Environment variable BOT_PREFIX not specified")

BOT_PREFIX = os.environ.get('BOT_PREFIX')

BOT_ADMINS = os.environ.get('BOT_ADMINS', '').split() or ('*@localhost', )
# Text is a special case
if BACKEND == 'Text':
    BOT_ADMINS = ('@localhost', )

DIVERT_TO_PRIVATE = ('help', )

ROOMS_TO_JOIN = ['community', 'cmbot']

if BACKEND == 'Gitter':
    ROOMS_TO_JOIN = ['codemute/' + item for item in ROOMS_TO_JOIN]

CHATROOM_PRESENCE = os.environ.get('ROOMS', '').split() or ROOMS_TO_JOIN

AUTOINSTALL_DEPS = True


DEFAULT_CONFIG = {
    'LabHub': {
        'GH_TOKEN': os.environ.get('GH_TOKEN'),
        'GL_TOKEN': os.environ.get('GL_TOKEN'),
        'GH_ORG_NAME': os.environ.get('GH_ORG_NAME', 'coala'),
        'GL_ORG_NAME': os.environ.get('GL_ORG_NAME', 'coala'),
    },
}
