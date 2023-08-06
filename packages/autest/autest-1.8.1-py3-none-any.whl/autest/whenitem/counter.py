from autest.api import AddWhenFunction
import hosts.output as host


def Counter(count_to: int):
    '''
    Will call this check the number of proved times then return True.

    Args:
        count_to: number of times to call function before returning true.

    '''
    initialState = {"counter" : 0}

    def up_to_count():
        initialState["counter"] += 1
        host.WriteDebug(["counter", "when"],
                        "updating count to {0}".format(initialState["counter"]))
        return initialState["counter"] >= count_to

    return up_to_count


AddWhenFunction(Counter, generator=True)
