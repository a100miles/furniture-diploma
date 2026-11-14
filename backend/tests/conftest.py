import os

# Tests use the fixed 25-item demo catalog so expectations do not change when
# the parsed store data is refreshed.
os.environ["CATALOG"] = "demo"
