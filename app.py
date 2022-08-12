# -*- coding: utf-8 -*-
from queue import PriorityQueue
from flask import Flask, render_template, request, Response, url_for, send_from_directory, redirect, jsonify
import json
import os
# from flask_cors import CORS

app = Flask(__name__)
# 解决跨域问题
# CORS(app, origins="*")
app.secret_key = 'app2app'  # 最好要指定这个参数

with open("./dbs/chinese.json", "r", encoding="utf-8") as c, open("./dbs/person.json", "r", encoding="utf-8") as p, open("./dbs/readMethod.json", "r", encoding="utf-8") as r,open("./dbs/ssml.xml", "r", encoding="utf-8") as s:
    chinese=json.load(c)
    person=json.load(p)
    readMethod=json.load(r)
    xml=s.read()


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/splitText", methods=['POST'])
def splitText():
    text = request.json["text"].splitlines()
    while "" in text:
        text.remove("")
    req={"text":text,"chinese":chinese,"person":person,"readMethod":readMethod}
    return jsonify(req)

@app.route("/idssml", methods=['POST'])
def idssml():
    text = request.json["text"]
    boJiangYuan = request.json["boJiangYuan"]
    yuQi = request.json["yuQi"]
    suDu = request.json["suDu"]
    shengDiao = request.json["shengDiao"]
    tingDun= request.json["tingDun"]
    # print(request.json)
    ssml=xml.replace("{name}",boJiangYuan)
    ssml=ssml.replace("{style}",yuQi)
    ssml=ssml.replace("{rate}",suDu)
    ssml=ssml.replace("{pitch}",shengDiao)
    ssml=ssml.replace("{text}",text)
    if tingDun=="0":
        ssml=ssml.replace("{tingdun}","")
    else:
        ssml=ssml.replace("{tingdun}",f'<break time="{tingDun}s"/>')
    return jsonify(ssml)

@app.route("/allssml", methods=['POST'])
def allssml():
    text = request.json["text"]
    boJiangYuan = request.json["boJiangYuan"]
    yuQi = request.json["yuQi"]
    suDu = request.json["suDu"]
    shengDiao = request.json["shengDiao"]
    tingDun= request.json["tingDun"]
    # print(request.json)
    allssml=""
    for i,_ in enumerate(text):
        ssml=xml.replace("{name}",boJiangYuan[i])
        ssml=ssml.replace("{style}",yuQi[i])
        ssml=ssml.replace("{rate}",suDu[i])
        ssml=ssml.replace("{pitch}",shengDiao[i])
        ssml=ssml.replace("{text}",text[i])
        if tingDun[i]=="0":
            ssml=ssml.replace("{tingdun}","")
        else:
            ssml=ssml.replace("{tingdun}",f'<break time="{tingDun[i]}s"/>')
        allssml=allssml+ssml+"\n"
    
    return jsonify(allssml)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(port=5000, debug=False)
