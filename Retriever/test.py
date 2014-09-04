from flask import Flask
from Tkinter import Tk
from tkFileDialog import askopenfilename

app = Flask(__name__)

@app.route('/')
def hello_world():
  Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
  filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
  print(filename)
  return filename

if __name__ == '__main__':
    app.run()
