from .shannon import Shannon
import logging

entropies = {

    'shannon': Shannon,

}


# ----------------------------------------------------------------------
def entropy(x, method='shannon', **kwargs):
    """"""

    ent = entropies.get(method, None)

    if ent is None:
        logging.error(
            f"'{method}' entropy is not available, select one from: {entropies.keys()}")
        return

    return ent(x, **kwargs)



