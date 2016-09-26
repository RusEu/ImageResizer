from flask import Flask, request, send_from_directory
import utils

app = Flask(__name__)


@app.route('/<app_client>', methods=['GET'])
def index(app_client):
    file = request.args.get('file')
    size = request.args.get('size')
    method = request.args.get('method')
    try:
        directory, file = utils.get_or_create_file(
            app_client, file, size, method
        )
        return send_from_directory(directory, file)
    except Exception as e:
        print e
        return "KO"

if __name__ == '__main__':
    app.run(debug=True)