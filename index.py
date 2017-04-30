from flask import Flask, request, send_from_directory
import utils

app = Flask(__name__)


@app.route('/<app_client>', methods=['GET'])
def index(app_client):
    image1 = request.args.get('image1')
    image2 = request.args.get('image2')
    method = request.args.get('method')
    width = request.args.get('width')
    height = request.args.get('height')
    try:
        directory, file = utils.get_or_create_file(
            app_client, image1, image2, method, width, height
        )
        return send_from_directory(directory, file)
    except Exception:
        return "KO"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
#    app.run(debug=True)
