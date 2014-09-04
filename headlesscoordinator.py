"""This GUI program either reads in a file, populates the frame with data about
the file with text fields where text is to be entered. This text and the image
data is then sent to a couchdb database which can be queried

Last update: August 11, 2014

Concerns: This is going to take forever

Dependencies: window.py
"""
__author__ = 'Michael Wolf (michael_wolf@intuit.com)'

# class FileObject(object):
#   def __init__(self):

class Coordinator(object,teek.Tk):

      ##

  # file_list_collection = []
  # file_object_collection = []
  #
  def OpenFile(self):
    #next arg
  #
  # def LoadFileData(self, path):
  #   ConnectToDB()
  #   file_object = FileObject()
  #   fileobject.attr1 = data1
  #   fileobject.attrx = datax
  #
  # def ListDirectory(self, path):
  #   for each:
  #     file = FileList()
  #     file_list_collection.append(file)
  #
  #
  def SubmitEntry(self):
    self.Warn()

  def RevertChanges(self):
    print 'Changes reverted!'
  #
  #
  # def Exit(self):
  #   response = frame.Warn()
  #   if response is yes:
  #     exit
  def GoForward(self):
    print 'Went forward!'
    #Warn()
    #go forward

  def GoBackward(self):
    print 'Went backward!'
    #Warn()
    #go backward

  def Warn(self):
    print 'toplevel warning captain, you sure?'

def main():
  coordinator = Coordinator()
  # ConnectToDB(params)

if __name__ == '__main__':
  main()

#//TODO
#Death
