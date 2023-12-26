
function count(elemtntId,maxvalue) {
    let element = document.getElementById(elemtntId)
    let y = 0
    let interval = setInterval(() => {
        if (y <= maxvalue) {
            element.innerText = y
            y += 1
        }
        else {
            clearInterval(interval)
        }
    });
}

count("tuition_count",656)
count("teacher_count",547)
