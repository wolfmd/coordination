"""Do not run! This is merely a library

Last update: August 11, 2014

Concerns: This is going to take forever

Dependencies: frame.py
"""
__author__ = 'Michael Wolf (michael_wolf@intuit.com)'

from Tkinter import *
import coordinator
import tkFileDialog as tkf
import Image
import ImageTk


#file_object
class Window(Frame):
  """Pretty much controls the UI
  """
  def __init__(self, master, has_initial_entry,):
    Frame.__init__(self)
    app = coordinator.Coordinator()
    frame = Frame(master, height=200, width=400)
    left_frame = Frame(master, height=200, width=200)
    right_frame = Frame(master, height=200, width=200)
    file_object = coordinator.FileObject()
    self.file_object = app.CreateForm(file_object)
    self.has_initial_entry = has_initial_entry

    @property
    def file_object(self):
      return self.file_object

    @file_object.setter
    def file_object(self, value):
      self.file_object = value

    @property
    def has_initial_entry(self):
      return self._has_initial_entry

    @has_initial_entry.setter
    def has_intial_entry(self, value):
      self._has_initial_entry = value

    @property
    def image_label(self):
      return self._image_label

    @image_label.setter
    def image_label(self, value):
      self._image_label = value

    #MENUBAR
    menubar = Menu(master)

    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label='Open', command=lambda: app.OpenFile(app, self))
    file_menu.add_command(label='Save',  command=lambda: app.SubmitEntry(self))
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=lambda: self.ExitWarn(self, app))
    menubar.add_cascade(label='File', menu=file_menu)

    edit_menu = Menu(menubar, tearoff=0)
    edit_menu.add_command(label='Revert', command=lambda: self.RevertWarn(self, app))
    menubar.add_cascade(label='Edit', menu=edit_menu)

    help_menu = Menu(master)
    help_menu.add_command(label='About', command=self.AboutDialog)
    help_menu.add_command(label='Documentation', command=self.HelpDialog)
    menubar.add_cascade(label='Help', menu=help_menu)

    master.config(menu=menubar)

    #LOGO
    temp_photo = PhotoImage(file='img/logo.gif', width=100, height=100)
    self.logo_label = Label(left_frame, image=temp_photo)
    self.logo_label.image = temp_photo
    self.logo_label.pack(expand=1, fill=X, side='top')

    #PHOTO
    if self.has_initial_entry is False:
      temp_photo = PhotoImage(file='img/404.gif')
    else:
      temp_photo = PhotoImage(file=self.file_object.filename.get())
    self.image_label = Label(left_frame, image=temp_photo)
    self.image_label.image = temp_photo
    self.image_label.pack(expand=1, fill=Y, side='top')

    #BACK BUTTON
    self.left_button = Button(left_frame, text="<", fg="red", command=lambda: app.MoveBackward(app, self))
    self.left_button.pack(side=LEFT)

    #OPEN BUTTON
    self.open_button = Button(left_frame, text="Open File", command=lambda: app.OpenFile(app, self))
    self.open_button.pack(side=LEFT)

    #FORWARD BUTTON
    self.right_button = Button(left_frame, text=">", command=lambda: app.MoveForward(app, self))
    self.right_button.pack(side=LEFT)

    left_frame.pack(side=LEFT)

    #TITLE
    filename_title = Label(master, textvariable=self.file_object.filename, anchor='w', font=("Times", 40, "bold"))
    filename_title.pack(fill=X)

    #DIRECTORY
    directory_title = Label(master, text="Directory:", anchor='w', font=(None, 14, "bold"))
    directory_title.pack(fill=X)
    directory = Label(master, textvariable=self.file_object.file_path, anchor='w')
    directory.pack(fill=X)

    #FILETYPE
    filetype_title = Label(master, text="Filetype:", anchor='w', font=(None, 14, "bold"))
    filetype_title.pack(fill=X)
    filetype = Label(master, textvariable=self.file_object.filetype, anchor='w')
    filetype.pack(fill=X)

    #CREATED DATE
    created_title = Label(master, text="Created Date:", anchor='w', font=(None, 14, "bold"))
    created_title.pack(fill=X)
    created_date = Label(master, textvariable=self.file_object.created_date, anchor='w')
    created_date.pack(fill=X)

    #FILENAME
    filename_title = Label(master, text="Filename:", anchor='w', font=(None, 14, "bold"))
    filename_title.pack(fill=X)
    self.filename_entry = Entry(master, textvariable=self.file_object.filename)
    self.filename_entry.pack(fill=X)

    #CATEGORY
    category_title = Label(master, text="Category:", anchor='w', font=(None, 14, "bold"))
    category_title.pack(fill=X)
    self.cat_chosen = StringVar(master)
    self.cat_chosen.set("Other")
    var2 = StringVar(master)
    var2.set("IRL")
    var3 = StringVar(master)
    var3.set("LLI")
    var4 = StringVar(master)
    var4.set("Adorable")
    self.category_optionmenu = OptionMenu(master, self.cat_chosen, var2.get(), var3.get(), var4.get())
    self.category_optionmenu.pack(fill=X)

    #SOURCEURL
    sourceurl_title = Label(master, text="Source URL:", anchor='w', font=(None, 14, "bold"))
    sourceurl_title.pack(fill=X)
    sourceurl_entry = Entry(master, textvariable=self.file_object.source_url)
    sourceurl_entry.pack(fill=X)

    #TAGS
    tag_title = Label(master, text="Tags:", anchor='w', font=(None, 14, "bold"))
    tag_title.pack(fill=X)
    tag_entry = Entry(master, textvariable=self.file_object.tags)
    tag_entry.pack(fill=X)

    #RELATED ITEMS
    related_title = Label(master, text="Related Items:", anchor='w', font=(None, 14, "bold"))
    related_title.pack(fill=X)
    tag_entry = Entry(master, textvariable=self.file_object.related_entries)
    tag_entry.pack(fill=X)

    #SUBMIT BUTTON
    self.sub_button = Button(right_frame, text="Submit Entry", command=lambda: self.SubmitPrep(self, app))
    self.sub_button.pack(side=RIGHT)

    #REVERT BUTTON
    self.rev_button = Button(right_frame, text="Revert Changes", command=lambda: self.RevertWarn(self, app))
    self.rev_button.pack(side=RIGHT)

    #QUIT BUTTON
    self.quit_button = Button(right_frame, text="Quit", command=lambda: self.ExitWarn(self, app))
    self.quit_button.pack(side=RIGHT)

    right_frame.pack()
    frame.pack()

  def OpenFileDialog(self):
    """ Opens up the openfile dialogbox

    Params, self  - an instance of the app class

    Returns, path - the chosen file path
    """
    path = tkf.askopenfilename()
    return path


  def UpdatePhoto(self):
    """ Changes the image label on the tkinterface to the current fellow

    Params, self  - an instance of the app class
    """
    temp_photo = ImageTk.PhotoImage(Image.open(self.file_object.file_path.get()))
    self.image_label.configure(image = temp_photo, width=400, height=400)
    self.image_label.image = temp_photo


  def HelpDialog(self):
    """ Displays a dialog containing documentation
    """
    print 'Things would happen'


  def AboutDialog(self):
    """ Displays a dialog containing an about message
    """
    title_message = "File Coordinator (with CouchDB)"
    about_message = "   v.01   \nCreated with trepidation by Michael Wolf"

    top = Toplevel(bg='grey', height=300, width=400)
    top.title("About this application...")

    title = Message(top, text=title_message, font=(None, 18, "bold"), bg='grey')
    title.pack()

    msg = Message(top, text=about_message, bg='grey')
    msg.pack()


  def RevertFields(self):
    """Reverts the fields which cannot revert themselves"""
    False


  def SubmitPrep(event, self, app):
    """ Nabs some of the form data in the window and places it in a respectable
    storage facility called the file_object

    Params, event - the Tkinter thing
            self  - an instance of the window class
            app   - an instance of the application class
    """
    self.file_object.category = self.cat_chosen
    app.SubmitEntry(app, self)


  def RevertWarn(event, self, app):
    """ Presents a dialog box informing the user that they are about to revert
    changes. If yes is selected, calls the revert function

    Params, event - the Tkinter thing
            self  - an instance of the window class
            app   - an instance of the application class
    """
    title_message = "Are you sure you want to discard changes?"

    top = Toplevel(bg='grey', height=300, width=400)
    top.title("Discard Changes?")

    title = Message(top, text=title_message, font=(None, 18, "bold"), bg='grey')
    title.pack()

    yes_button = Button(top, text="Yes", command=lambda: app.RevertChanges(app, self))
    yes_button.pack()

    no_button = Button(top, text="No", command=top.destroy)
    no_button.pack()


  def ExitWarn(event, self, app):
    """ Presents a dialog box informing the user that they are about to exit. If
    yes is selected, calls the exit function

    Params, event - the Tkinter thing
            self  - an instance of the window class
            app   - an instance of the application class
    """
    title_message = "Are you sure you want to exit and discard changes?"

    top = Toplevel(bg='grey', height=300, width=400)
    top.title("Discard Changes?")

    title = Message(top, text=title_message, font=(None, 18, "bold"), bg='grey')
    title.pack()

    yes_button = Button(top, text="Yes", command=lambda: app.Exit(self))
    yes_button.pack()

    no_button = Button(top, text="No", command=top.destroy)
    no_button.pack()


  def WrongFileWarn(self):
    """ Presents an error message for the user who chooses a non-image file

    Params, self  - an instance of the window class
    """
    title_message = "Please select an image file"

    top = Toplevel(bg='grey', height=300, width=400)
    top.title("Error")

    title = Message(top, text=title_message, font=(None, 18, "bold"), bg='grey')
    title.pack()

    okay_button = Button(top, text="Okay", command=top.destroy)
    okay_button.pack()


  def GetFilenameField(self):
    """Experimental"""
    return self.filename_entry.get()

#//TODO
#if non image file open, throw dialog
