var pages = [
    ["Home", "/shipakinator/home"],
    ["ACFC Shipakinator", "/shipakinator/game"]
]

function topbar() {
    var i = 0;

    while (i < pages.length) {
        var page = pages[i];
        document.getElementById('topbar').innerHTML += "<a href=" + page[1] + ">" + page[0] + "</a> ";

        i++;
    }
}

topbar()