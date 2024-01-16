var packagedItems = [];

var answered = [];
var selectable = [];
var focusedIndex = undefined;
var focused = undefined;

var question = undefined;
var HTMLquestion = undefined;

var yesses = 0;
var nos = 0;

document.getElementById("example-button").style.display = "none";

function packageItems() { 
    var i = 0;

    while (i < items.length) {
        packagedItems = packagedItems.concat(items[i][1]);

        i++;
    }
}

function reload() {
    location.reload();
}

function buttons(buttons) {
    document.getElementById("buttons").innerHTML = null;

    var i = 0;

    while (i < buttons.length) {
        var button = document.getElementById("example-button").cloneNode();
        button.style.display = "initial";
        button.style.padding = "2px";
        button.style.margin = "3px";
        button.innerHTML = buttons[i][0];
        button.onclick = buttons[i][1];

        document.getElementById("buttons").appendChild(button);

        i++;
    }
}

function askQuestion() {
    if (!selectable.includes(focused)) {
        focusedIndex = Math.floor(Math.random() * (selectable.length));
        focused = selectable[focusedIndex];
    }

    document.getElementById("ship").style.display = "none";

    var i = 3;
    var a = 0;
    var b = false;

    while (answered.includes(question) & i < focused.length || a === 0) { 
        question = focused[i];
        HTMLquestion = focused[i];

        if (i === 5 & !b) { 
            question = focused[2];
            if (focused[2] != "ANY") {
                HTMLquestion = "Does your ship belong to " + focused[2] + "?";
            } else {
                HTMLquestion = "Can your ship belong to any faction?";
            }
            b = !b;
            i--;
        }

        i++;
        a++;
    }

    document.getElementById("question").innerHTML = HTMLquestion;
}

function oops() { 
    document.getElementById("question").innerHTML = "I give up, what ship were you going for?";

    buttons(
        [["Restart", reload]],
    );
}

function guessShip() {
    var guesstarget = selectable[0];

    document.getElementById("question").innerHTML = "I guess...  a " + guesstarget[0] + "?";
    document.getElementById("ship").src = "/static/kodiak/images/shipakinator/" + guesstarget[1];
    document.getElementById("ship").style.removeProperty("display");

    buttons(
        [["Restart", reload]],
    );
}

function proceedQuestion() {
    if (selectable.length === 0) { 
        oops();
    } else if (selectable.length === 1) {
        guessShip();
    } else {
        askQuestion();
    }
}

function selectableChisel(boolean) {
    answered.push(question);

    var i = 0;
    var l = selectable.length;

    while (i < l) {
        var item = selectable[i];

        if (item.includes(question) === boolean) {
            selectable.splice(i, 1);
            i--;
            l--;
        }

        i++;
    }
}

function yes() {
    selectableChisel(false)

    yesses++;
    proceedQuestion();
}

function probyes() {
    proceedQuestion();
}

function idk() {
    proceedQuestion();
}

function probno() {
    proceedQuestion();
}

function no() {
    selectableChisel(true)

    nos++;
    proceedQuestion();
}

function start() {
    document.getElementById("akinator").style.display = "contents";
    document.getElementById("ship").style.display = "none";

    document.getElementById("button").style.display = "none";
    document.getElementById("warningtext").style.display = "none";

    selectable = packagedItems;

    buttons(
        [
            ["Yes", yes],
            ["Probably yes", probyes],
            ["I don't know", idk],
            ["Probably no", probno],
            ["No", no]
        ]
    );

    askQuestion();
}

packageItems();