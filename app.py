from flask import Flask,request,jsonify,abort
import json,os
import codecs


app = Flask(__name__)

@app.route('/reader',methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        dat = request.data

        modat = dat.decode('utf-8')
        try:
            with codecs.open('file.txt', 'w+', encoding='utf8') as f:
                f.write(modat)
        except:
            return not_found

        f = open("file.txt", "r")

        lists = []
        for x in f:
            if 'ENTER' in x or 'EXIT' in x:
                y = x.split(':')
                detail = {}
                detail["operation"] = y[0].replace('ENTER', 'ENTRY').split(']')[1]
                detail["filename"] = y[1].strip()
                detail["line_number"] = y[2].split(' ', 1)[0]
                detail["name"] = "Anonymous" if y[2].split(' ', 1)[1].strip() == "0" else y[2].split(' ', 1)[1].strip()
                lists.append(detail)
        results = {
            "result": lists
        }
        jsonStr = json.dumps(results, indent=2, sort_keys=True)

        os.remove("file.txt")
        return jsonStr

    else:
        return not_found()

@app.errorhandler(400)
def not_found(error=None):
    message = {
            'status': 400,
            'message': 'POST is Required',
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


app.run(debug=True)