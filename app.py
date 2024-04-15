from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/proxy', methods=['GET'])
def proxy():
    url = request.args.get('url')
    if not url:
        return 'Please provide a URL parameter.', 400

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Response(response.content, mimetype=response.headers['Content-Type'])
        else:
            return 'Error: Unable to fetch URL.', response.status_code
    except Exception as e:
        return f'Error: {e}', 500

if __name__ == '__main__':
    app.run(debug=True)