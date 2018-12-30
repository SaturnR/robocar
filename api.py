#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response

from flask import Flask, jsonify, abort, make_response
from flask import request
from flask import url_for
import datetime
import timeout_decorator

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

#import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

from control import Car
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)

car = Car(pwm_frequency=150)



def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@auth.get_password
def get_password(username):
    if username == 'max':
        return 'max'
    return None

@auth.error_handler
def unauthorized():
    print('401 error')
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(400)
def not_found(error):
    print(error)
    return make_response(jsonify({'error':'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    print('not found')
    return make_response(jsonify({'error':'Not found'}), 404)

@app.errorhandler(423)
def locked_error(error):
    return make_response(jsonify({'error':'Device is locked'}), 423)

@app.errorhandler(500)
def internal_error(error):
    print('internal server error')
    return make_response(jsonify({'error':'Internal Error'}), 500)

'''
@app.errorhandler(444)  
def connection_error(error):
return make_response(jsonify({'error':"Connection refused"}), 444)
'''

@timeout_decorator.timeout(5, use_signals=False)
def send_command(config, duration):
    print('time out')
    return config.set_alarm_off_duration(duration)

@app.route('/video')
@auth.login_required
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),  mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/drive')
@auth.login_required
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/api/getstate', methods=['GET'])
@auth.login_required
def get_state():
    try:
        state = car.state
    except Exception as ex:
        abort(404)
    return jsonify({'Car State info': state})

@app.route('/api/car/forward', methods=['POST'])
@auth.login_required
def forward():
    try:
        data = request.json['data']
        print(data)
        duration = float(data['duration'])
        speed = int(data['speed'])
        print(duration, speed)
        
        responce = car.forward(duration, speed)
        state = responce
        
    except timeout_decorator.TimeoutError as tm:
       abort(423)
    except ConnectionRefusedError:
        abort(423)
    except Exception as ex:
        abort(500)
        
    return jsonify({'Car State info': state}), 201

@app.route('/api/car/backward', methods=['POST'])
@auth.login_required
def backward():
    
    try:
        data = request.json['data']
        duration = float(data['duration'])
        speed = int(data['speed'])
        print(duration, speed)
        responce = car.backward(duration, speed)
        state = responce
        
    except timeout_decorator.TimeoutError as tm:
       abort(423)
    except ConnectionRefusedError:
        abort(423)
    except Exception as ex:
        abort(500)

    return jsonify({'Car State info': state}), 201

@app.route('/api/car/turn', methods=['POST'])
@auth.login_required
def turn():
    
    try:
        data = request.json['data']
        degree = float(data['degree'])
        responce = car.turn_lr(degree)
        print('left right =========<', degree)
        state = responce
        if responce == -1:
            abort(404)
    except timeout_decorator.TimeoutError as tm:
       abort(423)
    except ConnectionRefusedError:
        abort(423)
    #except Exception as ex:
    #    abort(500)
        
    return jsonify({'Car State info': state}), 201

@app.route('/api/car/cam_position', methods=['POST'])
@auth.login_required
def cam_position():
    
    try:
        data = request.json['data']
        position = int(data['position'])
        responce = car.camera_position(position)
        print('cam position  =========', position)
        state = responce
        if responce == -1:
            abort(404)
    except timeout_decorator.TimeoutError as tm:
       abort(423)
    except ConnectionRefusedError:
        abort(423)
    #except Exception as ex:
    #    raise ex #abort(500)
        
    return jsonify({'Car State info': state}), 201


@app.route('/api/set/<int:car_id>', methods=['POST'])
@auth.login_required
def set_state(car_id):
    received = False
    
    try:
        print(request)
        data = request.json['data']
        print(data)
        received = True
    except timeout_decorator.TimeoutError as tm:
       abort(423)
    except ConnectionRefusedError:
        abort(423)
    except Exception as ex:
        abort(500)

    return jsonify({'Data': {'car_id':car_id, 'received':received} }), 201


if __name__ == "__main__":
    car = Car(pwm_frequency=150)
    app.run(host='0.0.0.0', port=8080, ssl_context=('cert.crt', 'cert.key'), debug=True)
