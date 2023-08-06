import fabric
from . import commands

class Connection (fabric.Connection):
    def run2 (self, cmd):
        x = self.run (cmd, hide = True)
        pcmd = cmd.split ()[0]
        try:
            rclass = getattr (commands, pcmd)
        except AttributeError:
            rclass = commands.default

        r = rclass.Result (x.stdout, pcmd)
        x.command = cmd
        x.header = r.header
        x.meta = r.meta
        x.data = r.data
        return x

def connect (host, user = 'ubuntu', password = None, key_file = None, port = 22):
    if hasattr (host, 'public_dns_name'):
        host = host.public_dns_name
    if key_file:
        return Connection (host, user, port = port, connect_kwargs = dict (key_filename = key_file))
    return Connection (host, user, port = port, connect_kwargs = dict (password = password))
