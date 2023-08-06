class SingletonMeta(type):
   def __getattr__(cls, name):
      return (super() if name == "INSTANCE" else cls.INSTANCE).__getattribute__(name)
   
   def __setattr__(cls, name, value):
      (super() if name == "INSTANCE" else cls.INSTANCE).__setattr__(name, value)


class Singleton(metaclass = SingletonMeta):
   def __init__(self):
      if hasattr(self.__class__, "INSTANCE"):
         raise ValueError(f"Only one instance of {self.__class__} can be created")
      
      self.__class__.INSTANCE = self


class Global(Singleton):
   pass

Global()
