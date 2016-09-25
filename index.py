from flask import Flask, request, send_from_directory
import utils

app = Flask(__name__)


@app.route('/<app_client>', methods=['GET'])
def index(app_client):
    file = request.args.get('file')
    modified_time = request.args.get('modified_time')
    size = request.args.get('size')
    method = request.args.get('method')
    if file:
        file = file[1:] if file[0] == "/" else file
    try:
        directory, file = utils.get_or_create_file(
            app_client, file, modified_time, size, method
        )
        return send_from_directory(directory, file)
    except Exception as e:
        print e
        return "KO"

if __name__ == '__main__':
    app.run(debug=True)