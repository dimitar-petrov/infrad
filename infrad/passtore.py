import yaml
import re
from passpy.store import Store

class PassStore:
   def __init__(self):
       self._store = Store()

   def getkey(self, fileregex, key):
       files = self._store.find(fileregex)
       if len(files) == 1:
           contents = self._store.get_key(files[0])
           filtered = list(filter(lambda x: not re.match(r'^\s*$|^#.*$', x), contents.splitlines()))

           if key == "pass":
               return filtered[0]
           else:
               mapping = yaml.safe_load('\n'.join(filtered[1:]))
               return mapping.get(key)
