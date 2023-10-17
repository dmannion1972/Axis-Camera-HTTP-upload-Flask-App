import os
import http.server
import socketserver
import threading
from flask import Flask, render_template

# ----- HTTP Server to Receive Images -----

# Update the UPLOAD_DIR to be inside a static folder
UPLOAD_DIR = 'static/uploads'

# Create the directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ImageUploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        image_data = self.rfile.read(content_length)
        filename = os.path.join(UPLOAD_DIR, 'uploaded_image.jpg')
        
        with open(filename, 'wb') as img_file:
            img_file.write(image_data)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Image uploaded successfully')

server_address = ('0.0.0.0', 8000)

def run_http_server():
    with socketserver.TCPServer(server_address, ImageUploadHandler) as httpd:
        print('Server listening on port 8000...')
        httpd.serve_forever()

# ----- Flask App to Display Images -----

app = Flask(__name__)

@app.route('/')
def display_images():
    image_names = os.listdir(UPLOAD_DIR)
    return render_template('display.html', image_names=image_names)

def run_flask_app():
    app.run(host='0.0.0.0', port=8001)

# ----- Running Both Services Concurrently -----

if __name__ == '__main__':
    # Start HTTP server in a separate thread
    t1 = threading.Thread(target=run_http_server)
    t1.start()

    # Start Flask app in the main thread
    run_flask_app()
