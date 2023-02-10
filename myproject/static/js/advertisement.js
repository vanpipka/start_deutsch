
document.addEventListener('DOMContentLoaded', function() {
    //console.log(window.innerWidth)
    if (window.innerWidth <= 768) {
        document.getElementById("ya_rtb_4").hidden = false;
        document.getElementById("ya_rtb_1").remove();
    }
    else{
        document.getElementById("ya_rtb_1").hidden = false;
        document.getElementById("ya_rtb_4").remove();
    }
    }, false);
