#!/usr/bin/env python
from myapp import app
from helpers import set_up_test_app

set_up_test_app()

app.run(debug=True)
