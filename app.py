from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

@app.route("/",methods=['POST'])
def hello():
    data = request.get_json()
   
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    # print(final_amount)
    return jsonify(response)

def fetch_conversion_factor(source,target):
    
    url = "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=62fa1e8b70dd1821a9fb".format(source,target)

    response = requests.get(url)
    response = response.json()

    return response['{}_{}'.format(source,target)]    


app.run(debug=True)
