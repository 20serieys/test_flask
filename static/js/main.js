

window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );

    document.onkeydown = function(e){
        switch(e.keyCode){
            //clavier joueur 1
            case 37:
                socket.emit("move_1", {dx:-1, dy:0});
                break;
            case 38:
                socket.emit("move_1", {dx:0, dy:-1});
                break;
            case 39:
                socket.emit("move_1", {dx:1, dy:0});
                break;
            case 40:
                socket.emit("move_1", {dx:0, dy:1});
                break;
            
            //clavier joueur 2
            case 41:
                socket.emit("move_2", {dx:-1, dy:0});
                break;
            case 42:
                socket.emit("move_2", {dx:0, dy:-1});
                break;
            case 43:
                socket.emit("move_2", {dx:1, dy:0});
                break;
            case 44:
                socket.emit("move_2", {dx:0, dy:1});
                break;
            //clavier sauvegarde
            case 83:
                console.log("start save");
                socket.emit("save");
                break;
        }


    };
    
    // boutons du joueur 1
    var btn_n = document.getElementById("go_n");
    btn_n.onclick = function(e) {
        console.log("Clicked on button north (player 1)");
        socket.emit("move_1", {dx:0, dy:-1});
    };

    var btn_s = document.getElementById("go_s");
    btn_s.onclick = function(e) {
        console.log("Clicked on button south (player 1)");
        socket.emit("move_1", {dx:0, dy:1});
    };

    var btn_w = document.getElementById("go_w");
    btn_w.onclick = function(e) {
        console.log("Clicked on button west (player1)");
        socket.emit("move_1", {dx:-1, dy:0});
    };

    var btn_e = document.getElementById("go_e");
    btn_e.onclick = function(e) {
        console.log("Clicked on button east (player 1)");
        socket.emit("move_1", {dx:1, dy:0});
    };

    // boutons du joueur 2
    var btn_n_2 = document.getElementById("go_n_2");
    btn_n_2.onclick = function(e) {
        console.log("Clicked on button north (player 2)");
        socket.emit("move_2", {dx:0, dy:-1});
    };

    var btn_s = document.getElementById("go_s_2");
    btn_s.onclick = function(e) {
        console.log("Clicked on button south (player 2)");
        socket.emit("move_2", {dx:0, dy:1});
    };

    var btn_w = document.getElementById("go_w_2");
    btn_w.onclick = function(e) {
        console.log("Clicked on button west (player 2)");
        socket.emit("move_2", {dx:-1, dy:0});
    };

    var btn_e = document.getElementById("go_e_2");
    btn_e.onclick = function(e) {
        console.log("Clicked on button east (player 2)");
        socket.emit("move_2", {dx:1, dy:0});
    };

    // Chargement d'une sauvegarde
    var charge = document.getElementById("charge_save");
    charge.onchange = function(){
        console.log("un fichier a été chargé");
        var reader = new FileReader();
        var json_charge = reader.readAsText(charge.files[0]);
        socket.emit("charge", charge.files[0]);
    };

    
    // Enregistre la sauvegarde
    socket.on("save_response", function(data_save, filename) {
        console.log("Back in js")
        var filename = 'rogue-save'
        var data = data_save
        var file = new Blob([data], {type: JSON});
        if (window.navigator.msSaveOrOpenBlob) // IE10+
            window.navigator.msSaveOrOpenBlob(file, filename);
        else { // Others
            var a = document.createElement("a"),
                    url = URL.createObjectURL(file);
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            setTimeout(function() {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);  
            }, 0); 
        }
    });

    socket.on("response", function(data){
        console.log(data)
        for( var k=0; k<1; k++){ // 14 car 6 monstres et 1 joueurs fois deux coordonnées
            var cell_id = "cell " + data[k].i + "-" + data[k].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.textContent = data[k].content;
        }

        // rafraîchissement des stats du joueur
        var PV = document.getElementById("PV_1");
        PV.textContent = data[14];
        var money = document.getElementById("money_1");
        money.textContent = data[15];
        var protection = document.getElementById("protection_1");
        protection.textContent = data[16];
        var PV = document.getElementById("PV_2");
        PV.textContent = data[17];
        var money = document.getElementById("money_2");
        money.textContent = data[18];
        var protection = document.getElementById("protection_2");
        protection.textContent = data[19];
    });

});