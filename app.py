from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/proxy', methods=['GET'])
def proxy():
    # Get the URL parameter from the request
    url = request.args.get('url')
    if not url:
        return 'Please provide a URL parameter.', 400

    # Get the custom headers if any
    custom_headers = request.headers.get('Custom-Headers')
    headers = {}
    if custom_headers:
        headers = eval(custom_headers)

    try:
        # Send the request to the actual URL
        response = requests.get(url, headers=headers, stream=True)
        # Stream the content
        def generate():
            for chunk in response.iter_content(chunk_size=4096):
                yield chunk
        return Response(generate(), content_type=response.headers['Content-Type'])
    except Exception as e:
        return f'Error: {e}', 500
import os

if __name__ == '__main__':
    port  = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
