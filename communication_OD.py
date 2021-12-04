from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

image = ""
result = ""
prediction = ""


@app.route('/')
def index():
    print("PATH: /")
    return "The connection is up!"


@app.route('/image', methods=['GET', 'PUT'])
def transmit_pose():
    global image
    if request.method == 'PUT':
        print("[/image]: client added image")
        image = request.data
    else:
        print("[/image]: server retrieved image")
    return image


@app.route('/result', methods=['GET', 'PUT'])
def transmit_frame():
    global result
    if request.method == 'PUT':
        print("[/result]: server put result")
        result = request.data
    else:
        print("[/result]: client get result")
    return result


@app.route('/prediction', methods=['GET', 'PUT'])
def transmit_prediction():
    global prediction
    if request.method == 'PUT':
        print("[/prediction]: server put prediction")
        prediction = request.data
    else:
        print("[/prediction]: client get prediction")
    return prediction


if __name__ == '__main__':
    # Fill in start
    # Change this to your IP address and port
    print("running")
    host_ip = '10.194.67.194'
    host_port = 20000
    socketio.run(app, host=host_ip, port=host_port)
    # Fill in end
