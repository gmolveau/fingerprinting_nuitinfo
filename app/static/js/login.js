document.getElementById('loginForm').addEventListener("submit", function(e) {

    e.preventDefault();
    if ( ! navigator.geolocation){
        alert("old browser, aborting.");
    }
    let form = e.target;
    let request = new XMLHttpRequest();
    let data = {};

    // Récupération du login et du mot de passse
    data.username = form.elements["username"].value;
    data.password = form.elements["password"].value;

    // Récupération de la taille de l'écran
    data.size_screen = screen.height + "x" + screen.width;

        // error no https navigator.geolocation.getCurrentPosition();
    data.lat = 47.644795 ;
    data.long = -2.748394;
    request.open(form.method, form.action);
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify(data));

    request.onload = function() {
        if (request.status > 200){
            alert("Error login")
        }else{
            document.open();
            document.write(request.responseText);
            document.close();
        }
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