function images(list) {
    document.getElementById("list").innerHTML = null;

    var b = 0;

    while (b < list.length) {
        var text = document.createElement("p")
        text.innerHTML = list[b][0];
        document.getElementById("list").appendChild(text);
        var ships = list[b][1];

        var i = 0;

        while (i < ships.length) {
            var image = document.getElementById("example-image").cloneNode();
            image.src = "/static/kodiak/images/shipakinator/" + ships[i][1];
            image.style.removeProperty("display");

            document.getElementById("list").appendChild(image);

            i++;
        }

        b++;
    }
}

var a = false;
var b = false;

function expand() {
    if (a) {
        document.getElementById("button").innerHTML = "Expand"
        document.getElementById("list").style.display = "none";
    } else {
        document.getElementById("button").innerHTML = "Collapse"
        document.getElementById("list").style.removeProperty("display");
    }

    if (!b) { 
        images(items)
    }

    a = !a;
    b = true;
}