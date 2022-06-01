```python
app = Server()
router = Router(base_url="/router")


def image_to_base64(img: np.ndarray) -> bytes:
    img_buffer = cv2.imencode('.jpg', img)[1]
    return base64.b64encode(img_buffer).decode('utf-8')


cap = cv2.VideoCapture(0)

@router.get("/")
def index()->Union[str, dict]:
    return "Hello World"

@app.get("/")
def index()->Union[str, dict]:
    return "Hello World"

@app.get() # /about
def about()->Union[str, dict]:
    return "about"    

@app.get("/streaming/ws")
def streamingws():
    ret, frame = cap.read()
    img_b64  = image_to_base64(frame)
    return {"img": f"data:image/png;base64,{img_b64}", "continue": ret}
    

@app.get("/streaming")
def streaming():
    jspath = os.path.join(__file__, "../public/stream.js")
    file= (open(jspath, 'r').read())
    return (f"""
                <img id="image" src="" alt="">
                <script>{file}</script>
                """)

 

@app.get("/img")
def view_img():
    path = os.path.join(__file__, "../../data/img.png")
    img_b64  = image_to_base64(cv2.imread(path))
    return (f"""
                  <img src="data:image/png;base64,{img_b64}">
                  """)


@app.get("/url")
def go_to_url(r:Request, rw:ResponseWriter):
    
    rw.setContent(  """
                        <h1>?<h1>
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
def go_to_url():
    return {"cars":"cool"}


@app.get("/api/request")
def go_to_url(rw:ResponseWriter, r:Request):
    rw.setJsonContent(r.toJson())
 
 
if __name__ == '__main__': 
    app.add_subrouter("/subrouter", router)
    app.run()

```
