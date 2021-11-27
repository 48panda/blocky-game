#utility class to reduce repetitiveness in code(x and y)
import math
class Vector2():
  def __init__(self,x,y=None):
    if y == None:
      self.x = x[0]
      self.y = x[1]
    else:
      self.x = x
      self.y = y
  def __getitem__(self, item):
    if item == 0:
      return self.x
    if item == 1:
      return self.y
    raise IndexError(f"Vector2 does not have item {item}")
  def __len__(self):
    return 2
  def __add__(self,other):
    if hasattr(other,"__getitem__"):
      # other is multiple values
      return Vector2(self.x + other[0],self.y + other[1])
    else:
      #other is single value
      return Vector2(self.x + other, self.y + other)
  def __radd__(self,other):
    return self + other
  def __mul__(self,other):
    if hasattr(other,"__getitem__"):
      # other is multiple values
      return Vector2(self.x * other[0],self.y * other[1])
    else:
      #other is single value
      return Vector2(self.x * other,self.y * other)
  def __rmul__(self,other):
    return self * other
  def __sub__(self,other):
    if hasattr(other,"__getitem__"):
      # other is multiple values
      return Vector2(self.x - other[0],self.y - other[1])
    else:
      #other is single value
      return Vector2(self.x - other,self.y - other)
  def __rsub__(self,other):
    if hasattr(other,"__getitem__"):
      # other is multiple values
      return Vector2(other[0] - self.x,other[1] - self.y)
    else:
      #other is single value
      return Vector2(other - self.x,other - self.y)
  def __truediv__(self,other):
    if hasattr(other,"__getitem__"):
      # other is multiple values
      return Vector2(self.x / other[0],self.y / other[1])
    else:
      #other is single value
      return Vector2(self.x / other,self.y / other)
  def __rdiv__(self,other):
    if hasattr(other,"__getitem__"):
      # other is multiple values
      return Vector2(other[0] / self.x,other[1] / self.y)
    else:
      #other is single value
      return Vector2(other / self.x,other / self.y)
  def int(self):
    self.x = int(self.x)
    self.y = int(self.y)
  def get_magnitude(self):
    return self.x**2 + self.y**2
  def set_magnitude(self,mag):
    current = self.get_magnitude()
    self *= mag / current
  def rotate(self,angle):
    angle = math.radians(angle)
    mag = self.get_magnitude()
    self.x*=16
    self.y*=9
    self.x,self.y = self.x * math.cos(angle) - self.y * math.sin(angle),self.x * math.sin(angle) + self.y * math.cos(angle)
    self.x /= 16
    self.y /=9
    self.set_magnitude(mag)
