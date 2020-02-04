from __future__ import absolute_import
from .app import app
import time


@app.task(name='tasks.longtime_add')
def longtime_add(x, y):
    print ('long time task begins')
    # sleep 5 seconds
    time.sleep(5)
    print('long time task finished')
    return x + y