import sys
from importlib.metadata import distributions

print("Python version: ",sys.version)
for dist in sorted(distributions(), key=lambda x: x.metadata['Name'].lower()):
    name = dist.metadata['Name']
    version = dist.version
    print(f"{name}=={version}")
