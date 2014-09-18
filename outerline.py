import sys, random
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Outerline(object):
    def __init__(self, w, lineNo):
        self.lineNo = lineNo
        self.occupied = False
        self.status = True
        self.train = None
        if self.lineNo<4:
            self.body = w.create_rectangle(100, self.lineNo*55,
            300, self.lineNo*55+8, fill="#080")
        else:
            self.body = w.create_rectangle(900, (self.lineNo-3)*55,
            1100, (self.lineNo-3)*55+8, fill="#080")

    def update(self, w):
        if self.occupied:
            w.itemconfigure(self.body, fill="#800")
        else:
            w.itemconfigure(self.body, fill="#080")

