#!/usr/bin/env python3

import os
import sys
import base64

# Where to look for the secrets file.
basedir = "/" if os.geteuid() == 0 else os.environ.get('HOME')
default_filename = os.path.join(basedir, "etc/secrets")

# Default encoding to use in case of base64 decode (maybe also others in the
# future).
default_encoding = "utf-8"

# tag => decoder function mapping for tagged values in the secrets file. If a
# secret value starts with a tag, find the decoder function here.
decoders = {
    "{b64}": lambda string, encoding: str(base64.b64decode(string), encoding),
}


def maybe_decode(string, encoding):
    """Decode the string, if tagged and necessary.

    See `decoders` above for available decoding functions.

    """
    for tag, decode_func in decoders.items():
        if string.startswith(tag):
            string = decode_func(string[len(tag):], encoding)
    return string


def getsecret(key, fname=None, encoding=default_encoding):
    """Get a secret tagged with `key` from the secrets file `fname`.

    The default pathname for the secrets file is `/etc/secrets` if
    called by root, and `$HOME/etc/secrets` for normal users.

    The file consist of lines of the form `_key_:_value_`, so the key
    may not contain a colon. Whitespace is significant except at the end
    of the line, where it will be stripped, so the secret may not end
    with whitespace. You can get around these limitations by encoding
    key and/or value with e.g. base64.

    If the key is found, the value is returned. Otherwise, a `KeyError`
    exception is raised. The exception's arguments are a format string,
    the key, and the file name. (Splitting this up allows for subsequent
    i18n.)

    If the found value for the key starts with "{b64}", it will be
    base64-decoded before it is returned.

    """
    if fname is None:
        fname = default_filename
    with open(fname) as f:
        for line in f:
            tag, *value = line.split(":", 1)
            if value and tag == key:
                return maybe_decode(value[0].rstrip(), encoding)
    raise KeyError("cannot find secret for '{}' in '{}'", key, fname)


def main():
    if not (2 <= len(sys.argv) <= 3):
        sys.exit("usage: getsecret key [filename]")
    try:
        print(getsecret(*sys.argv[1:]))
    except Exception as e:
        sys.exit("getsecret: " + e.args[0].format(*e.args[1:]))


if __name__ == '__main__':
    main()
