class DictPopper:
   def __init__(self, d):
      self.__d = d
      self.__data = dict()
   
   def __iter__(self):
      def f(pair):
         return self.__d.pop(*pair)
      
      return map(f, self.__data.items())
   
   def add(self, key, default = None):
      self.__data[key] = default
      
      return self
