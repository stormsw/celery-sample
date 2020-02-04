from __future__ import absolute_import
from .app import app
from celery import Task
from celery.result import AsyncResult 
import time

class CeleryException(Exception):
    task_id = None
    task_name = None

    def __init__(self, task_id, task_name, exc):
        self.task_id = task_id
        self.task_name = task_name
        self.exc = exc

    def __str__(self):
        return 'Exception raised in celery taskId: ' + \
            self.task_id + '. TaskName: ' + self.task_name + '.' \
            'Exception: ' + str(self.exc)


class MfTask(Task):
    def __call__(self, *args, **kwargs):
        # If an error has been raised from a previous task, pass down the error
        for arg in args:
            # Need to handle list of chord
            if type(arg) is list:
                for el in arg:
                    if type(el) is CeleryException:
                        return el

            if type(arg) is CeleryException:
                return arg

        try:
            return Task.__call__(self, *args, **kwargs)
        except Exception as e:
            return CeleryException(self.request.id, self.name, e)


class MfAsyncResult(AsyncResult):
    def get(self, *args):
        res = AsyncResult.get(self, args)

        if type(res) is CeleryException:
            raise res

        return res

@app.task(name='tasks.longtime_add')
def longtime_add(x, y):
    print ('long time task begins')
    # sleep 5 seconds
    time.sleep(5)
    print('long time task finished')
    return x + y

@app.task(name='tasks.rise')
def rise(x):
    time.sleep(x)
    raise Exception("error")

@app.task(base=MfTask)
def add(x, y, failes):
    if failes:
        raise Exception('Failing in add')
    return x + y

@app.task
def test_a(arg):
    print('Task A1, starring with arg:' + str(arg))
    if arg == 3:
        raise Exception('A1 Error')
    time.sleep(5)
    print('A1 done')
    return {'a1': True}

@app.task
def test_b(arg):
    print('Task A2, starring with arg:' + str(arg))
    time.sleep(5)
    print('A2 done')
    return {'a2': True}

@app.task
def test_c(arg):
    print('Task B1, starring with arg:' + str(arg))
    time.sleep(5)
    print('B1 done')
    return {'b1': True}

@app.task(base=MfTask)
def mul(x, y, failes):
    if failes:
        raise Exception('Failing in mul')
    return x * y


@app.task(base=MfTask)
def sumall(v, failes):
    if failes:
        raise Exception('Failing in sumall')
    return sum(v)


@app.task(base=MfTask)
def some_test(main_f, add_f, sumall_f, mul_f):
    nbs = [1, 2, 3, 4]

    add_chord = chord(
        (add.s(nb, 1, add_f) for nb in nbs),
        sumall.s(sumall_f)
    )

    add_async = chain(
        add_chord, mul.s(2, mul_f)).apply_async()

    if main_f:
        raise Exception('Failing in some_test')

    return add_async.task_id


