var items = [];

var dsc = [
    ["Dagger", "dagger.png", "DSC", "Is your ship a Capital?", "Is your ship a Battleship?", "Would your ship be sharp if it was used as a weapon?"],
    ["M-80", "m80.png", "DSC", "Is your ship a Light Tank?", "Does your ship hover on land?"],
    ["Axe", "axe.png", "DSC", "Is your ship a Frigate?", "Is your ship vertical?", "Would your ship be sharp if it was used as a weapon?"],
    ["Kunai", "kunai.png", "DSC", "Is your ship an attack drone?", "Is your ship tiny?"],
    ["Katana", "katana.png", "DSC", "Is your ship a Capital?", "Is your ship a Battleship?", "Does your ship have many tetras?"],
    ["Lance", "lance.png", "DSC", "Is your ship a Gunship?", "Is your ship's 'top deck' flatter than the hull?"],
    ["Flyswatter Mk3", "flyswattermk3.png", "DSC", "Is your ship a Fighter?", "Does your ship have wings?"],
    ["Razor", "razor.png", "DSC", "Is your ship a Frigate?", "Does your ship have a long nose?", "Does your ship have wings?"],
    ["Zeus Laser System", "zeus.png", "DSC", "Is your ship an ODP?", "Does your ship have a shark mouth decal?"],
    ["Greatsword", "greatsword.png", "DSC", "Is your ship a Capital?", "Is your ship a Battleship?", "Does your ship have a front inset?"],
    ["Talwar", "talwar.png", "DSC", "Is your ship a Capital?", "Is your ship a Cruiser?", "Does your ship have a front inset?", "Does your ship have a shark mouth decal?"],
    ["Longsword", "longsword.png", "DSC", "Is your ship a Destroyer?", "Does your ship have a long nose?"],
    ["Gladius", "gladius.png", "DSC", "Is your ship a Corvette?", "Does your ship have a barrel?"],
    ["CH-64", "ch64.png", "DSC", "Is your ship a Freighter?", "Does your ship carry 32 or more crates?"],
    ["CH-16", "ch16.png", "DSC", "Is your ship a Freighter?", "Does your ship carry less than 32 crates?"],
];

var hoh = [
    ["Tahom II ", "tahom.png", "Hearts of Hades", "Is your ship a Capital?", "Is your ship a Cruiser?", "Does your ship have 2 'knives' on each side.", "Are your ship's neon's orange?"],
    ["Tahom D2 ", "diabolustahom.png", "Hearts of Hades", "Is your ship a Capital?", "Is your ship a Cruiser?", "Does your ship have 2 'knives' on each side.", "Are your ship's neons red?"],
    ["Trozen III ", "trozen.png", "Hearts of Hades", "Is your ship a Frigate?", "Does your ship have multiple modifications?", "Are your ship's neons purple?"],
    ["Unicry", "unicry.png", "Hearts of Hades", "Is your ship a Patrol Ship?", "Does your ship have multiple modifications?", "Does your ship have two sections connected to each other by a 'neck'?"],
    ["Monocry", "monocry.png", "Hearts of Hades", "Is your ship a Corvette?", "Does your ship have a younger sibling?", "Does your ship have two sections connected to each other by a 'neck'?"],
    ["Pylian", "pylian.png", "Hearts of Hades", "Is your ship a Corvette?", "Does your ship have 'ventral miniguns'?", "Is your ship 'wide'?"],
    ["Locust", "locust.png", "Hearts of Hades", "Is your ship a Fighter?", "Does your ship have multiple modifications?", "Does your ship have 4 wings?"],
    ["Instar", "instar.png", "Hearts of Hades", "Is your ship a Fighter?", "Does your ship have multiple modifications?", "Is your ship thin?"],
]

var ufp = [
    ["Kentaurus", "kentaurus.png", "UFP", "Is your ship a Capital?", "Is your ship a Carrier?", "Does your ship have 4 nacelles?"],
    ["Inquiry", "inquiry.png", "UFP", "Is your", "Is your ship a Capital?", "Is your ship a Battleship?", "Does your ship's nacelle pylons go frontward?", "Does your ship have a front inset?"],
    ["Thanatos", "thanatos.png", "UFP", "Is your ship a Capital?", "Is your ship a Battleship?", "Does your ship's nacelle pylons go frontward?", "Is your ship's front smooth?"],
    ["Hermes", "hermes.png", "UFP", "Is your ship a Capital?", "Is your ship a Cruiser?", "Does your ship's saucer have tailfin shaped sides?"],
    ["Vesta", "vesta.png", "UFP", "Is your ship a Capital?", "Is your ship a Cruiser?", "Does your ship's nacelle pylons bend?"],
    ["Credence", "credence.png", "UFP", "Is your ship a Capital?", "Is your ship a Cruiser?", "Does your ship have a neck?"],
    ["Eclipse", "eclipse.png", "UFP", "Is your ship a Capital?", "Is your ship a Cruiser?", "Is your ship's front wide?"],
    ["Judge", "judge.png", "UFP", "Is your ship a Destroyer?", "Does your ship have 4 nacelles?", "Is your ship's saucer a dorito?"],
    ["Arrowhead", "arrowhead.png", "UFP", "Is your ship a Gunship?", "Is your ship's saucer a dorito?"],
]

var kneall = [
    ["Scout", "scout.png", "Kneall", "Is your ship an Old Gen?", "Is your ship based off a roblox game?", "Does your ship have 4 ventral 'arms'?"],
    ["Swarmer", "swarmer.png", "Kneall", "Is your ship an Old Gen?", "Is your ship based off a roblox game?", "Does your ship have semicircle wings?"],
    ["Bruiser", "bruiser.png", "Kneall", "Is your ship an Old Gen?", "Is your ship based off a roblox game?", "Is your ship's ventral one cannon?"],
    ["Outrider", "outrider.png", "Kneall", "Is your ship an Old Gen?", "Is your ship based off a roblox game?", "Does your ship have secondary wings behind the primary ones?"],
    ["Punisher", "punisher.png", "Kneall", "Is your ship an Old Gen?", "Is your ship based off a roblox game?", "Is your ship thin?"],
    ["Lapis", "lapis.png", "Kneall", "Is your ship a Light Tank?", "Does your ship look futuristic?", "Does your ship have a double-barrel turret?"],
    ["Thoroughbred", "thoroughbred.png", "Kneall", "Is your ship a Hover Tank?", "Does your ship look futuristic?", "Does your ship have a quadruple-barrel turret?"],
    ["Thrasher", "thrasher.png", "Kneall", "Is your ship a Heavy Tank?", "Does your ship look futuristic?", "Does your ship have 4 'wheel pods'?"],
]

var westerlight = [
    ["Tanto", "tanto.png", "Westerlight", "Is your ship a Corvette?", "Is your ship used for escorting cargo runs?", "Does your ship's front end at 1 singular point?"],
]

var mbr = [
    ["Space Halo", "spacehalo.png", "MBR", "Is your ship a Morbius Ball?", "Is your ball purple?", "Does your ball have a ring?"],
    ["Novean", "novean.png", "MBR", "Is your ship a Morbius Ball?", "Is your ball blue?", "Does your ball have no detail?"],
    ["Vytal", "vytal.png", "MBR", "Is your ship a Morbius Ball?", "Is your ball red?", "Does your ball have no detail?"],
    ["PCEC", "pcec.png", "MBR", "Is your ship a Morbius Ball?", "Is your ball blue?", "Does your ball have a checkerboard pattern?"],
    ["DSC", "dsc.png", "MBR", "Is your ship a Morbius Ball?", "Is your ball red?", "Does your ball have 2 neon stripes?"],
]

var items = [
    ["DSC", dsc],
    ["HoH", hoh],
    ["UFP", ufp],
    ["Kneall", kneall],
    ["Westerlight", westerlight],
    ["MBR", mbr],
];