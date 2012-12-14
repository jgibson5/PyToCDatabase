import pickle
import marshal
import types
from Exceptions import *

class PickleMonger(object):

  def __init__(self, objectMap=None, classDB=None, dbFileName=".pickleDB.dat", classFileName=".classDB.dat", newDB=0):
    '''Note: Only set newDB to True iff when you want to create a new database. 
    This will wipe out any existing database with the dbFileName.
    '''
    if objectMap == None: objectMap = {}
    if classDB == None: classDB = {}

    self.db = dbFileName
    self.classDBName = classFileName

    if newDB:
      self.objectMap = objectMap
      self.classDB = classDB

      #dump objectMap and classDef sonto the db only if creating a new DB
      dbFile = open(self.db, 'w+b')
      pickle.dump(self.objectMap, dbFile)
      dbFile.close()
      classFile = open(self.classDBName, 'w+b')
      pickle.dump(self.classDB, classFile)
      classFile.close()

    else:
      #get objectMap and classDB from DB if not creating a new DB
      dbFile = open(self.db, 'r+b')
      print dbFile.read()
      # self.objectMap = pickle.load(dbFile)
      dbFile.close()
      classFile = open(self.classDBName, 'r+b')
      self.classDB = pickle.load(classFile)
      classFile.close()

  def saveClasses(self):
    dbFile = open(self.classDBName, 'w+b')
    pickle.dump(self.classDB, dbFile)
    dbFile.close()

  def saveObjects(self):
    dbFile = open(self.db, 'w+b')
    pickle.dump(self.objectMap, dbFile)
    dbFile.close()

  def addClass(self, *args):
    '''adds new class(es) to the DB

    *args refers to a list of serialized dictionaries that contain class definitions.
    Example class definition:
      {
        "name": className,
        "methods": {
          "methodName1": methodName1.func_code
          "methodName2": methodName2.func_code
        }
      }

    The methods section of the class def can be easily created using built-in Python module inspect:
      inspect.getmembers(CLASS, predicate=inspect.ismethod)
      src="http://stackoverflow.com/a/1911287"

    The above line returns a list of tuples of length 2 that groups the method name and the the method.
    You can call func_code on the second element of the tuple to get the method's func_code.
    '''
    # dbFile = open(self.db, 'r+b')
    #currentObjectMap = pickle.load(dbFile)
    
    #parse through all classes the user wants to add.
    for cl in args:            #cl should be a dictionary object that contains class definitions
      name = cl.__dict__['__name__']
      
      #if class with same name already exists, throw DuplicateClassException
      if name in self.classDB.keys(): raise DuplicateClassException

      #populate self.objectMap and self.classes
      self.objectMap[name] = []

      self.classDB[name] = self.marshalClass(cl)
      # classMethods = newClass["methods"] #dictionary that maps method names to each method's serialized func_code
      # for methodName, method in classMethods:
      #   self.classDB[className][methodName] = method
      self.saveObjects()
      self.saveClasses()
    
    

  def addInstance(self, cl, *args):
    '''adds instance(s) of a given class to the DB.

    Note: the parameter, instance, should be a dictionary that maps the instanceName to the pickled instance object
    '''
    className = cl.__dict__['__name__']
    if not className in self.objectMap.keys(): raise MissingClassException
    globals()[className] = self.constructClass(self.classDB[className])
                            
    for instance in args[0]:
      print instance
      instanceName = instance.__name__
      self.objectMap[className].append(instance)
      # setattr(globals, instanceName, instance)
      # for instanceName, instanceObject in instance.keys():
      #   if instanceName in self.objectMap[className].keys():
      #     raise DuplicateInstanceException

        # self.objectMap[className][instanceName] = instanceObject
    print globals()
    print self.objectMap
    self.saveObjects()

  def get(self, className, *args, **kwargs):
    '''returns object(s) stored in the DB.
    '''
    if not className in self.objectMap.keys(): raise MissingClassException
    
    #if no instanceName is given, return all objects within the class.
    if not len(args) and not len(kwargs.keys()):
      return self.objectMap[className]
    
    instances = {}
    if len(args):
      for instanceName in args:
        instances[instanceName] = self.objectMap[className][instanceName]
        for attr, value in kwargs: #if there is a request to look for specific attributes, run it. if not, skip it.
          pass
          #reconstruct class thing
        return instances

  def removeClass(self, *args):
    '''remove an existing class

    Note: this will remove all instances of the class along with the class definitions.
    '''
    for className in args:
      if not className in self.objectMap.keys(): raise MissingClassException

      del self.objectMap[className]
      del self.classDB[className]

    dbFile = open(self.db, 'w+b')
    pickle.dump(self.objectMap, dbFile)
    dbFile.close()
    classFile = open(self.classDB, 'w+b')
    pickle.dump(self.classDB, classFile)
    classFile.close()

  def removeInstance(self, className, instanceName):
    '''remove an instance of a class
    '''
    if not className in self.objectMap.keys(): raise MissingClassException
    if not instanceName in self.objectMap[className].keyse(): raise MissingInstanceException

    del self.objectMap[className][instanceName]
    
    dbFile = open(self.db, 'w+b')
    pickle.dump(self.objectMap, dbFile)
    dbFile.close()

  def executeMethod(self, className, method, *args, **kwargs):
    '''executes specified method on specified instances.
    '''
    instances = get(className, args, kwargs) #get instances

    #reconstruct class & run methods

    dbFile = open(self.db, 'w+b')
    pickle.dump(self.objectMap, dbFile)
    dbFile.close()

    return results

  def changeAttr(self, className, *args, **kwargs):
    '''changes attributes of specific instances
    '''
    instances = get(className, *args)

    #reconstruct class & change attributes

    dbFile = open(self.db, 'w+b')
    pickle.dump(self.objectMap, dbFile)
    dbFile.close()

    return instances

  # Takes a Class definition and returns changed
  # __dict__ for serialization.
  def marshalClass(self, c):
    d = {}
    d['__name__'] = c.__name__
    for a, b in c.__dict__.items():
      if type(b) == types.FunctionType:
        d[a] = b.func_code
      elif type(b) == types.GetSetDescriptorType:
        pass
      else:
        d[a] = b
    return marshal.dumps(d)

  def constructClass(self, m):
    d = marshal.loads(m)
    new = type('Test', (object,), d)
    name = new.__dict__['__name__']
    globals()[name] = new
    for k, v in new.__dict__.items():
      if type(v) == types.CodeType:
         setattr(new, k, types.FunctionType(v, globals(), k))
    return new

# ##BASIC TEST CLASS AND MAIN FOR PICKLEMONGER###
# class Model():
#   def __init__(self,username,instanceName,pw):
#     self.modelName=username
#     self.instanceName=instanceName
#     self.pw=pw

#   def __str__(self):
#     return "Username: %s\nInstanceName: %s\nPassword: %s" % (self.modelName, self.instanceName, self.pw)



# if __name__=="__main__":
#   PM = PickleMonger()
#   t = Model('abe','n1','12345')
#   t2 = Model('abe','n2','2343')
#   t3 = Model('abe','n3','ppp')
#   PM.create('abe')
#   PM.addObject(t)
#   PM.addObject(t2)
#   PM.destroyObjectInstance('abe','n1')

#   print PM.read('abe')

#   abes = PM.read('abe')
#   for i in range(len(abes)):
#     print abes[i]
