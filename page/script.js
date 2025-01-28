ip='http://127.0.0.1:4444'

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
    request.open('GET', ip + "/get_report?rep=" + input, true);
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
request.open('GET', ip + "/scan?name=" + name + '&wildcards=' + wildcards + "&subs=" + subdomains + "&out=" + out, true);
request.send();
}
function Notes() {
    var request = new XMLHttpRequest(); 
    var input = document.getElementById("input").value;
    request.onreadystatechange = function() {
        if (request.readyState === XMLHttpRequest.DONE) {
            if (this.readyState == 4 && request.status === 200) {
                document.getElementById('notes').innerHTML = request.responseText;
            }
            else {
                document.getElementById('notes').innerHTML = 'ERROR';
            }
    }
}
request.open('GET',ip + "/get_notes?proj=" + input, true);
request.send();
}
function Clear_notes() {
    var request = new XMLHttpRequest(); 
    var input = document.getElementById("input").value;
    request.onreadystatechange = function() {
        if (request.readyState === XMLHttpRequest.DONE) {
            if (this.readyState == 4 && request.status === 200) {
                document.getElementById('notes').innerHTML = request.responseText;
            }
            else {
                document.getElementById('notes').innerHTML = 'ERROR';
            }
    }
}
request.open('GET', ip + "/clear_notes?proj=" + input, true);
request.send();
}
function DeleteProj() {
    var request = new XMLHttpRequest(); 
    var input = document.getElementById("input").value;
    request.onreadystatechange = function() {
        if (request.readyState === XMLHttpRequest.DONE) {
            if (this.readyState == 4 && request.status === 200) {
                document.getElementById('notes').innerHTML = request.responseText;
            }
            else {
                document.getElementById('notes').innerHTML = 'ERROR';
            }
    }
}
request.open('GET', ip + "/delete_proj?proj=" + input, true);
request.send();
}


