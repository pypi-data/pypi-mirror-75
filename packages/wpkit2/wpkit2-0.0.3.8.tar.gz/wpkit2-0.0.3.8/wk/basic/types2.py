import uuid
import json,os
from json import JSONEncoder
import inspect
from types import MethodType
from  .types import PointDict,join_path



def get_arg_dict(func):
    sign = inspect.signature(func)
    keys = list(sign.parameters.keys())
    dic = dict()
    for key in keys:
        value = sign.parameters.get(key).default
        dic[key] = value
    return dic


def is_bound(m):
    return hasattr(m, '__self__')


class ArgumentSpace(PointDict):
    class EmptyArgument:
        pass

    class EmptyKey:
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seta(__parent__={})

    @classmethod
    def make(cls, *args, **kwargs):
        for arg in args:
            assert isinstance(arg, dict)
        args = list(args)
        args.append(kwargs)

        def my_update(dic1, *dics):
            for dic in dics:
                for k, v2 in dic.items():
                    v1 = dic1.get(k, None)
                    v = v2 if v2 is not None else v1
                    dic1[k] = v
            return dic1

        new = my_update(*args)
        return cls(**new)

    def get_parent(self):
        return self.geta('__parent__')

    def detach_parent(self):
        parent = self.geta('__parent__')
        self.seta(__parent__={})
        return parent

    def set_parent(self, parent):
        assert isinstance(parent, ArgumentSpace)
        self.seta(__parent__=parent)

    def get_argument(self, arg, default=EmptyArgument):
        return self.get(arg, default)

    def get(self, arg, default=EmptyArgument):
        EmptyKey = ArgumentSpace.EmptyKey
        v = PointDict.get(self, arg, EmptyKey)
        if v is EmptyKey or v is None:
            if isinstance(self.geta('__parent__'), ArgumentSpace):
                v = self.geta('__parent__').get_argument(arg, EmptyKey)
                if v is EmptyKey:
                    if default is ArgumentSpace.EmptyArgument:
                        raise Exception('Cannot get argument %s' % (arg))
                    v = default
        return v

    def retrieve_arguments(self, args, strict=True):
        Empty = EmptyKey = ArgumentSpace.EmptyKey

        arg_list = []
        params = []

        def handle_if_empty(arg, name=''):
            if arg is not Empty:
                return arg
            if strict:
                raise Exception('Cannot retrieve argument %s.' % (name))
            return None

        def check_arg_name(txt):
            return True

        if isinstance(args, str):
            if not ',' in args:
                v = self.get_argument(args, Empty)
                return handle_if_empty(v, args)
            else:
                args = args.strip().strip(',').strip().split(',')
                for arg in args:
                    arg = arg.strip()
                    check_arg_name(arg)
                    arg_list.append(arg)
        else:
            assert isinstance(args, (list, tuple, set))
            arg_list = args
        for arg in arg_list:
            params.append(handle_if_empty(self.get_argument(arg, Empty), arg))
        return params


class AttributeSetter:
    class _empty:
        pass
    def seta(self, key, value):
        self.__dict__[key] = value

    def geta(self, key, default=_empty):
        value = self.__dict__.get(key, default)
        if value is AttributeSetter._empty:
            raise KeyError('No such akey named %s.' % (key))
        return value



def class2dict(cls=None,recursive=None,dict_type=None):
    if (recursive or dict_type):
        assert cls is None
    dict_type=dict_type or dict
    def _get_attr_dict(cls,dict_type,recursive=False):
        dic = dict_type()
        for k, v in cls.__dict__.items():
            if k.startswith('__'): continue
            if isinstance(v,type)  and recursive:
                v=_get_attr_dict(v,dict_type,recursive=recursive)
            dic[k] = v
        return dic
    if cls is not None: # use directly by @class2dict
        assert isinstance(cls,type)
        return _get_attr_dict(cls,dict_type=dict_type,recursive=False)
    else: # use by @class2dict() so that you can config the decorator, where you can specify the value of `recursive` and `dict_type`
        def decorator(cls):
            return _get_attr_dict(cls,dict_type=dict_type,recursive=recursive)
        return decorator



class UnChangeableAttribute:
    def __init__(self):
        self.name=None
    def __set__(self, instance, value):
        self.name=value
    def __str__(self):
        return str(self.name)

class AttributeProxy(JSONEncoder):
    def __init__(self, data):
        self.data = data
    def __set__(self, instance, value):
        self.data = value
    def __get__(self, instance, owner):
        return self.data
    def __str__(self):
        return self.data.__str__()
    def __repr__(self):
        return self.__repr__()
    def default(self, o):
        return o.data

class UnsettableAttribute(AttributeProxy):
    def __set__(self, instance, value):
        raise Exception('You can not set this attribute, while you are trying to set it as %s'%(value))

def make_attribute_proxy(value):
    return AttributeProxy(value)
def unsettable_attribute(value):
    return UnsettableAttribute(value)




class PatherPoint:
    def __init__(self, name, location, title, children=[]):
        self.__name__ = name
        self.__location__ = location
        self.__title__ = title
        self.__children__ = children

    def __struct__(cls, indent=0, indent_step=5, indent_char=' ',
                   head_pattern='{title}  {location}  ==> {name}'):
        class_attrs = head_pattern.format(title=cls.__title__ or '/', location=cls.__location__,
                                          name=cls.__name__)
        self_line = '{spaces}{class_attrs}\n'.format(spaces=indent_char * indent, class_attrs=class_attrs)
        children_lines = ''.join(
            [child.__struct__(indent + indent_step, indent_step) for child in cls.__children__])
        return self_line + children_lines

    def __path__(cls, indent=0, indent_step=3, indent_char=' ', head_pattern='{location}'):
        class_attrs = head_pattern.format(name=cls.__name__, title=cls.__title__,
                                          location=os.path.basename(cls.__location__) or '/')
        self_line = '{spaces}{class_attrs}\n'.format(spaces=indent_char * indent, class_attrs=class_attrs)
        children_lines = ''.join(
            [child.__path__(indent + indent_step, indent_step) for child in cls.__children__])
        return self_line + children_lines

    def items(cls):
        return cls.__children__

    def structure(cls, *args, **kwargs):
        return cls.__struct__(*args, **kwargs)

    def map(cls, *args, **kwargs):
        return cls.__path__(*args, **kwargs)

    def path(cls, x=''):
        return join_path(cls.__location__, x)

    def __repr__(cls):
        return '''<PatherPoint name="{name}" location="{location}" title="{title}">'''.format(name=cls.__name__,
                                                                                              location=cls.__location__,
                                                                                              title=cls.__title__)
    def __str__(cls):
        return cls.__location__

    def __call__(self, x=None):
        if x:
            return join_path(self.__location__, x)
        return self.__location__


class PatherMetaClass(type):
    def __new__(cls, name, bases, attrs):
        assert isinstance(name, str)
        assert isinstance(attrs, dict)

        def bind_methods(class_):
            def __struct__(cls, indent=0, indent_step=5, indent_char=' ',
                           head_pattern='{title}  {location}  ==> {name}'):
                class_attrs = head_pattern.format(title=cls.__title__ or '/', location=cls.__location__,
                                                  name=cls.__name__)
                self_line = '{spaces}{class_attrs}\n'.format(spaces=indent_char * indent, class_attrs=class_attrs)
                children_lines = ''.join(
                    [child.__struct__(indent + indent_step, indent_step) for child in cls.__children__])
                return self_line + children_lines

            def __path__(cls, indent=0, indent_step=3, indent_char=' ', head_pattern='{location}'):
                class_attrs = head_pattern.format(name=cls.__name__, title=cls.__title__,
                                                  location=os.path.basename(cls.__location__) or '/')
                self_line = '{spaces}{class_attrs}\n'.format(spaces=indent_char * indent, class_attrs=class_attrs)
                children_lines = ''.join(
                    [child.__path__(indent + indent_step, indent_step) for child in cls.__children__])
                return self_line + children_lines

            def items(cls):
                return cls.__children__

            def structure(cls, *args, **kwargs):
                return cls.__struct__(*args, **kwargs)

            def map(cls, *args, **kwargs):
                return cls.__path__(*args, **kwargs)

            def path(cls, x=''):
                return join_path(cls.__location__, x)

            def __repr__(cls):
                return '''<PatherPoint name="{name}" location="{location}" title="{title}">'''.format(name=cls.__name__,
                                                                                                      location=cls.__location__,
                                                                                                      title=cls.__title__)

            def __str__(cls):
                return cls.map()

            def __call__(self, x=None):
                if x:
                    return join_path(self.__location__, x)
                return self.__location__

            class_.__struct__ = MethodType(__struct__, class_)
            class_.__path__ = MethodType(__path__, class_)
            class_.items = MethodType(items, class_)
            class_.structure = MethodType(structure, class_)
            class_.map = MethodType(map, class_)
            class_.path = MethodType(path, class_)
            class_.__repr__ = MethodType(__repr__, class_)
            class_.__str__ = MethodType(__str__, class_)
            return class_

        def should_dig_into(x):
            if not isinstance(x, type): return False
            if issubclass(x, Pather): return False
            if x.__name__.lower() == 'const': return False
            return True

        def get_string_keys(attrs: dict):
            keys = []
            for k, v in attrs.items():
                if not k.startswith('_') and isinstance(v, str):
                    keys.append(k)
            return keys

        def get_methods_dict(attrs):
            new_attrs = {}
            for k, v in attrs.items():
                if inspect.isfunction(v):
                    new_attrs[k] = v
            return new_attrs

        def convert_string_keys(class_, string_keys, attrs):
            new_attrs = {}
            for key in string_keys:
                new_attrs[key] = join_path(class_.__location__, attrs[key])
            return new_attrs

        __location__ = attrs.get('__location__', '/')
        __title__ = attrs.get('__title__', name.lower())
        keys = list(filter(lambda x: should_dig_into(attrs[x]), attrs.keys()))
        string_keys = get_string_keys(attrs)
        methods = get_methods_dict(attrs)

        def build_class(parent_location, class_):
            attrs = class_.__dict__
            name = class_.__name__
            string_keys = get_string_keys(attrs)
            keys = list(filter(lambda x: should_dig_into(attrs[x]), attrs.keys()))
            methods = get_methods_dict(attrs)
            __title__ = attrs.get('__title__', name.lower())
            __location__ = attrs.get('__location__', None)
            if __location__:
                if not __location__.startswith('/'):
                    __location__ = join_path(parent_location, __location__)
            else:
                __location__ = join_path(parent_location, __title__)

            new_attrs = {}
            for key in keys:
                new_attrs[key] = build_class(__location__, attrs[key])
            __children__ = list(new_attrs.values())
            class_ = PatherPoint(name=name, location=__location__, title=__title__, children=__children__)
            new_attrs.update(convert_string_keys(class_, string_keys, attrs))
            new_attrs.update(**methods)
            for k, v in new_attrs.items():
                if inspect.isfunction(v):
                    args = list(get_arg_dict(v).keys())
                    if args and args[0] == 'self':
                        v = MethodType(v, class_)
                setattr(class_, k, v)

            return class_

        new_attrs = {}
        for key in keys:
            new_attrs[key] = build_class(__location__, attrs[key])
        __children__ = list(new_attrs.values())
        # class_ = PatherPoint(name=name, location=__location__, title=__title__, children=__children__)
        class_ = type.__new__(cls, name, bases, attrs)
        new_attrs.update(
            __location__=__location__, __title__=__title__, __children__=__children__
        )
        new_attrs.update(convert_string_keys(class_, string_keys, attrs))
        new_attrs.update(**methods)
        for k, v in new_attrs.items():
            setattr(class_, k, v)
        class_ = bind_methods(class_)
        return class_


class Pather(metaclass=PatherMetaClass):
    pass





class Monitor(AttributeSetter):
    def __init__(self,on_change):
        self.seta('on_change',on_change)
        self.make_self()
    def _handle_change(self):
        return self.geta('on_change')()

    def recursively_make(self, value):
        if isinstance(value,dict):
            tmp = {}
            for k, v in value.items():
                if isinstance(v, (list,dict)):
                    v = self.recursively_make(v)
                tmp[k] = v
            return MonitoredDict(tmp,on_change=self._handle_change)
        elif isinstance(value,list):
            tmp=[]
            for v in value:
                if isinstance(v, (list,dict)):
                    v = self.recursively_make(v)
                tmp.append(v)
            return MonitoredList(tmp,on_change=self._handle_change)
        else:
            return value

    def make_self(self):
        if isinstance(self, MonitoredList):
            for i in range(len(self)):
                self[i] = self.recursively_make(self[i])
        elif isinstance(self, MonitoredDict):
            for k, v in self.items():
                self[k] = self.recursively_make(v)
class MonitoredList(list,Monitor):
    def __init__(self,lis,on_change):
        list.__init__(self,lis)
        Monitor.__init__(self,on_change)
    def __setitem__(self, key, value):
        value=self.recursively_make(value)
        list.__setitem__(self,key,value)
        self._handle_change()
    def pop(self, index=-1):
        res=list.pop(self,index)
        self._handle_change()
        return res
    def append(self, obj):
        obj=self.recursively_make(obj)
        list.append(self,obj)
        self._handle_change()
    def sort(self,*,key, reverse: bool = False) -> None:
        list.sort(self,key=key,reverse=reverse)
        self._handle_change()
    def reverse(self) -> None:
        list.reverse(self)
        self._handle_change()
    def remove(self, object) -> None:
        list.remove(self,object)
        self._handle_change()
    def __setslice__(self, i, j, sequence):
        for n in range(len(sequence)):
            sequence[i]=self.recursively_make(sequence[i])
        list.__setslice(self,i,j,sequence)
        self._handle_change()
    def __delitem__(self, key):
        list.__delitem__(self,key)
        self._handle_change()
    def __delslice__(self, i, j):
        list.__delslice__(self,i,j)
        self._handle_change()
class MonitoredDict(dict,Monitor):
    point_mode=True
    def __init__(self,*args,on_change,**kwargs):
        dict.__init__(self,*args,**kwargs)
        Monitor.__init__(self,on_change)
    def __setitem__(self, key, value):
        value=self.recursively_make(value)
        dict.__setitem__(self,key,value)
        self._handle_change()
    if point_mode:
        def __setattr__(self, key, value):
            return self.__setitem__(key, value)
        def __getattr__(self, item):
            return self.__getitem__(item)




