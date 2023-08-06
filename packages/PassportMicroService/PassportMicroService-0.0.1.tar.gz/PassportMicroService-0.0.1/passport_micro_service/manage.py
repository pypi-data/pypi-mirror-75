import sys
sys.path.append('.')

from app import create_app

app = create_app('dev')
app.run(debug=True, port=8000)
