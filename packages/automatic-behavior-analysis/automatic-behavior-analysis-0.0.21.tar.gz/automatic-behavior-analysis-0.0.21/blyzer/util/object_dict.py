class ObjectDict(dict):
  def __init__(self, *args, **kwargs):
    super(ObjectDict, self).__init__()

    for arg in args:
      if isinstance(arg, dict):
        for k, v in arg.items():
          self[k] = v

    if kwargs:
        for k, v in kwargs.items():
            self[k] = v

  def __getattr__(self, attr):
    # return self.get(attr)
    return self[attr]

  def __setattr__(self, key, value):
    self.__setitem__(key, value)

  def __setitem__(self, key, value):
    super(ObjectDict, self).__setitem__(key, value)

  def __delattr__(self, item):
    self.__delitem__(item)

  def __delitem__(self, key):
    super(ObjectDict, self).__delitem__(key)