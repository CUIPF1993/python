async def func(x,y):
    return x + y

f = func(3,4)
print(f)
"""
<coroutine object func at 0x000002973EC34410>
sys:1: RuntimeWarning: coroutine 'func' was never awaited"""