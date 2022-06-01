from __future__ import annotations
import inspect
import json
from typing import Any, List
from .request_details import Request
from .response_writer import ResponseWriter

class Options :
   def __init__(self,*, retry=False, params=False) -> None:
      self.retry = retry
      self.params = params

   def __str__(self) -> str:
      return f"[retry: {self.retry}, params: {self.params}]"
   
   def __repr__(self) -> str:
     return str(self) 

class ParamsException(Exception): pass
  

class Handler:

   def __init__(self, function, pattern:str) -> None:
   
     self.__pattern = pattern 
     self.__inspected_params = inspect.getfullargspec(function)
     self.function = self.__create_handle(function)
     
   def __create_handle(self, func):
      
      annotations =self.__inspected_params.annotations
      filtered = dict(filter(lambda items: items[0]!='return', annotations.items()))

      params: List[type] = sorted(filtered.values(), key=lambda x: str(x))
      num_params = len(params)
      
      if num_params ==2 :
         
         sorted_params = sorted(params, key=lambda x: str(x))
         params_1_is_r = sorted_params[0].__name__ == Request.__name__
         params_2_is_rw = sorted_params[1].__name__, ResponseWriter.__name__
         
         if params_1_is_r and params_2_is_rw:
            
            if params_1_is_r:   
             
               return lambda rw, r: func(r, rw) 
           
            else:
             
               return lambda rw, r: func(rw, r) 
            
      if num_params==0 :
         return lambda rw, _: self.processContent(func(), rw)
   
      raise ParamsException(f"The parameters {params} are not yet supported! Check for any mistakes.\n\n{self.__inspected_params.annotations.get('return')}\n\n")
      
            
            
   def processContent(self, content, rw): 
        
         if isinstance(content, dict):
            return rw.setJsonContent(content)   
         return rw.setContent(content) 
        
   def __call__(self, *args: Any, **kwds: Any) -> Any:
     return self.function(*args, **kwds)  
  
   def __str__(self) -> str:
      return  json.dumps({"function": str(self.function), "options": str(self.options)})
   
   def __repr__(self) -> str:
     return str(self) 
