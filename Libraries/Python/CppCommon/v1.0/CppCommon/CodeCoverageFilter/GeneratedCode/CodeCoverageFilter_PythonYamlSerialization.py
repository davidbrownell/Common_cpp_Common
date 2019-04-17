# --------------------------------------------------------------------------------
# |
# |  WARNING:
# |  This file was generated; any local changes will be overwritten during
# |  future invocations of the generator!
# |
# |  Generated by: Plugins/Impl/PythonSerializationImpl.py
# |  Generated on: 2019-04-15 22:11:38.748705
# |
# --------------------------------------------------------------------------------
import copy
import sys

from collections import OrderedDict

import six

import CommonEnvironment
from CommonEnvironment.TypeInfo import Arity
from CommonEnvironment.TypeInfo.AnyOfTypeInfo import AnyOfTypeInfo
from CommonEnvironment.TypeInfo.ClassTypeInfo import ClassTypeInfo
from CommonEnvironment.TypeInfo.DictTypeInfo import DictTypeInfo
from CommonEnvironment.TypeInfo.GenericTypeInfo import GenericTypeInfo
from CommonEnvironment.TypeInfo.ListTypeInfo import ListTypeInfo

from CommonEnvironment.TypeInfo.FundamentalTypes.Serialization.PythonCodeVisitor import PythonCodeVisitor

# <Unused import> pylint: disable = W0611
# <Unused import> pylint: disable = W0614
from CommonEnvironment.TypeInfo.FundamentalTypes.All import *               # <Wildcard import> pylint: disable = W0401

# <Standard import should be placed before...> pylint: disable = C0411

# ----------------------------------------------------------------------
import rtyaml
import yaml

from CommonEnvironment.CallOnExit import CallOnExit
from CommonEnvironment import FileSystem
from CommonEnvironment.TypeInfo.FundamentalTypes.Serialization.YamlSerialization import YamlSerialization


# ----------------------------------------------------------------------
# <Method name "..." doesn't conform to PascalCase naming style> pylint: disable = C0103
# <Line too long> pylint: disable = C0301
# <Too many lines in module> pylint: disable = C0302
# <Wrong hanging indentation> pylint: disable = C0330

# <Too few public methods> pylint: disable = R0903
# <Too many public methods> pylint: disable = R0904
# <Too many branches> pylint: disable = R0912
# <Too many statements> pylint: disable = R0915


# ----------------------------------------------------------------------
class SerializationException(Exception):
    def __init__(self, ex_or_string):
        if isinstance(ex_or_string, six.string_types):
            super(SerializationException, self).__init__(ex_or_string)
        else:
            super(SerializationException, self).__init__(str(ex_or_string))

            self.__dict__ = copy.deepcopy(ex_or_string.__dict__)


class UniqueKeySerializationException(SerializationException):              pass
class SerializeException(SerializationException):                           pass
class DeserializeException(SerializationException):                         pass


class DoesNotExist(object):                                                 pass


# ----------------------------------------------------------------------
# |
# |  Utility Methods
# |
# ----------------------------------------------------------------------
def Deserialize(
    root,
    process_additional_data=False,
    always_include_optional=False,
):
    """Convenience method that deserializes all top-level elements"""

    if isinstance(root, six.string_types):
            if FileSystem.IsFilename(root):
                with open(root) as f:
                    root = rtyaml.load(f)
            else:
                root = rtyaml.load(root)

    result = _CreatePythonObject(
            attributes=None,
        )

    this_result = Deserialize_filter(
        root,
        is_root=True,
        process_additional_data=process_additional_data,
        always_include_optional=always_include_optional,

    )
    if this_result is not DoesNotExist:
        setattr(result, "filter", this_result)
    elif always_include_optional:
        setattr(result, "filter", None)

    this_result = Deserialize_named_filters(
        root,
        is_root=True,
        process_additional_data=process_additional_data,
        always_include_optional=always_include_optional,

    )
    if this_result is not DoesNotExist:
        setattr(result, "named_filters", this_result)
    elif always_include_optional:
        setattr(result, "named_filters", [])

    return result


# ----------------------------------------------------------------------
def Deserialize_filter(
    item,
    process_additional_data=False,
    always_include_optional=False,
    is_root=False,
):
    """Deserializes 'filter' from a YAML object to a python object"""

    if isinstance(item, six.string_types):
        if FileSystem.IsFilename(item):
            with open(item) as f:
                item = rtyaml.load(f)
        else:
            item = rtyaml.load(item)

    if not isinstance(item, list):
        if isinstance(item, dict) and "filter" in item:
            item = item["filter"]
        elif not isinstance(item, dict) and hasattr(item, "filter"):
            item = getattr(item, "filter")
        elif is_root:
            item = DoesNotExist

    try:
        try:
            item = Deserializer().filter(
                item,
                process_additional_data=process_additional_data,
                always_include_optional=always_include_optional,
            )
        except:
            _DecorateActiveException("filter")
    except SerializationException:
        raise
    except Exception as ex:
        raise DeserializeException(ex)

    return item


# ----------------------------------------------------------------------
def Deserialize_named_filters(
    items,
    process_additional_data=False,
    always_include_optional=False,
    is_root=False,
):
    """Deserializes 'named_filters' from a YAML object to a python object"""

    if isinstance(items, six.string_types):
        if FileSystem.IsFilename(items):
            with open(items) as f:
                items = rtyaml.load(f)
        else:
            items = rtyaml.load(items)

    if not isinstance(items, list):
        if isinstance(items, dict) and "named_filters" in items:
            items = items["named_filters"]
        elif not isinstance(items, dict) and hasattr(items, "named_filters"):
            items = getattr(items, "named_filters")
        elif is_root:
            items = DoesNotExist

    try:
        try:
            items = Deserializer().named_filters(
                items,
                process_additional_data=process_additional_data,
                always_include_optional=always_include_optional,
            )

            if items is DoesNotExist:
                items = []
        except:
            _DecorateActiveException("named_filters")
    except SerializationException:
        raise
    except Exception as ex:
        raise DeserializeException(ex)

    return items


# ----------------------------------------------------------------------
# |
# |  Type Infos
# |
# ----------------------------------------------------------------------
filter_TypeInfo                                                             = ClassTypeInfo(OrderedDict([ ( "includes", StringTypeInfo(min_length=1, arity=Arity.FromString('*')) ), ( "excludes", StringTypeInfo(min_length=1, arity=Arity.FromString('*')) ) ]), require_exact_match=True, arity=Arity.FromString('?'))
named_filters_TypeInfo                                                      = ClassTypeInfo(OrderedDict([ ( "glob", StringTypeInfo(min_length=1) ) ]), require_exact_match=True, arity=Arity.FromString('*'))

_filter_TypeInfo_Contents                                                   = OrderedDict([("includes", GenericTypeInfo(arity=Arity.FromString('*'))), ("excludes", GenericTypeInfo(arity=Arity.FromString('*')))])
_named_filters_TypeInfo_Contents                                            = OrderedDict([("glob", GenericTypeInfo()), ("includes", GenericTypeInfo(arity=Arity.FromString('*'))), ("excludes", GenericTypeInfo(arity=Arity.FromString('*')))])

_filter_TypeInfo                                                            = AnyOfTypeInfo([ClassTypeInfo(_filter_TypeInfo_Contents, require_exact_match=False), DictTypeInfo(_filter_TypeInfo_Contents, require_exact_match=False)], arity=Arity.FromString('?'))
_filter_includes_TypeInfo                                                   = StringTypeInfo(min_length=1, arity=Arity.FromString('*'))
_filter_excludes_TypeInfo                                                   = StringTypeInfo(min_length=1, arity=Arity.FromString('*'))
_named_filters_TypeInfo                                                     = AnyOfTypeInfo([ClassTypeInfo(_named_filters_TypeInfo_Contents, require_exact_match=False), DictTypeInfo(_named_filters_TypeInfo_Contents, require_exact_match=False)], arity=Arity.FromString('*'))
_named_filters_glob_TypeInfo                                                = StringTypeInfo(min_length=1)

# ----------------------------------------------------------------------
# |
# |  Deserializer
# |
# ----------------------------------------------------------------------
class Deserializer(object):

    # ----------------------------------------------------------------------
    @classmethod
    def filter(cls, item, always_include_optional, process_additional_data):
        if item in [DoesNotExist, None]:
            _filter_TypeInfo.ValidateArity(None)
            return DoesNotExist

        result = cls._filter_Item(item, always_include_optional, process_additional_data)

        _filter_TypeInfo.ValidateArity(result)

        return result

    # ----------------------------------------------------------------------
    @classmethod
    def filter_includes(cls, items):
        if items in [DoesNotExist, None, []]:
            _filter_includes_TypeInfo.ValidateArity(None)
            return DoesNotExist

        results = []

        for this_index, this_item in enumerate(items or []):
            try:
                results.append(cls._filter_includes_Item(this_item))
            except:
                _DecorateActiveException("Index {}".format(this_index))

        _filter_includes_TypeInfo.ValidateArity(results)

        return results

    # ----------------------------------------------------------------------
    @classmethod
    def filter_excludes(cls, items):
        if items in [DoesNotExist, None, []]:
            _filter_excludes_TypeInfo.ValidateArity(None)
            return DoesNotExist

        results = []

        for this_index, this_item in enumerate(items or []):
            try:
                results.append(cls._filter_excludes_Item(this_item))
            except:
                _DecorateActiveException("Index {}".format(this_index))

        _filter_excludes_TypeInfo.ValidateArity(results)

        return results

    # ----------------------------------------------------------------------
    @classmethod
    def named_filters(cls, items, always_include_optional, process_additional_data):
        if items in [DoesNotExist, None, []]:
            _named_filters_TypeInfo.ValidateArity(None)
            return DoesNotExist

        results = []

        for this_index, this_item in enumerate(items or []):
            try:
                results.append(cls._named_filters_Item(this_item, always_include_optional, process_additional_data))
            except:
                _DecorateActiveException("Index {}".format(this_index))

        _named_filters_TypeInfo.ValidateArity(results)

        return results

    # ----------------------------------------------------------------------
    @classmethod
    def named_filters_glob(cls, item):
        if item in [DoesNotExist, None]:
            _named_filters_glob_TypeInfo.ValidateArity(None)
            return DoesNotExist

        result = cls._named_filters_glob_Item(item)

        _named_filters_glob_TypeInfo.ValidateArity(result)

        return result

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @classmethod
    def _filter_Item(cls, item, always_include_optional, process_additional_data):
        result = _CreatePythonObject(
            attributes=None,
        )

        # includes
        try:
            cls._ApplyOptionalChildren(item, "includes", result, cls.filter_includes, always_include_optional)
        except:
            _DecorateActiveException("includes")

        # excludes
        try:
            cls._ApplyOptionalChildren(item, "excludes", result, cls.filter_excludes, always_include_optional)
        except:
            _DecorateActiveException("excludes")

        # Additional data
        if process_additional_data:
            cls._ApplyAdditionalData(
                item,
                result,
                exclude_names={"includes", "excludes"},
            )

        _filter_TypeInfo.ValidateItem(
            result,
            recurse=False,
            require_exact_match=not process_additional_data,
        )

        return result

    # ----------------------------------------------------------------------
    @classmethod
    def _filter_includes_Item(cls, item):
        return YamlSerialization.DeserializeItem(_filter_includes_TypeInfo, item, **{})

    # ----------------------------------------------------------------------
    @classmethod
    def _filter_excludes_Item(cls, item):
        return YamlSerialization.DeserializeItem(_filter_excludes_TypeInfo, item, **{})

    # ----------------------------------------------------------------------
    @classmethod
    def _named_filters_Item(cls, item, always_include_optional, process_additional_data):
        attributes = OrderedDict()

        # glob
        try:
            attributes["glob"] = cls.named_filters_glob(
                cls._GetPythonAttribute(
                    item,
                    "glob",
                    is_optional=False,
                ),
            )
        except:
            _DecorateActiveException("glob")

        result = _CreatePythonObject(
            attributes=attributes,
        )

        # includes
        try:
            cls._ApplyOptionalChildren(item, "includes", result, cls.filter_includes, always_include_optional)
        except:
            _DecorateActiveException("includes")

        # excludes
        try:
            cls._ApplyOptionalChildren(item, "excludes", result, cls.filter_excludes, always_include_optional)
        except:
            _DecorateActiveException("excludes")

        # Additional data
        if process_additional_data:
            cls._ApplyAdditionalData(
                item,
                result,
                exclude_names={"glob", "includes", "excludes"},
            )

        _named_filters_TypeInfo.ValidateItem(
            result,
            recurse=False,
            require_exact_match=not process_additional_data,
        )

        return result

    # ----------------------------------------------------------------------
    @classmethod
    def _named_filters_glob_Item(cls, item):
        return YamlSerialization.DeserializeItem(_named_filters_glob_TypeInfo, item, **{})

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    @classmethod
    def _ApplyOptionalChild(cls, item, attribute_name, dest, apply_func, always_include_optional):
        value = cls._GetPythonAttribute(
            item,
            attribute_name,
            is_optional=True,
        )

        if value is not DoesNotExist:
            value = apply_func(value)
            if value is not DoesNotExist:
                setattr(dest, attribute_name, value)
                return

        if always_include_optional:
            setattr(dest, attribute_name, None)

    # ----------------------------------------------------------------------
    @classmethod
    def _ApplyOptionalChildren(cls, items, attribute_name, dest, apply_func, always_include_optional):
        value = cls._GetPythonAttribute(
            items,
            attribute_name,
            is_optional=True,
        )

        if value is not DoesNotExist:
            value = apply_func(value)
            if value is not DoesNotExist:
                setattr(dest, attribute_name, value)
                return

        if always_include_optional:
            setattr(dest, attribute_name, [])

    # ----------------------------------------------------------------------
    @classmethod
    def _ApplyOptionalAttribute(cls, item, attribute_name, dest, apply_func, always_include_optional):
        value = cls._GetPythonAttribute(
            item,
            attribute_name,
            is_optional=True,
        )

        if value is not DoesNotExist:
            value = apply_func(value)
            if value is not DoesNotExist:
                dest[attribute_name] = value
                return

        if always_include_optional:
            dest[attribute_name] = None

    # ----------------------------------------------------------------------
    @classmethod
    def _ApplyAdditionalData(
        cls,
        source,
        dest,
        exclude_names,
    ):
        for name, child in [(k, v) for k, v in six.iteritems(source if isinstance(source, dict) else source.__dict__) if not k.startswith("_") and k not in exclude_names]:
            try:
                if isinstance(child, list):
                    children = []

                    for index, item in enumerate(child):
                        item_name = "Index {}".format(index)

                        try:
                            children.append(cls._CreateAdditionalDataItem(item_name, item))
                        except:
                            _DecorateActiveException(item_name)

                    setattr(dest, name, children)
                else:
                    setattr(dest, name, cls._CreateAdditionalDataItem(name, child))
            except:
                _DecorateActiveException(name)

    # ----------------------------------------------------------------------
    @classmethod
    def _CreateAdditionalDataItem(cls, name, source):
        if not isinstance(source, dict):
            source = source.__dict__

        attributes = OrderedDict()
        items = OrderedDict()

        for k, v in six.iteritems(source):
            if k.startswith("_"):
                continue

            if k in source["_attribute_names"]:
                attributes[k] = v
            else:
                items[k] = v

        if len(items) == 1 and next(six.iterkeys(items)) == source.get("_text_attribute_name", None):
            return _CreatePythonObject(
                attributes=attributes,
                **{"simple_value": source[source["_text_attribute_name"]], "_text_attribute_name": "simple_value"},
            )

        result = _CreatePythonObject(
            attributes=attributes,
        )

        for k, v in six.iteritems(items):
            try:
                if isinstance(v, list):
                    new_items = []

                    for index, child in enumerate(v):
                        try:
                            new_items.append(cls._CreateAdditionalDataItem("item", child))
                        except:
                            _DecorateActiveException("Index {}".format(index))

                    setattr(result, k, new_items)
                else:
                    new_item = cls._CreateAdditionalDataItem(k, v)

                    setattr(result, k, new_item)
            except:
                _DecorateActiveException(k)

        return result

    # ----------------------------------------------------------------------
    @staticmethod
    def _GetPythonAttribute(
        item,
        attribute_name,
        is_optional=False,
    ):
        if not isinstance(item, dict):
            item = item.__dict__

        value = item.get(attribute_name, DoesNotExist)
        if value is DoesNotExist and not is_optional:
            raise SerializeException("No items were found")

        return value


# ----------------------------------------------------------------------
class Object(object):
    def __init__(self):
        self._attribute_names = set()

    def __repr__(self):
        return CommonEnvironment.ObjectReprImpl(self)


# ----------------------------------------------------------------------
def _CreatePythonObject(
    attributes=None,
    **kwargs
):
    attributes = attributes or {}

    result = Object()

    for d in [attributes, kwargs]:
        for k, v in six.iteritems(d):
            setattr(result, k, v)

    for k in six.iterkeys(attributes):
        result._attribute_names.add(k)

    return result


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _ValidateUniqueKeys(unique_key_attribute_name, items):
    unique_keys = set()

    for item in items:
        if isinstance(item, dict):
            unique_key = item.get(unique_key_attribute_name)
        else:
            unique_key = getattr(item, unique_key_attribute_name)

        if unique_key in unique_keys:
            raise UniqueKeySerializationException("The unique key '{}' is not unique: '{}'".format(unique_key_attribute_name, unique_key))

        unique_keys.add(unique_key)


# ----------------------------------------------------------------------
def _DecorateActiveException(frame_desc):
    exception = sys.exc_info()[1]

    if not hasattr(exception, "stack"):
        setattr(exception, "stack", [])

    exception.stack.insert(0, frame_desc)

    # <The raise statement is not inside an except clause> pylint: disable = E0704
    raise


# ----------------------------------------------------------------------
def _ObjectToYaml(dumper, data):
    d = dict(data.__dict__)
    for k in list(six.iterkeys(d)):
        if k.startswith("_"):
            del d[k]

    return dumper.represent_dict(d)


yaml.add_representer(Object, _ObjectToYaml)
