import asyncio
import functools

# every coroutine


async def coromask(coro, args, kwargs, fargs):
    """
    A coroutine that mask another coroutine  callback with args, and a
    function callbacks who manage input/output of corotine callback

    :param coro: is a coroutine object defined by the developer
    :param args: the list of arguments to run on the corotine *coro*
    :param fargs: the function that process the input and create an output related with the coro result

    :returns: a result, is a list of the elements for future argument
    """
    try:
        _in = args
        msg = ("Coromask args %s, kwargs %s, in coro %s" %
               (args, kwargs, coro))
        obtained = await coro(*args, **kwargs)
        if isinstance(obtained, Exception):
            raise Exception()
        else:
            result = fargs(_in, obtained)
            return result
    except Exception:
        raise Exception(msg)


def renew(task, coro, fargs, *args, **kwargs):
    """
    A simple function who manages the scheduled task and set the
    renew of the task

    :param task: is a Future initialized coroutine but not executed yet
    :param coro: is the corutine to renew when the first is finished
    :param fargs: the function to process input/output
    :param args: the unpacked list of extra arguments
    """
    if not task.cancelled():
        try:
            result = task.result()
            result_args, result_kwargs = result
            loop = asyncio.get_event_loop()
            task = loop.create_task(
                coromask(coro, result_args, result_kwargs, fargs))
            task.add_done_callback(functools.partial(renew, task, coro, fargs))
        except asyncio.InvalidStateError as ie:
            print("Invalid State Error", ie,
                  "Coro", coro,
                  "args", args,
                  "kargs", kwargs)
            raise ie
        except Exception as e:
            print("Resultado", result, task, coro, fargs)
            print("Excepcion en renew", e)
            raise e
    else:
        try:
            loop = task.get_loop()
            loop.stop()
            return False
        except Exception as e:
            raise e


def simple_fargs(_in, obtained):
    """
    Simple function who can be used in callback on coromask, the
    inputs are /_in/ and /obtained/ value from the coroutine executed.
    Return _in

    :_in: the input list
    :param obtained: the object that came from the result of coroutine execution

    :returns: _in
    """
    return _in


def simple_fargs_out(_in, obtained):
    """
    Simple function who can be used in callback on coromask, the
    inputs are /_in/ and /obtained/ value from the coroutine executed.
    Return obtained

    :param _in: the input list
    :param obtained: the object that came from the result of coroutine execution

    :returns: obtained
    """
    return obtained
