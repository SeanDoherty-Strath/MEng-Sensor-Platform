
import json
import time
import random

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

if __name__ == "__main__":
    updateJSON()