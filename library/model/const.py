class Const:
   """
   This class contains all constants.

   Attributes
   ----------

   earth_radius : the earth radius in meter (~ 6378137 m)
      used for geodisic distance calculation.
   
   """
   
   def __init__(self):
       Const.__items = {}
       Const.__items["earth_radius"]=6378137 # earth radius in meter

   def __getattr__(self, attr):
       try:
           return Const.__items[attr]
       except:
           return self.__dict__[attr]

   def __setattr__(self, attr, value):
       if attr in Const._items:
           raise "Cannot reassign constant %s" % attr
       else:
           Const.__items[attr] = value

   def __str__(self):
       return '\n'.join(['%s: %s' % (str(k), str(v)) for k,v in Const.__items.items()])
