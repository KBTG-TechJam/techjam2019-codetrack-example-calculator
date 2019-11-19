import os

from webapp.services import app

debug = bool(os.getenv('PRIVATE_DEBUG', ''))
app.run(host='0.0.0.0', port=8000, debug=debug)
