import sys
print sys.argv
class Class1(object):
   k=7
   def __init__(self,color="green"):
      self.color=color
   def H1(sefl):
      print "HEKK CLASS!"
      
class Class2 (Class1):
   def H2(self):
      print "CLASS2"
      print self.k, "is my color"
      
c1=Class1("blue")
c2=Class2("red")
c1.H1()
c2.H1()
c2.H2()            

seq=range(4)
def add(x,y):
  return x+y
  
print map(add,seq,seq)  
print "SSS"

