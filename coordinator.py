"""This GUI program either reads in a file, populates the frame with data about
the file with text fields where text is to be entered. This text and the image
data is then sent to a couchdb database which can be queried

Last update: August 11, 2014

Concerns: This is going to take forever

Dependencies: window.py
"""
__author__ = 'Michael Wolf (michael_wolf@intuit.com)'
from couchdb import *
from Tkinter import *
import base64
import couchdb
import json
import os.path
import requests
import subprocess
import time
import Tkinter as teek
import window


class FileObject(object):
  """ This object holds all of the data about a single file
  """
  def __init__(self):
    self._filename = ''
    self._file_path = ''
    self._filetype = ''
    self._created_date = ''
    self._category = ''
    self._tags = ''
    self._related_entries = ''
    self._source_url = ''

  @property
  def filename(self):
    return self._filename

  @filename.setter
  def filename(self, value):
    self._filename = value

  @property
  def file_path(self):
    return self._file_path

  @file_path.setter
  def file_path(self, value):
    self._file_path = value

  @property
  def filetype(self):
    return self._filetype

  @filetype.setter
  def filetype(self, value):
    self._filetype = value

  @property
  def created_date(self):
    return self._created_date

  @created_date.setter
  def created_date(self, value):
    self._created_date = value

  @property
  def category(self):
    return self._category

  @category.setter
  def category(self, value):
    self._category = value

  @property
  def tags(self):
    return self._tags

  @tags.setter
  def tags(self, value):
    self._tags = value

  @property
  def related_entries(self):
    return self._related_entries

  @related_entries.setter
  def related_entries(self, value):
    self._related_entries = value

  @property
  def source_url(self):
    return self._source_url

  @source_url.setter
  def source_url(self, value):
    self._source_url = value


class Coordinator(object,teek.Tk):
  """ This application class runs the backend connections and data movement.
  """
  def __init__(self, true_window):
    None

    self._file_list_collection = []
    self._current_position = ''

  def __init__(self):
    None

  @property
  def file_list_collection(self):
    return self._file_list_collection

  @file_list_collection.setter
  def file_list_collection(self, value):
    self._file_list_collection = value

  @property
  def current_position(self):
    return self._current_position

  @current_position.setter
  def current_position(self, value):
    self._current_position = value

  cache = FileObject()

  #
  def OpenFile(event, self, true_window):
    """ Selects a file to view
    Params, event - Tkinter clickable value
            self  - an instance of the app class
            true_window - an instance of the window class

    Returns, path - the directory of the selected file
    """
    path = ''
    while path.find('.jpg') == -1 and path.find('.png') == -1 and path.find('.gif') == -1:
      if path is not '':
        true_window.WrongFileWarn()
      path = true_window.OpenFileDialog()
    self.LoadFileData(path, true_window)
    self.CreateFileList(path)
  #  true_window.UpdatePhoto()
    return path


  def LoadFileData(self, path, true_window):
    """ Reads in data about the file from the path and db, creates a cache, and
        pushes the data to the window.

    Params, self  - an instance of the app class
            path  - the selected file path
            true_window - an instance of the window class
    """
    #clear out the tags, related items, and
    filename = path.split('/')[-1]
    if path.find('.')!=-1:
      ext = path.split('/')[-1].split('.')[1].upper()
    else: ext = 'FILE'
    created = time.ctime(os.path.getctime(path))
    true_window.file_object.filename.set(filename)
    true_window.file_object.file_path.set(path)
    true_window.file_object.filetype.set(ext)
    true_window.file_object.created_date.set(created)
    exists, entry_id, entry_rev = self.SearchExists(path)
    if exists is True:
      print entry_id
      print entry_rev
      #load tags, load category, load related
    self.CacheObject(true_window)
    true_window.UpdatePhoto()
    #QueryDB
    #if exists:
      #fill other attributes
  def SearchExists(self, path):
    exists = False
    entry_id = None
    entry_rev = None
    couch = couchdb.Server('http://lain:<13tg597@127.0.0.1:5984')
    db = couch['coordinator']
    for doc in db:
      if path.lower() == db[doc]['file_path']:
        entry_id = db[doc]['_id']
        entry_rev = db[doc]['_rev']
        exists = True
        print 'hi'
    return exists, entry_id, entry_rev

  def CreateFileList(self, path):
    """ Builds a little image of the file system in order to allow for movement
        between files

    Params, self  - an instance of the app class
            path  - the selected file path
    """
    directory = path.rsplit('/', 1)[0]
    new_list = []
    for file in os.listdir(directory):
      if file.find('.jpg') !=-1 or file.find('.png') !=-1 or file.find('.gif') !=-1:
        new_list.append(directory+'/'+ file)
        self.file_list_collection = new_list
    self.current_position = self.file_list_collection.index(path)


  def CacheObject(self, true_window):
    """ Creates a new file_object object and fills it with the initial state of
        a file details

    Params, self  - an instance of the app class
            true_window - an instance of the window class
    """
    self.cache = self.CreateForm(self.cache)
    self.cache.filename.set(true_window.file_object.filename.get())
    self.cache.file_path.set(true_window.file_object.file_path.get())
    self.cache.category.set(true_window.file_object.category.get())
    self.cache.tags.set(true_window.file_object.tags.get())
    self.cache.related_entries.set(true_window.file_object.related_entries.get())
    self.cache.source_url.set(true_window.file_object.source_url.get())


  def RevertChanges(event, self, true_window):
    """ Uses the cached object to reload the window/focus object with the
        orginal data

    Params, event - a Tkinter thing
            self  - an instance of the app class
            true_window - an instance of the window class
    """
    true_window.file_object.filename.set(self.cache.filename.get())
    true_window.file_object.category.set(self.cache.category.get())
    true_window.file_object.tags.set(self.cache.tags.get())
    true_window.file_object.related_entries.set(self.cache.related_entries.get())
    true_window.file_object.source_url.set(self.cache.source_url.get())
    true_window.RevertFields()


  def MoveForward(event, self, true_window):
    """ Moves the file focus forward (next file down in an ls list)

    Params, event - a Tkinter thing
            self  - an instance of the app class
            true_window - an instance of the window class
    """
    if true_window.file_object.filename.get() != '':
      if self.current_position != (len(self.file_list_collection) - 1):
        self.current_position += 1
      else:
        self.current_position = 0
      new_file_path = self.file_list_collection[self.current_position]
      self.LoadFileData(new_file_path, true_window)
    else:
      print 'No file selected so no moving allowed'


  def MoveBackward(event, self, true_window):
    """ Moves the file focus backward (last file up in an ls list)

    Params, event - a Tkinter thing
            self  - an instance of the app class
            true_window - an instance of the window class
    """
    if true_window.file_object.filename.get() != '':
      if self.current_position != 0:
        self.current_position -= 1
      else:
        self.current_position = (len(self.file_list_collection) - 1)
      new_file_path = self.file_list_collection[self.current_position]
      self.LoadFileData(new_file_path, true_window)


  def SubmitEntry(event, self, true_window):
    """ Organizes and pushes data about a file to a couchdb database

    Params, event - a Tkinter thing
            self  - an instance of the app class
            true_window - an instance of the window class
    """
    if true_window.file_object.filename.get() != self.cache.filename.get():
      true_window.file_object.file_path.set(self.cache.file_path.get().rsplit('/',1)[0] + '/'+ true_window.GetFilenameField())
      os.rename(self.cache.file_path.get(), self.cache.file_path.get().rsplit('/',1)[0] + '/'+ true_window.GetFilenameField())
    #if not already in the place
    self.CreateDocumentEntry(true_window)
    #PUSH THE IMAGE


  def CreateDocumentEntry(self, true_window):
    """Forms the actual CouchDB request and the json which is sent

    Params, self  - an instance of the app class
            true_window - an instance of the window class
    """
    with open(true_window.file_object.file_path.get(), "rb") as image_file:
      encoded_image = base64.b64encode(image_file.read())
    headers = {"Content-Type": "application/json"}
    payload = "{\"_attachments\":{\"%s\":{\"content_type\":\"image/%s\",\"data\":\"%s\"}},\"file_path\":\"%s\",\"created_date\":\"%s\",\"source_url\":\"%s\",\"category\":\"%s\",\"tags\":\"%s\",\"related_entries\":\"%s\"}" % (
      true_window.file_object.filename.get().lower().split('/')[-1], true_window.file_object.filetype.get().lower(), encoded_image,
      true_window.file_object.file_path.get().lower(), true_window.file_object.created_date.get().lower(), true_window.file_object.source_url.get().lower(),
      true_window.file_object.category.get(), true_window.file_object.tags.get().lower(), true_window.file_object.related_entries.get().lower())
    #PUSH THE TAGS ETC
    server_post = requests.post('http://lain:<13tg597@127.0.0.1:5984/coordinator', headers=headers, data=payload)
    print server_post.status_code
    print server_post.text


  def Exit(event, true_window):
    """ Run away

    Params, event - a Tkinter thing
            true_window - an instance of the window class
    """
    true_window.quit()

  def CreateForm(self, file_object):
    """ Generates an empty file_object object

    Params, self  - an instance of the app class
            file_object - an instance of the file_object class

    Returns, the file_object object
    """
    filename_var = StringVar()
    filename_var.set(file_object.filename)
    filepath_var = StringVar()
    filepath_var.set(file_object.file_path)
    filetype_var = StringVar()
    filetype_var.set(file_object.filetype)
    createddate_var = StringVar()
    createddate_var.set(file_object.created_date)
    category_var = StringVar()
    category_var.set(file_object.category)
    tags_var = StringVar()
    tags_var.set(file_object.tags)
    related_var = StringVar()
    related_var.set(file_object.related_entries)
    sourceurl_var = StringVar()
    sourceurl_var.set(file_object.source_url)

    file_object._filename = filename_var
    file_object._file_path = filepath_var
    file_object._filetype = filetype_var
    file_object._created_date = createddate_var
    file_object._category = category_var
    file_object._tags = tags_var
    file_object._related_entries = related_var
    file_object._source_url = sourceurl_var

    return file_object


def main():
  root = Tk()
  app_frame = window.Window(root, False)
  root.mainloop()
  coordinator = Coordinator(app_frame)

  # if #arg:
  #   frame = Frame(None)
  # else:
  #   frame = Coordinator.BuildFrame()
  #
  # ConnectToDB(params)

if __name__ == '__main__':
  main()

#//TODO
# fix category revert etc. How to even?
# Hook up tags/category/related to the window on load (ie reload everytime the view changes for unsubmitted data)
# If the database entry exists, load the data, if the database entry exists, update to the correct id/whatever
# add extra data when it finds a corresponding entry
