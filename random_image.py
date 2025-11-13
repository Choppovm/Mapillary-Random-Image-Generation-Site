# Imports (random and requests required (do not touch))
import random
import requests

token = "MAPILLARY TOKEN GOES HERE" # Mapillary token goes here

def getRandomImage():
    bbox = (0, 0, 0, 0) # Bounding box goes here
    
    # Do not touch
    url = "https://graph.mapillary.com/images"
    params = {
        "fields": "id,geometry",
        "bbox": ",".join(map(str, bbox)),
        "limit": 25, # Hard cap 100
    }
    headers = {"Authorization": f"OAuth {token}"}
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()["data"]

    # If no images found within given bounding box...
    if not data:
        raise RuntimeError("No images found in given bounding box")
    
    # Return a random image from list of images found
    image = random.choice(data)
    return {
        "image_key": image["id"],
        "lat": image["geometry"]["coordinates"][1],
        "lon": image["geometry"]["coordinates"][0],
    }

print(getRandomImage())