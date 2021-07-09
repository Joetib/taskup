from backend import app
from backend.tests import *

if __name__ == "__main__":
    import unittest
    unittest.main()
    app.run(debug=True)