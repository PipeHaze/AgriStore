function initMap() {
  // your code like...
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: { lat: -33.448890, lng: -70.669265 }, // Santiago coordinates
  });
  
  // The marker, positioned at Santiago
  const marker = new google.maps.Marker({
    position: { lat: -33.448890, lng: -70.669265 },
    map: map,
  });

  // and other stuff...
  var directionsService = new google.maps.DirectionsService();

  //objeto de visualizacion en el mapa
  var directionsDisplay = new google.maps.DirectionsRenderer({
    map: map
  });

  // Datos del formulario
  var form = document.getElementById('route-form');
  var destinationInput = document.getElementById('destination');

  //controlador de eventos
  form.addEventListener('submit',function(event){
    event.preventDefault();

    //obtener el punto de destino
    var destination = destinationInput.value;

    //definir los parametros de la direccion
    var request = {
      origin: 'Mall Plaza Norte', 
      destination: destination,
      travelMode: 'DRIVING'
    };

    //enviar solicitud de la direccion
    directionsService.route(request, function(response, status){
      if (status === 'OK'){
        //mostrar ruta
        directionsDisplay.setDirections(response);
      }
    });
  });
}

$(document).ready(function() {
  initMap();
});