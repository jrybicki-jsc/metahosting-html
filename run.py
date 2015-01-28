#!/usr/bin/env python
from myapp import app
#from helpers import set_up_test_app

#set_up_test_app()

app.run(host='0.0.0.0', port=8080, debug=True)
