from Tkinter import *
import couchdb
import Tkinter


root = Tk()


def MoveView(event):

  print 'Okay'
  if repr(event.char) is '\xef\x9c\x83':
    GoForward()
  elif repr(event.char) is '\xef\x9c\x82':
    GoBackward()

frame = Frame(root, width=200, height=5000)
frame.bind("<Key>", MoveView)
frame.pack(fill=X, expand=True)
label=Label(frame, image='http://lain:<13tg597@127.0.0.1:5984/coordinator/58d48ebebbda27bc0133ac4e8400fb14/values_badge_desktop_mac coassdldnkbaslpy 2.jpg',
bg="red",fg="white")
label.pack
frame.pack_propagate(0)


root.mainloop()
