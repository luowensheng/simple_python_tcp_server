import pprint
import socket
from threading import Thread
from .router import Router
from .request_details import Request
from .response_writer import ResponseWriter

class Server(Router) :
  def __init__(self, buffer_size=1024, **kwargs):
       super().__init__(**kwargs)
       self.buffer_size = buffer_size
    
  
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
      for method in self.urlMapping.keys():
          pprint.pprint(self.urlMapping[method].keys())
      try:
        self.processRequest(responseWriter, request)
      except AssertionError as e:
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

      handler = self.get_handler_for_url(r.method, r.uri)
      if (not handler is None):  
         return handler(rw, r)
     
      rw.setContent(f"Nothing for {r.uri} for Method '{r.method}'")  
      print("processed")

  def get_handler_for_url(self, method:str, uri:str):
       uri = self.process_pattern(uri)
       return self.urlMapping[method].get(uri)
           