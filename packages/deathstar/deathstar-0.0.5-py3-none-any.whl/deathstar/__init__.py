import random, os
"""
This __init__.py file allows Python to read your package files
and compile them as a package. It is standard practice to leave 
this empty if your package's modules and subpackages do not share
any code.
(If your package is just a module, then you can put that code here.)
"""

class DeathStar():
  def __init__(self,dialogue=False):
    self.dialogue = dialogue
  
  def __repr__():
    ascii_death_star="""
                _----_
           _·''  ____ ''·_   
         .'     /    \    '.
        ./     |  ()  |    \. 
      ./        \    /       \.
     ./          ¯¯¯¯         \.
     |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
      '\                      /'
       '\                   /'
        '._               _.'
           '-··__    __··-'
                 ¯¯¯¯
    """
    return ascii_death_star
  

  def fire_at(self,file_name):
    if self.dialogue:
      print("pew")
    os.remove(file_name)

  def trash_compacter(self,object):
    if self.dialogue:
      print("Listen to them, they're dying, R2!")
    del object

class DeathStar2():
  def __init__(self):
    print("Under Construction...")