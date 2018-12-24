from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor

for key,value in Future.__dict__.items():
    if not key.startswith("__"):
        print("{}--->{}".format(key,value.__name__))

# _invoke_callbacks--->_invoke_callbacks
# cancel--->cancel
# cancelled--->cancelled
# running--->running
# done--->done
# _Future__get_result--->__get_result
# add_done_callback--->add_done_callback
# result--->result
# exception--->exception
# set_running_or_notify_cancel--->set_running_or_notify_cancel
# set_result--->set_result
# set_exception--->set_exception
print(20*"*")
for key,value in ThreadPoolExecutor.__dict__.items():
    if not key.startswith("__"):
        print("{}--->{}".format(key,value.__name__))

# _counter--->__next__
# submit--->submit
# _adjust_thread_count--->_adjust_thread_count
# shutdown--->shutdown