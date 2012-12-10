import pickle
from Exceptions import *
# DBFILE is a constant which names the file ObjectMap is read from
DBFILENAME = ".pickleDB.dat"


class PickleMonger(object):

    #The constructor creates a database file and an object map
    def __init__(self, objectMap={}):
        dbFile = open(DBFILENAME, 'w+b')
        self.objectMap = objectMap
        pickle.dump(self.objectMap, dbFile)
        dbFile.close()

    #This method is used for adding new models to the database
    def create(self, modelname):
        dbFile = open(DBFILENAME, 'r+b')
        currentObjectMap = pickle.load(dbFile)
        if modelname in currentObjectMap.keys():
            raise MultipleModelException
        self.objectMap[modelname] = []
        dbFile = open(DBFILENAME, 'w+b')
        pickle.dump(self.objectMap, dbFile)
        dbFile.close()

    #This method returns the objects stored in a model
    def read(self, modelName):
        dbFile = open(DBFILENAME, 'r+b')
        self.objectMap = pickle.load(dbFile)
        return self.objectMap[modelName]
        dbFile.close()

    #This method is used to add objects to a model
    def addObject(self, model):
        modelName = model.modelName
        dbFile = open(DBFILENAME, 'r+b')
        self.objectMap = pickle.load(dbFile)
        for instances in self.objectMap[model.modelName]:
            if instances.instanceName == model.instanceName:
                raise MultipleInstanceException()
        self.objectMap[modelName].append(model)
        dbFile = open(DBFILENAME, 'w+b')
        pickle.dump(self.objectMap, dbFile)
        dbFile.close()

    #This method destroys a model
    def destroyModel(self, modelName):
        dbFile = open(DBFILENAME, 'r+b')
        self.objectMap = pickle.load(dbFile)
        self.objectMap.pop(modelName)
        dbFile.close()

    #This method destroys an object in a model
    def destroyObjectInstance(self, modelName, instanceName):
        dbFile = open(DBFILENAME, 'r+b')
        self.objectMap = pickle.load(dbFile)
        for modelObject in self.objectMap[modelName]:
            if modelObject.instanceName == instanceName:
                self.objectMap[modelName].remove(modelObject)
        dbFile.close()




##BASIC TEST CLASS AND MAIN FOR PICKLEMONGER###
class Model():
    def __init__(self,username,instanceName,pw):
        self.modelName=username
        self.instanceName=instanceName
        self.pw=pw

    def __str__(self):
        return "Username: %s\nInstanceName: %s\nPassword: %s" % (self.modelName, self.instanceName, self.pw)



if __name__=="__main__":
    PM = PickleMonger()
    t = Model('abe','n1','12345')
    t2 = Model('abe','n2','2343')
    t3 = Model('abe','n3','ppp')
    PM.create('abe')
    PM.addObject(t)
    PM.addObject(t2)
    PM.destroyObjectInstance('abe','n1')

    print PM.read('abe')

    abes = PM.read('abe')
    for i in range(len(abes)):
        print abes[i]
