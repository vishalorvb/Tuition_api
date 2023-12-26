
let slideIntervalTime = 2500
let currentSlide = 0
let slide = document.querySelectorAll('.slides')
slide[currentSlide].style.display = 'block'



function changeSlide() {
    if (currentSlide+1  >= slide.length) {
        slide[slide.length - 1].style.display = 'none'
        currentSlide = 0
        slide[currentSlide].style.display = 'block'
    }
    else{
        slide[currentSlide].style.display = 'none'
        currentSlide += 1 
        slide[currentSlide].style.display = 'block'
    }
}

let timeout = setInterval(changeSlide,slideIntervalTime)

function stopSlide(){
    clearInterval(timeout)
}
function restartSlide(){
    timeout = setInterval(changeSlide,slideIntervalTime)
}



