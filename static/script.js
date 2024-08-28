// variables
let loading = document.getElementById("loading");
let submitform = document.getElementById("process");
let lockeditable = document.getElementById("lock")
let outputdiv = document.getElementById("output");

// loading gif loader
submitform.addEventListener("click", loadingPannel);
function loadingPannel(){
    console.log("loading start...");
    loading.style.visibility = "visible";
}

// lock unlock event for output section
lockeditable.addEventListener("click", lockunlock);
function lockunlock(){
    if(lockeditable.classList.contains("bi-lock")){ // unlock
        lockeditable.classList.remove("bi-lock");
        lockeditable.classList.add("bi-unlock");
        outputdiv.contentEditable = "true";
    }else{
        lockeditable.classList.remove("bi-unlock"); // lock
        lockeditable.classList.add("bi-lock");
        outputdiv.contentEditable = "false";
    }
}