import os
import sys
from flask_marshmallow import Marshmallow

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from api.api import app

ma = Marshmallow(app)
import_data = {}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
