
import json
from typing import Union


class ResponseWriter:

  def __init__(self):
      self.__protocol = "HTTP/1.1"
      self.__statusCode = 200
      self.__status = "OK"
      self.__contentType = "text/html"
      self.__content = ""
      self.__headers: dict() = dict()

  def __setitem__(self, key, value):
      self.__headers[key] = value

  def __getitem__(self, key):
      return self.__headers.get(key)

  def setProtocol(self, value):
      self.__protocol = value


  def setStatusCode(self, value):
      self.__statusCode = value


  def setStatus(self, value):
      self.__status = value


  def setContentType(self, value):
      self.__contentType = value


  def setContent(self, value):
      self.__content = value


  def setJsonContent(self, value:Union[dict, str]):
      self.__contentType = "application/json"
      if isinstance(value, dict):
          value = json.dumps(value)
      self.setContent(value)


  def getContentLength(self):
      return len(self.getResponse())


  def getResponse(self):
    return str(self)

  def __str__(self):
    
      headerStr = ""
      for (key, value) in self.__headers.items():
        headerStr+=f"{key}: {value}\r\n"
        
      return f"{self.__protocol} {self.__statusCode} {self.__status}\r\nContent-Type: {self.__contentType}\r\n{headerStr}\r\n\r\n{self.__content}"

