import re

from ocflib.account.search import user_attrs
from ocflib.account.search import user_attrs_ucb

VHOST_DB_PATH = '/etc/ocf/vhost.conf'


def get_vhost_db():
    """Returns lines from the vhost config file."""
    with open(VHOST_DB_PATH) as f:
        return f.read().splitlines()


def get_vhosts():
    """Returns a list of virtual hosts in convenient format.

    >>> get_vhosts()
    ...
    {
        'bpreview.berkeley.edu': {
            'username': 'bpr',
            'aliases': ['bpr.berkeley.edu'],
            'docroot': '/',
            'flags': [],
        }
    }
    ...
    """
    def fully_qualify(host):
        """Fully qualifies a hostname (by appending .berkeley.edu) if it's not
        already fully-qualified."""
        return host if '.' in host else host + '.berkeley.edu'

    vhosts = {}

    for line in get_vhost_db():
        if not line or line.startswith('#'):
            continue

        fields = line.split(' ')

        if len(fields) < 5:
            flags = []
        else:
            flags = re.match(r'\[(.*)\]$', fields[4]).group(1).split(',')

        username, host, aliases, docroot = fields[:4]

        if aliases != '-':
            aliases = list(map(fully_qualify, aliases.split(',')))
        else:
            aliases = []

        vhosts[fully_qualify(username if host == '-' else host)] = {
            'username': username,
            'aliases': aliases,
            'docroot': '/' if docroot == '-' else docroot,
            'flags': flags,
        }

    return vhosts


def has_vhost(user):
    """Returns whether or not a virtual host is already configured for
    the given user."""
    return any(vhost['username'] == user for vhost in get_vhosts().values())


def eligible_for_vhost(user):
    """Returns whether a user account is eligible for virtual hosting.

    Currently, group accounts, faculty, and staff are eligible for virtual
    hosting.
    """
    attrs = user_attrs(user)
    if 'callinkOid' in attrs:
        return True
    elif 'calnetUid' in attrs:
        attrs_ucb = user_attrs_ucb(attrs['calnetUid'])
        # TODO: Uncomment when we get a privileged LDAP bind.
        if attrs_ucb:  # and 'EMPLOYEE-TYPE-ACADEMIC' in attrs_ucb['berkeleyEduAffiliations']:
            return True

    return False
