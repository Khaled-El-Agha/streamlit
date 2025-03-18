function shutdown() {
    fetch("/shutdown", { method: "POST" })
        .then(response => response.json())
        .then(data => alert(data.status))
        .catch(error => alert("Error: " + error));
}

function copyImages() {
    fetch("/copy_images", { method: "POST" })
        .then(response => response.json())
        .then(data => alert(data.status))
        .catch(error => alert("Error: " + error));
}

function startM4() {
    fetch("/m4_core/start", { method: "POST" })
        .then(response => response.json())
        .then(data => alert(data.status))
        .catch(error => alert("Error: " + error));
}

function stopM4() {
    fetch("/m4_core/stop", { method: "POST" })
        .then(response => response.json())
        .then(data => alert(data.status))
        .catch(error => alert("Error: " + error));
}
