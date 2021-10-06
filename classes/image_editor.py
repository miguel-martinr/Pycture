

from typing import List
# TODO: Check mypy for numpy typing
class ImageEditor:
  # TODO Define a type for image 
  def __init__(self, image) -> None: 
      self.image = image # One image at a time for now
      

  def setImage(self, img):
    self.image = img

  def getImage(self):
    return self.image

  def getNegative(self, method): # TODO Add a default value for method
    """Returns the current image negative by applying the method passed"""
    return method(self.image) 





  