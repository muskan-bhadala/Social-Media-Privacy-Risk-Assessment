import os, sys, tempfile
os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db"); os.environ["RATE_LIMIT"] = "100000"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
