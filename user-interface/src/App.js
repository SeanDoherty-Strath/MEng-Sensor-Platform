import './App.css';
import React, {useState, useEffect} from 'react';
import { Map } from './components/Map.js';
import { Panorama } from './components/Panorama.js';

function App() {
  
  const [panorama, setPanorama] = useState();
  const [locationName, setLocationName] = useState('unnamed location')
  const [pins, setPins] = useState([])
  
  const refreshData = () => {
    fetch("/getData").then(
      res => res.json()
    ).then(
      data => {
        setLocationName(data.location)
        setPins(data.pins)
        console.log(data)
      }
    )
  }

  useEffect(()=> {
    const interval = setInterval(() => {
      refreshData();
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
          <Map setPanorama={setPanorama} pins={pins} setPins={setPins}/>
        </div>

        <div className='panoramic-container'>
          <Panorama panorama={panorama} locationName={locationName} setLocationName={setLocationName}/>
        </div>

      </div>
    </div>
  );
}

export default App;
