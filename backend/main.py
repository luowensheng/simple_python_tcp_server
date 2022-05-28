import base64
import os

import numpy as np
from server import Server, Request, ResponseWriter
import cv2


app = Server()


def image_to_base64(img: np.ndarray) -> bytes:
    img_buffer = cv2.imencode('.jpg', img)[1]
    return base64.b64encode(img_buffer).decode('utf-8')


cap = cv2.VideoCapture(0)

@app.get("/streaming/ws")
def js(rw:ResponseWriter, r:Request):
    ret, frame = cap.read()
    img_b64  = image_to_base64(frame)
    rw.setJsonContent({"img": f"data:image/png;base64,{img_b64}", "continue": ret})
    

@app.get("/streaming")
def streaming(rw:ResponseWriter, r:Request):
    jspath = os.path.join(__file__, "../public/stream.js")
    file= (open(jspath, 'r').read())
    rw.setContent(f"""
                <img id="image" src="" alt="">
                <script>{file}</script>
                """)

 

@app.get("/img")
def go_to_url(rw:ResponseWriter, r:Request):
    path = os.path.join(__file__, "../../data/img.png")
    
    img_b64  = image_to_base64(cv2.imread(path))
    rw.setContent(f"""
                  <img src="data:image/png;base64,{img_b64}">
                  """)


@app.get("/url")
def go_to_url(rw:ResponseWriter, r:Request):
    
    rw.setContent(  """
                        <h1>Im Happy<h1>
                        <script>
                            const h1 = document.querySelector("h1");
                            var content = [1, 2]
                            let i = 0;
                            document.addEventListener("click", ()=>{
                            i = (i==0)? 1:0; 
                            h1.textContent = content[i];  
                            })
                        </script>              
                    """)

@app.get("/api")
def go_to_url(rw:ResponseWriter, r:Request):
    rw.setJsonContent({"cars":"cool"})


@app.get("/api/request")
def go_to_url(rw:ResponseWriter, r:Request):
    rw.setJsonContent(r.toJson())
  
app.run()
