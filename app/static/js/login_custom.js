document.getElementById('loginForm').addEventListener("submit", function(e) {

    e.preventDefault();
    let form = e.target;
    let request = new XMLHttpRequest();
    let data = {};

    // Récupération du login et du mot de passse
    data.username = form.elements["username"].value;
    data.language = form.elements["language"].value;
    data.country = form.elements["country"].value;
    data.size_screen = form.elements["size_screen"].value;
    data.os = form.elements["os"].value;
    data.provider = form.elements["provider"].value;
    data.os_version = form.elements["os_version"].value;
    data.browser = form.elements["browser"].value;

    request.open(form.method, form.action);
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify(data));

    request.onload = function() {

        if(request.responseText >=60){
            info = "Error, an alert has been sent"
        }else if(request.responseText >=30){
            info = "A verification code has been sent by SMS."
        }else{
            info = "Login ok, no alert raised"
        }

        alert("Divergence score = "+request.responseText+"/100\n" +info);
        // let resp = JSON.parse(request.responseText);
        // sessionStorage.setItem("token", resp.data.token);
        // document.location.href = "/";
    };

    request.onerror = function() {
        console.log("front-end error | could not send the login request");
        console.error(request);
    };

    return false;

})