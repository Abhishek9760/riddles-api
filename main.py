import json
import random
import os
from flask import Flask, request, jsonify
from glob import glob

app = Flask(__name__)

PER_PAGE = 10

files = [
    'adult riddles',
    'best riddles',
    'brain teasers riddles',
    'classic riddles',
    'difficult riddles',
    'easy riddles',
    'funny riddles',
    'good riddles',
    'jokes and riddles',
    'kids riddles',
    'logic puzzles',
    'math riddles',
    'medium riddles',
    'riddles',
    'short riddles',
    'video riddles',
    'what am i riddles',
    'what is it riddles',
    'who am i riddles',
    'who is it riddles',
]


def get_random_riddle(cat='riddles.json'):
    my_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(my_dir, cat)
    with open(json_file_path, 'r', encoding="cp866") as f:
        data = json.loads(f.read())
        return data[random.randint(0, len(data)-1)]


def get_list_msg():

    msg = ''
    for i in range(len(files)):
        file = files[i]
        msg += f"{i+1} - " + file + "\n"
    return msg


def message_formater(jmsg):
    msg = f'''  
*{jmsg['Heading'].strip()}* [ _{jmsg["id"]}_ ]

```{jmsg['Riddle'].strip()}```
'''
    return msg


@app.route("/cat", methods=["POST"])
def get_cat():
    msg = get_list_msg()
    return jsonify({
        "replies": [
            {
                "message": msg,
            },
        ]
    })


@app.route('/list', methods=["POST", "GET"])
def list_riddles():
    p_data = request.data
    msg = ''
    if p_data:
        cmd = json.loads(p_data)['query']['message']
        print(p_data)
        c = cmd.split()
        msg = ''
        if cmd == '/r':
            msg = message_formater(get_random_riddle())
        elif c[0] == "/r" and c[1].isnumeric():
            c = int(c[1])
            if (c in range(1, len(files) + 1)):
                file = files[c-1].replace(" ", "_") + '.json'
                r = get_random_riddle(file)
                msg = message_formater(r)
        return jsonify({
            "replies": [
                {
                    "message": msg,
                }
            ]
        })

    return jsonify(get_list_msg())


def get_answer(id_):
    with open("riddles.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
        for i in data:
            if i.get("id") == id_:
                return i


@app.route('/answer', methods=["POST"])
def send_answer():
    data = request.data
    cmd = json.loads(data)['query']['message']
    c = cmd.split()
    msg = ""
    if len(c) > 1 and c[0] == '/a' and c[1].isnumeric():
        ans = get_answer(int(c[1]))
        msg = ans["Answer"]
    return {
        "replies": [
            {"message": "*Answer*\n" + msg}
        ]
    }


@app.route('/')
def home():
    return get_random_riddle()


@app.route('/riddle')
def get_category():
    my_dir = os.path.dirname(__file__)
    data = request.args.get('q')
    page = request.args.get('page') or 1
    page = int(page)
    file_name = data + '.json'
    json_file_path = os.path.join(my_dir, file_name)
    result = []
    if (os.path.exists(json_file_path)):
        with open(json_file_path, 'r') as f:
            start, end = (page-1)*PER_PAGE,  PER_PAGE*page+1
            result = json.loads(f.read())[start:end]
    return json.dumps(result)
