function LOOKAT() {
    var request = new XMLHttpRequest(); 
    var input = document.getElementById("input").value;

    request.onreadystatechange = function() {
            if (request.readyState === XMLHttpRequest.DONE) {
                if (this.readyState == 4 && request.status === 200) {
                    document.getElementById('Reports').innerHTML = request.responseText;
                }
                else {
                    document.getElementById('Reports').innerHTML = 'ERROR';
                }
        }
    }
    request.open('GET', "http://127.0.0.1:4444/get_report?rep=" + input, true);
    request.send();
}
function SEND() {
    var request = new XMLHttpRequest(); 
    var name = document.getElementById("name").value;
    var wildcards = document.getElementById("wildcards").value;
    wildcards = wildcards.replace(/\n/g, ",");

    var subdomains = document.getElementById("subdomains").value
    subdomains = subdomains.replace(/\n/g, ",");
    var out = document.getElementById("out").value
    out = out.replace(/\n/g, ",");
request.open('GET', "http://127.0.0.1:4444/scan?name=" + name + '&wildcards=' + wildcards + "&subs=" + subdomains + "&out=" + out, true);
request.send();
}
