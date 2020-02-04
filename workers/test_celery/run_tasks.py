from __future__ import absolute_import
from .tasks import longtime_add, rise, test_a,test_b,test_c

from celery import chain, chord
import time

if __name__ == '__main__':
    # result = longtime_add.delay(1,2)
    # # at this time, our task is not finished, so it will return False
    # print ('Task finished? ', result.ready())
    # print ('Task result: ', result.result)
    # # sleep 10 seconds to ensure the task has been finished
    # time.sleep(10)
    # # now the task should be finished and ready method will return True
    # print ('Task finished? ', result.ready())
    # print ('Task result: ', result.result)
    #chord([ a1.s(1)  , a1.s(2) , a1.s(3)  ])(b1.s()).get()
    chord([ ( test_a.s(1) | test_b.s()) , ( test_c.s(2) | test_b.s()), ( test_a.s(3) | test_b.s())  ])(test_c.s()).get()
    #test(add=True)
    # res = chain(rise.s(10), longtime_add.s(2,8)).apply_async()
    # res.get()

def test(main=False, add=False, sumall=False, mul=False):
    taskid = some_test.delay(
        main,
        add,
        sumall,
        mul
    ).get()

    res = MfAsyncResult(taskid).get()

    print('Res is', res, 'type is: ', type(res))