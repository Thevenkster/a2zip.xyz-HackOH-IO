from flask import Flask
import config
from server.main import main

application = Flask(__name__)

# Register the blueprint
application.register_blueprint(main)

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    application.run(debug=False)
