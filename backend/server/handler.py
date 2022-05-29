import inspect
import json
from typing import Any
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

   

class Handler:

   def __init__(self, function, params=True) -> None:
   
     self.options = Options(params=params) 
     self.function = self.__handle_for_options(function)
     self.__inspected_params = inspect.getfullargspec(function)

   def __handle_for_options(self, func):
      
      if self.options.params:
         return lambda rw, r: func(rw, r) 
      else :
         return lambda rw, _: self.processContent(func(), rw)
            
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
