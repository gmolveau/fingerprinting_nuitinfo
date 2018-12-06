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
    data.height = screen.height;
    data.width = screen.width;

    navigator.geolocation.getCurrenftPosition(
        (position) => {
            data.lat = position.coords.latitude;
            data.long = position.coords.longitude;
            request.open(form.method, form.action);
            request.setRequestHeader("Content-Type", "application/json");
            request.send(JSON.stringify(data));
        }, 
        (err) => {
            console.error(err);
        }
    );

    request.onload = function() {
        let resp = JSON.parse(request.responseText);
        sessionStorage.setItem("token", resp.data.token);
        document.location.href = "/";
    };

    request.onerror = function() {
        console.log("front-end error | could not send the login request");
        console.error(request);
    };

    return false;

})