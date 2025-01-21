import './App.css';
import React, {useState, useEffect} from 'react';
import { Map } from './components/Map.js';
import { Panorama } from './components/Panorama.js';

function App() {
  
  const [panorama, setPanorama] = useState(require('./components/images/img2.jpg'));
  // const [panorama, setPanorama] = useState(null);
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

  const [locationName, setLocationName] = useState('unnamed location')
  // const searchNewPins = async () => {

  //     try {

  //       const response = await fetch('SensorPlatformAnalysis.json');
  //       if (!response.ok) {
  //         throw new Error(`HTTP error! status: ${response.status}`);
  //       }
  //       const data = await response.json();
  //       setLocationName(data.location_name)
  //     } catch (err) {
  //       console.log(err)
  //     }
  // }

  const searchNewPins = () => {
    fetch("/getData").then(
      res => res.json()
    ).then(
      data => {
        setLocationName(data.location)
        console.log(data)
      }
    )
  }

  useEffect(()=> {
    const interval = setInterval(() => {
      searchNewPins();
    }, 3000);

    // Cleanup the interval on component unmount
    return () => clearInterval(interval);

    }, [])

  return (
  
    <div className='container'>
      {/* <button onClick={searchNewPins}>Press me biatch</button> */}
      <div className='header'>
        <div className='search'>
          <button>{'<'}</button>
          <button>{'>'}</button>
          <input placeholder='Search...'/> 
          <button>{'↵'}</button>
        </div>
        <h1>Hyperbot</h1>
        
      </div>
      <div className='body'>
        <div className='map-container'>
          <Map setPanorama={setPanorama}/>
        </div>

        <div className='panoramic-container'>
          <Panorama panorama={panorama} locationName={locationName} setLocationName={setLocationName}/>
        </div>

      </div>
    </div>
  );
}

export default App;
