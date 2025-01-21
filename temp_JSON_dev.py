# The following code is being used to test and develop connection between front-end and back-end
# Sean Doherty

import json
import time
import random
import cv2
import numpy as np
import requests

def updateJSON(): 
    while (1):
        file_path = "./user-interface/api/data.json"

        with open(file_path, "r") as file:
            data = json.load(file)

        # Step 2: Update the data
        random_n = random.randint(0, 2)
        locations = ['Hawaii', 'Jamaica', 'Scotland']
        data["location"] = locations[random_n]  # Add or update a key-value pair

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        print("JSON file updated successfully.")
    
        time.sleep(3)


def uploadRandomImage():
    
    while(1):
        try:
            image_url = f"https://picsum.photos/seed/{random.randint(1, 1000)}/800/600"
            # Fetch the image from the URL
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Convert the content to a NumPy array
            image_array = np.frombuffer(response.content, np.uint8)

            # Decode the image array into an image
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            save_path = './user-interface/src/components/images/img4.jpg'
            # Save the image locally
            cv2.imwrite(save_path, image)
            print(f"Image saved as {save_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(5)


# PROPOSED JSON STRUCTURE
    # {
    # location: string
    # pins: [
    #   {
    #       geo_coords: [lon, lat]
    #       imgRef: './img
    #       objects: [
    #           {
    #           pixel_coords: [x y]
    #           RGB_classifcation: string
    #           HS_classification: string
    #           distance: double
    #           } ...
    #       ]
    #   }
    # ]...
    # }



if __name__ == "__main__":
    uploadRandomImage()