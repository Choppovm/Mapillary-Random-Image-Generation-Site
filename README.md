# Mapillary Random Image Generation Site
## Overview
NOTE: THIS REPOSITORY REQUIRES MANUAL DOWNLOADING + SETUP TO WORK.

This repo contains two main features:
1. A python flask server (app.py) that generates you a random image from Mapillary based on the bounding box you draw.
2. A python script (random_image.py) that prints the image id and coordinates of a random image based off a bounding box defined in the script.

Both scripts (and various other files relating to the scripts) need setting up in order to work. Details for each part are given below.

<details>
<summary><h2>Command-Line Image Generator | Using random_image.py</h2></summary>

### Setting Up
You'll need to set up two things before using the command-line image generator:

#### 1. Mapillary API key

1. Head to the [Mapillary Website](https://www.mapillary.com/).
2. From there, go to Developers --> Build with Mapillary (see [here](https://www.mapillary.com/developer)).
3. Click "Get an access token", which should bring you [here](https://www.mapillary.com/dashboard/developers). 
4. Register your application. Follow the criteria below:
    1. Give the app permission to read.
5. View the "Access Token". This should look something like `MLY|###|###`.
6. Copy this, and replace the token variable on line 5 with that access token.

#### 2. Bounding Box
1. Head to any bounding box finder site.
    1. Something like http://bboxfinder.com will work for this example.
2. Draw your bounding box.
    1. **THE AREA OF THE BOUNDING BOX MUST STAY BELOW 0.01 SQUARE DEGREES.**
    2. Mapillary changed their API to enforce this limit. There is no work around.
    3. Yes, it's very annoying. Yes, it's extremely inconvenient considering how small this is. No, there's nothing we can do about this. 
3. Copy the bounding box generated.
    1. If you're using http://bboxfinder.com, this will be the `Box` value.
4. Replace the bbox variable's value in line 8 with this bounding box. Do not remove the brackets, paste the numbers inside them.
    
### Additional Modifications
random_image.py has a few extra modifications that can be made to it. These are as follows:

- Line 15: "limit" parameter
    - This is the number of images Mapillary will get every time the script is ran.
    - There is a hard cap of 100 on this. Don't go above it, as it'll cause an error.
    - Currently set to 25, meaning it'll get a list of 25 image IDs from the bounding box (unless there's less than 25 images in the box).

### Python Script Usage
Once you've completed the setup, that's all you really need to do. You can just run the script, and it should print the image ID and coordinates of the image.

Always keep the API's rate limit in mind when using. 
</details>

<details>
<summary><h2>Python Flask Web Server | Using app.py</h2></summary>

### Setting Up
You'll need to set up your **Mapillary access token** before using the flask web app:

1. Head to the [Mapillary Website](https://www.mapillary.com/).
2. From there, go to Developers --> Build with Mapillary (see [here](https://www.mapillary.com/developer)).
3. Click "Get an access token", which should bring you [here](https://www.mapillary.com/dashboard/developers). 
4. Register your application. Follow the criteria below:
    1. Give the app permission to read.
5. View the "Access Token". This should look something like `MLY|###|###`.
6. Copy this, and replace the token variable on line 7 with that access token.

### Additional Modifications
app.py has a few extra modifications that can be made to it. These are as follows:

- Line 22: "limit" parameter
    - This is the number of images Mapillary will get every time the script is ran.
    - There is a hard cap of 100 on this. Don't go above it, as it'll cause an error.
    - Currently set to 25, meaning it'll get a list of 25 image IDs from the bounding box (unless there's less than 25 images in the box).
- Line 45: "timeout" request setting
    - The time (in seconds) before the request to Mapillary's API is terminated.
    - This is in place to prevent situations involving infinite loops (such as not finding any images, an error taking place in the code and hence breaking the website, etcetera).
    - There's no official limit on this, but I'd keep it at 15 personally. Using 30 seconds as a general maximum to avoid wasting time is a good idea.
    - Obviously don't set this to something below 10 seconds. Mapillary's API is often slow, and it takes time for the image to be gathered. Setting too short of a limit won't give Mapillary time to even return the image.

### Python Script Usage
Run the script, and wait. The time it takes for the web server to launch depends on your device's strength; lower-ended devices may take a few moments to launch the server, while stronger devices might launch it instantly.

When it's ready, go to the URL it provides. This url should be http://127.0.0.1:5000. 
- If the port or IP address seems different, you may be running a different script.
- If you're running another flask server on the same port (5000), this website might not work, or the previously running website might break. Consider changing the port if this is the case.

When on the site, draw the bounding box, submit it, THEN generate the mapillary image. The image will be displayed below.
</details>
