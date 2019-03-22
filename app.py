from flask import Flask,request,jsonify
import json,os,io,traceback,sys
import codecs

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
@app.route('/reader',methods=['POST'])
def hello():
    try:
        if request.data:
            dat = request.data
            datum = io.BytesIO(dat)

            lists = []
            for x in datum:
                x = x.decode('utf-8')
                if 'ENTER' in x or 'EXIT' in x:
                    y = x.split(':')
                    detail = {}
                    detail["operation"] = y[0].replace('ENTER', 'ENTRY').split(']')[1]
                    detail["filename"] = y[1].strip()
                    detail["line_number"] = y[2].split(' ', 1)[0]
                    detail["name"] = "anonymous" if y[2].split(' ', 1)[1].strip() == "0" else y[2].split(' ', 1)[1].strip()
                    lists.append(detail.copy())

            if not lists:
                return not_found("Please Enter Logs File Only")
            else:
                results = {
                    "result": lists.copy()
                }

            return jsonify(results)
        else:
            return not_found('File is Empty')

    except Exception:
        traceback.print_exc()
        return not_found("Internal Server Error")

@app.errorhandler(400)
def not_found(msg):

    message = {
            'status': 400,
            'message': msg,
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp

app.run(host = '0.0.0.0',debug=True,threaded=True)