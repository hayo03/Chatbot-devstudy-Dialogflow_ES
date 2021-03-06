import json

from flask import request, jsonify, make_response
from flask import Flask
#from flask_cors import CORS
from flask import Response

app = Flask(__name__)
#CORS(app)

from api_manager import invoke_api


@app.route('/my_webhook', methods=['POST'])
def post_webhook_dialogflow():
    body = request.get_json(silent=True)
    session_id = body['session']
    intent = body['queryResult']['intent']['displayName']
    slots = []

    for key, value in body['queryResult']['parameters'].items():
        if len(str(value)) > 0:
            slots.append({'name':key,'value':value})
           
    print (slots)

    # msg = 'hi'
    msg = invoke_api(intent, slots)
    return answer_webhook(msg, session_id, intent)


def answer_webhook(msg, session_id, user_intent):
    message = {
        "fulfillmentText": msg,
        "fulfillmentMessages": [
            {
                "simpleResponses": {
                    "simpleResponses": [
                        {
                            "textToSpeech": msg,
                            "displayText": msg
                        }

                    ]
                }
            }
        ],
        # "source": "example.com",
        "outputContexts": [
            {
                "name": '{}/contexts/{}'.format(session_id, user_intent),
                "lifespanCount": 5,
            }]
    }
    return Response(json.dumps(message), 200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
