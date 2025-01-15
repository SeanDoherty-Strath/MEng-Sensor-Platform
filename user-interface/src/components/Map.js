import React, {useState, useEffect} from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, useMapEvents } from "react-leaflet";
import '../styles/Map.css';
import 'leaflet/dist/leaflet.css';
import L from "leaflet";

// Update Map Coordinates
const UpdateMapCenter = ({ newCenter }) => {
    const map = useMap();
    map.setView(newCenter);
};

// Add a new pin
const AddPinOnClick = ({pins, setPins }) => {
    useMapEvents({
      click(e) {
        const { lat, lng } = e.latlng; // Get latitude and longitude of the click
        setPins((pins) => [
          ...pins,
          { id: Date.now(), coords: [lat, lng], img: ''},
        ]);
      },
    });
  };



export function Map({setPanorama}) {
    
    const [mapCenter, setMapCenter] = useState([51.505, -0.09]) // default to London
    const [pins, setPins] = useState([{ id: 1, coords: [55.86, -4.32], img: require("../assets/panoramas/panorama.png") }, { id: 2, coords: [55.86, -4.34], img: require("./images/img2.jpg")}, { id: 3, coords: [55.86, -4.36], img: require("./images/img3.jpg")}]);

    // periodically search for new pins
    // const searchNewPins = async () => {

    //   try {

    //     const response = await fetch('../assets/analysis/example.json');
    //     console.log(response)
    //     console.log(j)

    //     if (!response.ok) {
    //       throw new Error(`HTTP error! status: ${response.status}`);
    //     }
    //     const data = await response.json();
    //     console.log("JSON Contents:", data);
    //     // return data;
    //   } catch (err) {
    //     console.log(err)
    //   }
    // }

    // useEffect(() => {
    //   // Define the function to run every 5 seconds
    //   const asyncintervalId = setInterval(() => {
    //     searchNewPins();
    //   }, 5000);
  
    //   // Cleanup interval when the component unmounts
    //   return () => {
    //     clearInterval(asyncintervalId);
    //   };
    // }, []);

    useEffect(() => {
    // Fetching the JSON file containing the image data
      fetch('../assets/analysis/analysis.json')
        .then(resp => console.log(resp))
        // .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error loading JSON:', error));
    }, []);




    // Set co-ords to users location
    useEffect(()=> {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(      
              (position) => {
                const { latitude, longitude } = position.coords;
                setMapCenter([latitude, longitude]);
              },
              (err) => {
                console.log(err);
              }
            );
          }
    }, [])      


    const handlePinClick = (pin) => {
      setPanorama(pin.img)
    };
  
    
    return (
   
      <MapContainer
          className='map'
          center={mapCenter} // Latitude and Longitude (e.g., London)
          zoom={15} // Zoom level
          >
          

          <TileLayer
              url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
              attribution='&copy; <a href="https://carto.com/">CARTO</a>'
          />
          {pins.map((pin) => (
                  <Marker key={pin.id} position={pin.coords} icon={customIcon} eventHandlers={{
                    click: () => handlePinClick(pin),
                  }}>
                  <Popup>
                      <strong>{pin.name}</strong> <br /> Coordinates:{" "}
                      {pin.coords.join(", ")}
                  </Popup>
                  </Marker>
              ))}
          <UpdateMapCenter newCenter={mapCenter} />
          <AddPinOnClick pins={pins} setPins={setPins} />
      </MapContainer>

    );
}

const customIcon = L.divIcon({
    className: "emoji-icon", // Optional CSS for further styling
    html: '<span style="font-size: 30px;">📍</span>', // Adjust the font-size
});