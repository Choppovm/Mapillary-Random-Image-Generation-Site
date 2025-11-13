from flask import Flask, jsonify, render_template, request
import random
import requests

app = Flask(__name__)

token = "MAPILLARY TOKEN GOES HERE" # Mapillary token goes here

# bbox will be set by user drawing
currentBbox = None

# Function for getting random image from Mapillary
def getRandomimage():
    global currentBbox
    if not currentBbox:
        return {"error": "No bounding box selected. Please draw one on the map first."}

    url = "https://graph.mapillary.com/images"
    params = {
        "fields": "id,geometry",
        "bbox": ",".join(f"{v:.6f}" for v in currentBbox),
        "limit": 25, # Hard cap of 100
    }
    headers = {"Authorization": f"OAuth {token}"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json().get("data", [])
    except requests.exceptions.RequestException as e:
        # For Mapillary API errors, read it closely before immediately jumping to conclusions.
        # Check for logic errors in the code, too. You shouldn't need to change any file other than this one.
        # Always check their documentation and forums if you need extra help.
        return {"error": f"Mapillary API error: {e}"}

    if not data: # If no images found in the bounding box
        return {"error": "No images found in this bbox."}

    image = random.choice(data)
    try:
        thumbRESP = requests.get(
            f"https://graph.mapillary.com/{image['id']}",
            params={"fields": "thumb_1024_url"},
            headers=headers,
            timeout=15 # Time in seconds before stopping the program (i.e. if it gets stuck/can't find anything).
        )
        thumbRESP.raise_for_status()
        thumbURL = thumbRESP.json().get("thumb_1024_url")
    except requests.exceptions.RequestException as e:
        return {"error": f"Thumbnail fetch error: {e}"}

    return {
        "imageKey": image["id"],
        "lat": image["geometry"]["coordinates"][1],
        "lon": image["geometry"]["coordinates"][0],
        "thumbURL": thumbURL,
        "bboxUsed": currentBbox,
    }

# Do not touch; modify the function instead.
@app.route("/random.json")
def random_json():
    return jsonify(getRandomimage())

# Do not touch.
@app.route("/set_bbox", methods=["POST"])
def set_bbox():
    global currentBbox
    data = request.get_json(silent=True) or {}
    bbox = data.get("bbox")
    if bbox and len(bbox) == 4:
        currentBbox = tuple(float(v) for v in bbox)
        return jsonify({"bbox": currentBbox})
    return jsonify({"error": "Invalid bbox payload", "bbox": currentBbox})

# Do not touch; change templates/index.html or static/css/styles.css or static/js/main.js instead.
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
