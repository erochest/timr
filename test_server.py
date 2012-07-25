

from flask import Flask, request

app = Flask(__name__)
app.debug = True


@app.route('/', methods=["GET", "POST"])
def dump():
    print('METHOD = {0}'.format(request.method))
    if request.method == 'POST':
        data = request.form
    elif request.method == 'GET':
        data = request.args
    data = sorted(data.items())
    for (key, value) in data:
        print('\t{0} = {1}'.format(key, repr(value)))
    return 'hi!'


if __name__ == '__main__':
    app.run()
