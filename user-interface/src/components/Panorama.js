import React, {useState, useEffect} from 'react';
import '../styles/Panorama.css';


export function Panorama({panorama}) {

    // useEffect(() => {
    //     // Fetch the photo URL from the backend
    //     fetch("/api/photo") // Flask server URL
    //     .then((response) => {
    //     if (!response.ok) {
    //       throw new Error(`Failed to fetch image: ${response.statusText}`);
    //     }
    //     return response.blob();
    //   })
    //   .then((blob) => {
    //     const url = URL.createObjectURL(blob); // Create a URL for the image
    //     setPhotoUrl(url); // Update state with the image URL
    //   })
    //   .catch((error) => {
    //     console.error("Error fetching image:", error);
    //   });
    //   }, []);

    useEffect(()=> {
        console.log(panorama)
    }, [panorama])



    return (
        <div className='panorama-container'>
            {/* <button style={{fontSize: '30px', color: 'white'}} onClick={updateImageSrc}>Update Image</button> */}
            {panorama ? (
                <img src={panorama} className='panorama'/>
            ) : 
            <p style={{color: 'white', margin: '10px'}}>loading...</p>
        }
        </div>
    );
}
