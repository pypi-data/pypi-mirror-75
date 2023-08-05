# Config class with configuration file reader

from .namespace import Namespace
from .kvs import parse_kvs
from .alerts import debug

class Config(Namespace):
    """Name space class used to build a config object."""

    def update(self, new_values):
        super().update(new_values, skip_underscore=True, reject_unknown=True)

    def load_from(self, filename, must_exist=False):
        """Read a configuration from file 'filename'."""
        try:
            with open(filename, "r") as f:
                contents = f.read()
        except OSError as exc:
            if not must_exist and exc.errno == 2:   # ENOENT
                debug("config file {} not found".format(filename))
                return None
            else:
                raise exc
        new_locals = {}
        try:
            exec(contents, globals(), new_locals)
        except Exception as e:
            raise type(e)("Error in config file: {}; {}".format(
                filename, e
            ))
        self.update(new_locals)
        return True

    def load_config_files(self, config_files, notice_func=None):
        """Read the configuration from the config files.

        Optional "notice_func" is a function to print a message
        about a config file being loaded.

        """
        for file in config_files:
            if self.load_from(file):
                if notice_func:
                    notice_func("configuration loaded from " + file)

    def update_from_string(self, cfgstring):
        """Update the configuration from a key-value string.

        This can be used to pass config snippets on the command line.
        The string can look like e.g. this:

        "foo=bar,dang=[1,2,15],d={a=b,c=[d,e,f],quux=blech},e=not"

        """
        self.update(parse_kvs(cfgstring))
