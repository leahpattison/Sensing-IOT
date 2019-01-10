from flask import Flask, render_template, request, jsonify
from services import Analysis
import ipinfo


app = Flask(__name__)
# geo = pygeoip.GeoIP('GeoLiteCity.dat', pygeoip.MEMORY_CACHE)
def weather():
    access_token = '2cd79bed5b77a1'
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails()
    location = details.loc
    weather = Analysis.dark_sky_API((location))
    return weather

def predictPlay(t):
    model = Analysis.algorithm()
    data = t[0:7]
    description=t[-1]
    print(data)
    t = Analysis.regression(model, data)
    t = t[0]
    prediction = Analysis.spotifyRec(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], description)
    return prediction

@app.route('/')
def hello():
    ah="t"
    return render_template('index.html')


@app.route("/forward", methods=["GET", "POST"])
def move_forward():
    ah = weather()
    prediction = predictPlay(ah)
    print(type(prediction))
    lol = "lol"
    cloud = ah[0]
    wind = ah[1]
    temp = round((ah[2]-32)*5/9)
    humidity = ah[3]
    sum = ah[4]
    return render_template('index.html', cloud=cloud, wind=wind, temp=temp, humidity=humidity, sum=sum , lol=lol, prediction=prediction)

@app.route("/test/", methods = ["POST"])
def get_javascript_data():
    ah = weather()
    cloud = ah[0]
    wind = ah[1]
    temp = round((ah[2]-32)*5/9)
    humidity = ah[3]
    sum = ah[4]
    return render_template('index.html', cloud=cloud, wind=wind, temp=temp, humidity=humidity, sum=sum )

if __name__ == "__main__":
    app.run()