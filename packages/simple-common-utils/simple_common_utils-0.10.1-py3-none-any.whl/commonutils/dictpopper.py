class DictPopper:
   def __init__(self, d):
      self.__d = d
      self.__data = dict()
   
   def __iter__(self):
      def f(pair):
         return self.__d.pop(*pair)
      
      return map(f, self.__data.items())
   
   def add(self, key, default = None, spreadKey = False):
      for k in (key, ) if not spreadKey else key:
         self.__data[k] = default
      
      return self
