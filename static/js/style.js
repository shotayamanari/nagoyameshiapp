
    const img_src = ["media/main-visual-1.jpg","media/main-visual-2.jpg","media/main-visual-3.jpg"];
    
    let num = -1;

    function slide_time(){
        if(num == 2){
            num = 0;
        }
        else{
            num++;
        }

        document.getElementById("main_visual").src=img_src[num];    
    }

    setInterval(slide_time, 3000);
