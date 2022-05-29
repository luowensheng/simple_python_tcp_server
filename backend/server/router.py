
import json
import pprint
from typing import Union
from .handler import Handler


class Router :
  def __init__(self,*, base_url=""):
      self.base_url = base_url
      self.urlMapping = {"GET":{}, "PUT":{}, "POST":{}, "DELETE":{}}
      
  def showUrlMapping(self):
      pprint.pprint(self.urlMapping)
      
  def get(self, pattern:Union[None, str]=None, params=False):
      return lambda function: self.__add_to_mapping("GET", pattern, function, params)

  def post(self, pattern:Union[None, str]=None, params=False):
      return lambda function: self.__add_to_mapping("POST", pattern, function, params)

  def put(self, pattern:Union[None, str]=None, params=False):
      return lambda function: self.__add_to_mapping("PUT", pattern, function, params)

  def delete(self, pattern:Union[None, str]=None, params=False):
      return lambda function: self.__add_to_mapping("DELETE", pattern, function, params)

  def __add_to_mapping(self, method, pattern, function, params=False):
             
         if pattern is None:
             pattern =  f"/"+str(function.__name__)
         
         pattern = self.process_pattern(pattern)
         if isinstance(function, Handler):   
            self.urlMapping[method][f"{self.base_url}{pattern}"] = function
         else:   
            self.urlMapping[method][f"{self.base_url}{pattern}"] = Handler(function, params)
            
  def process_pattern(self, pattern):
      
      if len(pattern)==0:
         return "/" 
      
      if pattern[-1] == "/":
         return pattern[:-1]
      return pattern

  def __setitem__(self, pattern, router):
      self.add_subrouter(pattern, router)
      
  def __add__(self, router):
        self.add_router(router)
        return self
    
  def add_router(self, router):
      for method in self.urlMapping.keys():
          for (uri, handler) in router.urlMapping[method].items(): 
              self.__add_to_mapping(method, f"{uri}", handler)  

  def add_subrouter(self, pattern: str, router):
      for method in self.urlMapping.keys():
          for (uri, handler) in router.urlMapping[method].items(): 
              self.__add_to_mapping(method, f"{pattern}{uri}", handler) 
              
  def __str__(self) -> str:
       return json.dumps(self.urlMapping)            
           
