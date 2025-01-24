# The following code is being used to test and develop connection between front-end and back-end
# Sean Doherty

import json
import time
import random
import cv2
import numpy as np
import requests

def newPin():
    n = 4
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
            save_path = './user-interface/public/images/img' + str(n) + '.jpg'
            # Save the image locally
            cv2.imwrite(save_path, image)

            file_path = "./user-interface/api/data.json"

            with open(file_path, "r") as file:
                data = json.load(file)

            # Step 2: Update the data
            newData = {
                "coords": [55.880000, -4.300000+0.01*n],
                "imgRef": "./images/img" + str(n) + ".jpg"
            }
            data["pins"].append(newData)

            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)


            print("JSON file updated successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

        n += 1
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
    newPin()