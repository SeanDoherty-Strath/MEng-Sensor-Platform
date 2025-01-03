import './App.css';
import React, {useState, useEffect} from 'react';
import { Map } from './components/Map.js';
import { Panorama } from './components/Panorama.js';

function App() {
  
  const [panorama, setPanorama] = useState(null);

  // useEffect(()=> {
  //   fetch("/api/route")
  //   .then(res => res.json())
  //   .then(data => {setAccuracy(data.accuracy)})
  // })

  // TO DO: Implelement this
  // useEffect(() => {
  //   // Define query parameters
  //   const params = new URLSearchParams({
  //     param1: 'value1',
  //     param2: 'value2',
  //   });

  //   fetch(`/api/route?${params.toString()}`)
  //     .then(res => res.json())
  //     .then(data => setAccuracy(data.accuracy))
  //     .catch(err => console.error("Error fetching data:", err));
  // }, []);  // Add dependencies if needed

  return (
  
    <div className='container'>
      <div className='header'>
        <h1>HYPERBOT</h1>
      </div>
      <div className='body'>
        <div className='map-container'>
          <Map setPanorama={setPanorama}/>
        </div>

        <div className='panoramic-container'>
          <Panorama panorama={panorama}/>
        </div>

      </div>
    </div>
  );
}

export default App;
