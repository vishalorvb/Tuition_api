
function containsOnlyNumbers(str) {
    return /^[0-9]+$/.test(str);
}
function ValidateEmail(mail) {
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(myForm.emailAddr.value)) {
        return (true)
    }
    return (false)
}


function validateForm(names, cname) {
    console.log("Validation")
    let status = true
    names.forEach(element => {
        let collection = document.getElementsByName(element)
        for (let i = 0; i < collection.length; i++) {
            if (collection[i].value == undefined || collection[i].value.trim() == "") {
                collection[i].className += ` ${cname}`
                status = false;
            }
            if ((collection[i].name.includes("phone"))) {
                if (!(containsOnlyNumbers(collection[i].value)) || collection[i].value.length < 10) {
                    collection[i].className += ` ${cname}`
                    status = false;
                }
            }
            if (collection[i].name.toLowerCase().includes("email")) {
                if (ValidateEmail(collection[i].value))
                    console.log(collection[i].value)
            }
        }
    });
    return false;
}
