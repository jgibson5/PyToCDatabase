from pyClient import *

class Test(object):
	def __init__(self, name):
		self.name = name

	def assignGrade(self, grade):
		self.grade = grade

	def extraCredit(self, points):
		self.grade += points

if __name__ == "__main__":
	PM = PickleMonger()
	PM.addClass(Test)
	student1 = Test("Abe")
	student2 = Test("Joe")

	PM.addInstances(Test, student1, student2)

	print PM.getInstances(Test)

	PM.executeMethod(Test, "assignGrade")