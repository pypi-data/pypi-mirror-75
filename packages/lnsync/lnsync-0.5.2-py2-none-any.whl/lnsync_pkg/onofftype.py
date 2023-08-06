#!/usr/bin/env python

# Copyright (C) 2020 Miguel Simoes, miguelrsimoes[a]yahoo[.]com
# For conditions of distribution and use, see copyright notice in lnsync.py

"""
A framework for maintaining parallel class inheritance structures.

If instances of A have some constant two-value attribute "mode", which
determines the behavior its methods, this framework allows defining subclasses
A1 and A2 of A, with each subclass implementing the corresponding "mode"
behaviors and A the commonalities.

When creating an instance, x=A(mode=1) can be used, and the correct subclass A1
is selected.

Moreover, if B->A and the B likewise declenses on the "mode" atrtibute, we can
declare subclasses B1->B, B2->B and B->A, so that at instance creation time
y=B(mode=1) will create an object with MRO equivalent to B1->B->A1->A->object.

The mode names here are ONLINE and OFFLINE, instead of 1 and 2.

A metaclass onofftype is provided o achieve the above in this ways:
    class A(metaclass=onofftype): <body of A>
    class A(metaclass=onofftype, mode=ONLINE): <body of Aon>
    class A(metaclass=onofftype, mode=OFFLINE): <body of Aoff>

All classes have __name__ set to "A", "AOnline" and "AOffline", respectively.

NB: In that order of evaluation, A is set to the third class, but this will not
cause any problem in creating instances.

Below, A is a called the None class and the others are mode classes.

If only class A(metaclass=onofftype, mode=ONLINE):  <body of Aon>
is evaluated, a virtual None class A is created (and it will then be illegal
to evaluate class A(metaclass=onofftype): <body of A>.

To subclass do:
    class B(A, metaclass=onofftype): <body of B>
    class B(A, metaclass=onofftype, mode=ONLINE): <body of Bon>
    class B(A, metaclass=onofftype, mode=OFFLINE): <body of Boff>
(Where A may be bound to the None class A, or to any of the mode classes A.)

An alternative usage:
    class B(A, metaclass=onofftype): <body of B>
    class BOnline(A, metaclass=onofftype): <body of Bon>
    class BOffline(A, metaclass=onofftype): <body of Boff>
The suffixes Online and Offline are stripped to obtain both the None class name
and the mode values.

Implementation:

A new base class onoffobject handles instance creation via its __new__, so that
onoffobj.__bases__ == (object,).

Types in the onofftype metaclass are related as follows:
The __bases__ relations are set to:
    B -> (onoffobj,), A -> (onoffobj,)
    Aon -> (A, onoffobj), Bon -> (B, Aon, onoffobj)
A _onoff_super attribute is set to
    Bon -> B, B -> A, Aon -> A, A -> onoffobject
    (It may also happen that A->Z where Z is not in the onofftype metaclass.)

The onofftype metaclass itself keeps two registries:
    1. A record _name_to_none of all mode=None classes by name.
    (This is the name in the declarations, and the __name__ in the
    None class.)
    2. A map _none_to_mode from the mode=None class to the
        mode=ONLINE and mode=OFFLINE subclasses:
       {Cnone:{ONLINE:Con,OFFLINE:Coff}}.

Limitations:
- No multiple inheritance for onofftype classes. (It would only require a
reimplementation of the C3 MRO.)
- The same class name cannot be reused across different scopes, as they are
registered globally.
"""

ONLINE = "online"
OFFLINE = "offline"

_MODES = (ONLINE, OFFLINE)
_MODE_TO_SUFFIX = {ONLINE:"Online", OFFLINE:"Offline"}
_SUFFIXES = tuple(_MODE_TO_SUFFIX.values())

class onoffobj(object):
    def __new__(cls, *_args, mode=None, **_kwargs):
        """cls is an onoff class of arbitrary mode,
        mode must be either ONLINE or OFFLINE."""
        if mode is not None and mode not in _MODES:
            raise RuntimeError("invalid mode: %s" % (mode,))
        if mode is None:
            _name, _mode = onofftype._classname_split(cls.__name__)
            if _mode is None:
                msg = "cannot set mode for: %s"
                raise RuntimeError(msg % (cls.__name__,))
            if _name not in onofftype._name_to_none:
                raise RuntimeError("unknown type: %s" % (_name,))
            none_cls = onofftype._name_to_none[_name]
            mode = _mode
        else:
            none_cls = onofftype._get_noneclass(cls)
        mode_cls = onofftype._get_modeclass(none_cls, mode)
        return super().__new__(mode_cls)

class onofftype(type):
    """onoffobjects instances are dynamically created in one of two varieties,
    "online" or "offline", corresponding to two parallel class hierarchies."""
    _name_to_none = {}
    _none_to_mode = {}

    @staticmethod
    def _classname_split(name):
        for mode in _MODES:
            suffix = _MODE_TO_SUFFIX[mode]
            if name.endswith(suffix):
                return name[:-len(suffix)], mode
        return name, None

    @staticmethod
    def _classname_make(name, mode):
        return "%s%s" % (name, _MODE_TO_SUFFIX[mode])

    @staticmethod
    def _get_noneclass(cls):
        """Given an onoff class of mode ONLINE or OFFLINE or None,
        fetch the corresponding None class."""
        if cls.mode is None:
            return cls
        else:
            assert cls._onoff_super.mode is None
            return cls._onoff_super

    @staticmethod
    def _is_onoff(cls):
        return hasattr(cls, '_onoff_super')
        # TODO cls.__class__ == onoffobj

    @staticmethod
    def _get_canonical(cls):
        """If cls is onoff, return its noneclass, else return cls."""
        if onofftype._is_onoff(cls):
            return onofftype._get_noneclass(cls)
        else:
            return cls

    @staticmethod
    def _get_modeclass(nonecls, mode):
        """Given an onoff class of mode None, and a mode (not None),
        fetch the corresponding mode class (creating it, if needed)."""
        assert nonecls.mode is None
        assert mode is not None
        name = nonecls.__name__
        try:
            modecls = onofftype._none_to_mode[nonecls][mode]
        except KeyError:
            modecls = onofftype(name, (nonecls._onoff_super,), {}, mode=mode)
        return modecls

    @staticmethod
    def _make_mro(cls, mode):
        """Create the tuple of bases for Con or Coff classes to use as
        __bases__, by following __onoff_super links. Assume cls.mode==None.
        """
        assert cls.mode is None
        newbases = [cls]
        cur_cls = cls
        while onofftype._is_onoff(cur_cls._onoff_super):
            cur_cls = cur_cls._onoff_super
            newbases.append(onofftype._get_modeclass(cur_cls, mode))
        newbases.append(cur_cls._onoff_super)
        newbases = tuple(newbases)
        return newbases

    @staticmethod
    def _init_nonecls(nonecls, bases):
        # bases must contain exactly one element, any class.
        # Fill in nonecls, with bases from the class declaration, which must
        # consist in a single class, either onoff of any mode or a single
        # regular class or an empty tuple. Also, register this new none class.
        nonecls.mode = None
        assert len(bases) == 1
        if not onofftype._is_onoff(bases[0]):
            nonecls._onoff_super = bases[0]
        else:
            super_onoff_cls = bases[0]
            if super_onoff_cls.mode is not None:
                super_none_cls = super_onoff_cls._onoff_super
            else:
                super_none_cls = super_onoff_cls
            nonecls._onoff_super = super_none_cls
        onofftype._none_to_mode[nonecls] = {}
        onofftype._name_to_none[nonecls.__name__] = nonecls

    def __new__(mcs, name, bases, attrs,
                *_args, mode=None, **_kwargs):
        # Bases is either empty, or a single class, may or may not be of
        # type onofftype. If bases[0] is onoff, it may be of any mode.
        if len(bases) > 1:
            raise TypeError("onofftype: multiple inheritance not supported")
        if mode is None:
            _name, _mode = onofftype._classname_split(name)
            if _mode is not None:
                mode, name = _mode, _name
                if _name not in onofftype._name_to_none:
                    msg = "unknown class: %s"
                    raise TypeError(msg % (_name,))
                none_cls = onofftype._name_to_none[_name]
                namebase = none_cls._onoff_super
                if bases and bases[0] not in (none_cls, namebase):
                    msg = "declared base not compatible with name base"
                    raise TypeError(msg)
                bases = (namebase,)
        if not bases:
            bases = (object,)
        if mode is None:
            if name in onofftype._name_to_none:
                msg = "class already defined for mode=None: %s"
                raise TypeError(msg % (name,))
            newcls = type.__new__(mcs, name, (onoffobj,), attrs)
            onofftype._init_nonecls(newcls, bases)
            return newcls
        assert mode in _MODES
        # Before creating the mode class, create the none class.
        if name not in onofftype._name_to_none:
            nonecls = onofftype(name, (onoffobj,), {}, mode=None)
        else:
            nonecls = onofftype._name_to_none[name]
        if mode in onofftype._none_to_mode[nonecls]:
            msg = "class already defined for mode=%s: %s"
            raise TypeError(msg % (mode, name))
        modebases = onofftype._make_mro(nonecls, mode)
        # mode bases goes noneclass, basenoneORregular, ...
        if onofftype._get_canonical(bases[0]) != \
            onofftype._get_canonical(modebases[1]):
            msg = "inconsistent base class across modes: None, %s"
            raise TypeError(msg % (name,))
        modename = onofftype._classname_make(name, mode)
        modecls = type.__new__(mcs, modename, modebases, attrs)
        modecls._onoff_super = nonecls
        onofftype._none_to_mode[nonecls][mode] = modecls
        modecls.mode = mode
        return modecls
