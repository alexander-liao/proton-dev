metatables = {
    "test": {
        "__add__": lambda x, y: 3
    }
}

class List:
    def __init__(self, array):
        self.array = array
    def __getitem__(self, index):
        return self.array[index]
    def __setitem__(self, index, value):
        self.array[index] = value
    def __repr__(self):
        return "[%s]" % ", ".join(k["__repr__"]()["default"] for k in self.array)

class Tuple:
    def __init__(self, array):
        self.array = array
    def __getitem__(self, index):
        return self.array[index]
    def __setitem__(self, index, value):
        self.array[index] = value
    def __repr__(self):
        return "(%s)" % (", ".join(k["__repr__"]()["default"] for k in self.array) if len(self.array) != 1 else self.array[0]["__repr__"]()["default"] + ",")

class ProtonObject:
    def __init__(self, tname, attrs):
        self.tname = tname
        self.attrs = attrs
        if self.tname not in metatables:
            raise RuntimeError("meta not found for name '%s'" % self.tname)
    def __getitem__(self, index):
        if index in self.attrs:
            return self.attrs[index]
        if self.tname in metatables:
            if index in metatables[self.tname]:
                return metatables[self.tname][index]
            else:
                raise RuntimeError("no attribute %s found in metatable %s" % (index, self,tname))
        raise RuntimeError("%s not defined for type %s" % (index, tname))
    def __setitem__(self, index, value):
        self.attrs[index] = value
    def __repr__(self):
        return self.tname + " " + str(self.attrs)

class PythonLiteral(ProtonObject):
    def __init__(self, value):
        self.value = value
        self.attrs = {"__str__": str(value), "__repr__": repr(value)}
    def __getitem__(self, index):
        if hasattr(self.value, index):
            return getattr(self.value, index)
        try:
            return self.value[index]
        except:
            return self.attrs[attrname] if index in self.attrs else None
    def __setitem__(self, attrname, value):
        if hasattr(self.value, index):
            setattr(self.value, index, value)
        try:
            self.value[attrname] = value
        except:
            self.attrs[attrname] = value
    def __repr__(self):
        return repr(self.value)
    def __str__(self):
        return str(self.value)
