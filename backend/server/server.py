import socket
from threading import Thread
from typing import Any
from .request_details import Request
import inspect 
from .response_writer import ResponseWriter

class Handler:

  def __init__(self, function) -> None:
     self.function = function
     self.params = inspect.getfullargspec(function)

  def __call__(self, *args: Any, **kwds: Any) -> Any:
     return self.function(*args, **kwds)   

class Server :
  def __init__(self, buffer_size=1024):
      self.buffer_size = buffer_size
      self.urlMapping = {"GET":{}, "PUT":{}, "POST":{}, "DELETE":{}}

  
  def run(self, port=8500, host='localhost', backlog=1, max_calls=2**64):
    
      server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      server.bind((host, port))    
      server.listen(backlog)
      
      print(f"Server listening at http://{host}:{port}")
      
      while max_calls:
          client, address = server.accept()
          print(f"address: {address}")
          Thread(target=lambda: self.handleConnection(client)).start()
          max_calls-=1
          
      
  def handleConnection(self, client:socket.socket):
    
      responseWriter = ResponseWriter()
      request = Request(client.recv(self.buffer_size).decode("utf8"))
      
      try:
        self.processRequest(responseWriter, request)
      except Exception as e:
         print(e.with_traceback(None))
         responseWriter.setStatusCode(500)
      
      client.sendall(responseWriter.getResponse().encode())
      client.close()
        



  def handleFavicon(self, rw: ResponseWriter, r: Request):
    fav = """
            <html>
            <head>
            </head>
            <body>
            <img src="https://img.icons8.com/ios-filled/344/internet.png">
            </body>
            </html>
         """
    rw.setContent(fav)

  def processRequest(self, rw: ResponseWriter, r: Request):
      
      if ("favicon.i" in r.uri): 
          return self.handleFavicon(rw, r)

      handler = self.urlMapping[r.method].get(r.uri)
      if (not handler is None):  
         return handler(rw, r)
     
      rw.setContent(f"Nothing for {r.uri}")  
      print("processed")

  def get(self, pattern):
      return lambda function: self.__add_to_mapping("GET", pattern, function)

  def post(self, pattern):
      return lambda function: self.__add_to_mapping("POST", pattern, function)

  def put(self, pattern):
      return lambda function: self.__add_to_mapping("PUT", pattern, function)

  def delete(self, pattern):
      return lambda function: self.__add_to_mapping("DELETE", pattern, function)

  def __add_to_mapping(self, method, pattern, function):
      self.urlMapping[method][pattern] = Handler(function)
