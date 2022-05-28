function init(){    
    let url = window.location.href
    const stream_url = url+"/ws";
    const image_Slice = document.getElementById("image")
    

    async function run(){
       let response =  await fetch(stream_url);
       let data =  await response.json();
       if (!data.continue) return;
       updateSrc(data.img);
       requestAnimationFrame(run)
    }

    run();


   function updateSrc(arrayBuffer) {
        image_Slice.src = arrayBuffer;
        image_Slice.style.width = `${innerWidth}px`
        image_Slice.style.height = `${innerHeight}px`
    };


}

document.addEventListener("DOMContentLoaded", ()=>init())