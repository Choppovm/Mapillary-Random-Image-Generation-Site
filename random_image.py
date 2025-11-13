import random
import requests
token = "MAPILLARY TOKEN GOES HERE"
def getRandomImage():
    bbox = (0, 0, 0, 0)
    url = "https://graph.mapillary.com/images"
    params = {
        "fields": "id,geometry",
        "bbox": ",".join(map(str, bbox)),
        "limit": 25,
    }
    headers = {"Authorization": f"OAuth {token}"}
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()["data"]
    if not data:
        raise RuntimeError("No images found in given bounding box")
    image = random.choice(data)
    return {
        "image_key": image["id"],
        "lat": image["geometry"]["coordinates"][1],
        "lon": image["geometry"]["coordinates"][0],
    }
print(getRandomImage())