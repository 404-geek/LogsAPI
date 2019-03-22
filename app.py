from flask import Flask,request,jsonify
import json,os
import codecs


app = Flask(__name__)
@app.route('/reader',methods=['POST'])
def hello():
    try:
        if request.data:
            dat = request.data
            modat = dat.decode('utf-8')
            flag = False
            try:
                with codecs.open('file.txt', 'w+', encoding='utf8') as f:
                    f.write(modat)
                    flag = True
            except:
                print("Error in Saving the file")
        else:
            return not_found("File is Required in Body")

        if flag == True and os.stat("file.txt").st_size != 0:
            f = open("file.txt", "r")

            lists = []
            for x in f:
                if 'ENTER' in x or 'EXIT' in x:
                    y = x.split(':')
                    detail = {}
                    detail["operation"] = y[0].replace('ENTER', 'ENTRY').split(']')[1]
                    detail["filename"] = y[1].strip()
                    detail["line_number"] = y[2].split(' ', 1)[0]
                    detail["name"] = "anonymous" if y[2].split(' ', 1)[1].strip() == "0" else y[2].split(' ', 1)[1].strip()
                    lists.append(detail.copy())

            if not lists:
                os.remove("file.txt")
                return not_found("Please Enter Logs File Only")
            else:
                results = {
                    "result": lists.copy()
                }

            os.remove("file.txt")
            return jsonify(results)
        else:
            os.remove("file.txt")
            return not_found('File is Empty')
    except:
        return not_found("plain/text only supported")

@app.errorhandler(400)
def not_found(msg):

    message = {
            'status': 400,
            'message': msg,
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


app.run(debug=True,threaded=True)