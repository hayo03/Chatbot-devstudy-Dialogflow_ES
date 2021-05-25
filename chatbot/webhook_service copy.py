import json

from flask import request, jsonify, make_response
from flask import Flask
from flask_cors import CORS
from flask import Response

app = Flask(__name__)
CORS(app)

from api_manager import invoke_api


@app.route('/my_webhook', methods=['POST'])
def post_webhook_dialogflow():
    body = request.get_json(silent=True)
    session_id = body['detect_intent_response_id.response_id']
    intent = body['intent_info']['display_name']
    slots = []

    for key, value in body['intent_info']['parameters'].items():
        if len(str(value)) > 0:
            slots.append({'name':key,'value':value})
           
    print (slots)

    # msg = 'hi'
    msg = invoke_api(intent, slots)
    return answer_webhook(msg, session_id, intent)


def answer_webhook(msg, session_id, user_intent):
    message={"fulfillment_response":
             {"messages":[msg]}
    }
 
    return Response(json.dumps(message), 200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)