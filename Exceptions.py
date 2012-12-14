class DuplicateInstanceException(Exception):
  def __str__(self):
    return "An instance with the same name has already been saved to the \
     database. Run PickleMonger.update(instanceName) to modify the existing instance."

class DuplicateClassException(Exception):
  def __str__(self):
    return "A class with the same name already exists in \
    the database. Rename the class you are trying to save."

class MissingInstanceException(Exception):
	def __str__(self):
		return "No instance with such name exists in the database."

class MissingClassException(Exception):
	def __str__(self):
		return "No class with such name exists in the database. Please add the \
		class to the database prior to adding instances by running PickleMonger.addClass(className)"