
import json

class InvalidRequestFormat(Exception): pass
     

class Request:
  def __init__(self, reqStr: str):
    self.headers = dict()
    self.parseRequest(reqStr.replace("\r", ""))

  def parseRequest(self, reqStr:str):
      splitStr = reqStr.split("\n")
      try:
        self.requestLine(splitStr[0])
        self.parseOptionalHeaders(splitStr[1:])
      except IndexError:
        raise InvalidRequestFormat
        
  def requestLine(self, line: str):
      lineSplit = line.split(" ")
      self.method = lineSplit[0]
      self.uri = lineSplit[1]
      self.protocol = lineSplit[2]

  def __repr__(self):
    return self.toJson()

  def toJson(self):
      items = self.headers.copy()
      items['Method'] = self.method
      items['Uri'] = self.uri
      items['Protocol'] = self.protocol
      return json.dumps(items)

  def parseOptionalHeaders(self, array):
    for line in array:
        elements = line.split(":")
        if (len(elements) == 2):
            self.headers[elements[0]] = elements[1]
        else:
            self.headers[elements[0]] = (":").join(elements[1:])
