from replitdb import AsyncClient
import asyncio
import os

import replitdb._async as AsyncHandler
asyncio.run = AsyncHandler.run
class Client():
    def __init__(self,**args):
        self.client = AsyncClient(args.get('url',os.getenv('REPLIT_DB_URL')))
        self.args = args

    def __getitem__(self, key):
        return asyncio.run(self.client.view(key))

    def __setitem__(self, key, value):
        return asyncio.run(self.client.set_dict({key:value}))

    def __delitem__(self, key):
        return asyncio.run(self.client.remove(key))

    def __contains__(self, key):
        return key in self.keys()

    def __len__(self):
        return len(self.keys())

    def __repr__(self):
        x = asyncio.run(self.client.all_dict)
        print(x)
        exit()
        return repr(x)
    @property
    def _dict(self):
      return asyncio.run(self.client.all_dict)
    def __str__(self):
      return str(self._dict)
    def keys(self):
      return self._dict.keys()
    def values(self):
      return self._dict.values()
    def update(self,dict):
      return asyncio.run(self.client.set_dict(dict))
    def clear(self):
      return asyncio.run(self.client.wipe)
    def copy(self):
      return Client(*self.args)
    def get(self,get):
      return self._dict.get(get)
    def items(self):
      return self._dict.items()
    def pop(self,pop):
      return asyncio.run(self.client.remove(pop))
    def setdefault(self,key,val):
      if(key in self):
        return self[key]
      self[key] = val
      return val