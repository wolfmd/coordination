from Tkinter import *

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
label=Label(frame, text="please work", width=10, bg="red",fg="white")
label.pack
frame.pack_propagate(0)
root.mainloop()
