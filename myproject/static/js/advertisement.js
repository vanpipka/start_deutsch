
document.addEventListener('DOMContentLoaded', function() {
    //console.log(window.innerWidth)
    if (window.innerWidth <= 768) {
        document.getElementById("ya_rtb_4").hidden = false;
        document.getElementById("footer").removeChild(document.getElementById("ya_rtb_1"));
    }
    else{
        document.getElementById("ya_rtb_1").hidden = false;
        document.getElementById("footer").removeChild(document.getElementById("ya_rtb_4"));
    }
    }, false);
