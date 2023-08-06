import threading
import asyncio
asyncio._run = asyncio.run

class ResolveThread(threading.Thread):
            def __init__(self,result,func,*args,**kwargs):
                self.result= result
                self.func = func
                self.args = args
                self.kwargs = kwargs
                threading.Thread.__init__(self)
            def run(self):
                self.result[0] = asyncio.run(self.func)

def run(func):
  try:
    return asyncio._run(func)
  except RuntimeError:
    ret = [None]
    thread = ResolveThread(ret,func)
    thread.start()
    thread.join()
    return ret[0]
