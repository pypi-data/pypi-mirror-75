"""Interface definition metaclass.

Interfaces are defined using type annotations.
"""
from iprovide.exceptions import InterfaceDefException

class Interface(type):
    """Interface definition metaclass"""

    def __new__(cls, name, bases, classdict):
        """Build the interface class"""
        if [key for key in classdict.keys() if not key.startswith('__')]:
            raise InterfaceDefException

        annotations = classdict.get('__annotations__')
        del classdict['__annotations__']
        classdict['_attributes'] = annotations

        interface = type.__new__(cls, name, bases, classdict)

        return interface
