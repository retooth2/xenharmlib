import importlib
import pkgutil
import sys
from warnings import warn

# plugins are discovered by prefix convention
# packages with prefix 'xenharmlib_foo' are
# linked to xenharmlib.ext.foo

PREFIX = 'xenharmlib_'

for finder, name, ispkg in pkgutil.iter_modules():

    if name.startswith(PREFIX):

        ext_name = name[len(PREFIX):]

        try:
            module = importlib.import_module(name)
            sys.modules[f'xenharmlib.ext.{ext_name}'] = module

        except Exception as exc:
            warn(
                f'Could not import extension {name}. Got exception {exc}',
                UserWarning
            )

