deploy = '''
from setux.lib.targets import Local

exported = Local(name='remote')
exported.modules.add({exported})
exported.deploy('{module}', {kwargs})
'''

script = '''
#!/bin/bash

cd {path}
python3 {name}
'''
