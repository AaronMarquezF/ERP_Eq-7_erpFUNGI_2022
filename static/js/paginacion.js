$(document).ready(function() {
 $ = jQuery.noConflict();
     var select_1 = document.getElementById("select_1");
     $(select_1).change(function() { //Cuando un usuario selecciona alguna opcion de select
         valor = $(this).attr("value"); //Recoje el value de la opcion seleccionada del select

         var dataString = 'parametro='+valor; //almacenamos los parametros a enviar

         $.ajax({
             type: "GET", //El tipo (GET o POST)
             url:'data/archivo.php', //el archivo al cual pasaras los parametros
             data: dataString, //los parametros
             beforeSend: function () {
             //lo que quieras
             },
             success: function (response) {
             //lo que quieras
             }
         })

         alert(valor);

     });
});