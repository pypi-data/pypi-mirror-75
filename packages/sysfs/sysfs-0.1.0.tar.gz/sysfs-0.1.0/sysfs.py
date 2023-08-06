from os import path, listdir, access, R_OK


try:
    IsADirectoryError
except NameError:
    # This violation is acceptable because it will only
    # be executed in python 2 where IsADirectoryError
    # doesn't exist.
    IsADirectoryError = IOError  # noqa: W0622


class Node(object):
    def __init__(self, devpath):
        # Use the base object setattr method because this classes'
        # implementation will attempt to write to the sysfs.
        object.__setattr__(self, "path", devpath)

    def keys(self):
        """Return an iterator of available keys in the sysfs."""
        return (
            p for p in listdir(self.path) if not path.islink(path.join(self.path, p))
        )

    def values(self):
        """Yield each value in the sysfs.

        Write only values will be None.
        """
        for k in self.keys():
            yield self[k]

    def items(self):
        """Yield each key value pair in the sysfs.

        Write only values will be None, but the key will still be
        associated with the value.
        """
        for k in self.keys():
            yield k, self[k]

    @property
    def parent(self):
        return self.__class__(path.dirname(self.path))

    @property
    def name(self):
        return path.basename(self.path)

    def map_tree(self):
        return {
            k: v.map_tree() if isinstance(v, self.__class__) else v
            for k, v in self.items()
        }

    def __getitem__(self, key):
        p = path.join(self.path, key)
        # Sub-nodes should return an instance of Node.
        if path.isdir(p):
            return self.__class__(p)
        # Write only files should return None.
        if path.exists(p):
            if not access(p, R_OK):
                return None
        else:
            raise KeyError(repr(key))
        try:
            # Open and read all other keys.
            with open(p, "rb") as fh:
                contents = fh.read()
            # Attempt to decode as UTF-8, but default to returning bytes.
            try:
                if not isinstance(contents, str):
                    contents = contents.decode()
            except UnicodeDecodeError:
                return contents
            return contents.strip()
        # Failure to read a file that does exist, is a recoverable
        # error. Return None.
        except (OSError, IOError):  # noqa: W0705
            return None

    def __setitem__(self, key, value):
        try:
            with open(path.join(self.path, key), "wb") as fh:
                fh.write(value)
        except (FileNotFoundError, IsADirectoryError):
            raise KeyError(repr(key))

    def __contains__(self, item):
        return item in self.keys()

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(
                    self.__class__.__name__, name
                )
            )

    def __setattr__(self, name, value):
        try:
            self[name] = value
        except KeyError:
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(
                    self.__class__.__name__, name
                )
            )
