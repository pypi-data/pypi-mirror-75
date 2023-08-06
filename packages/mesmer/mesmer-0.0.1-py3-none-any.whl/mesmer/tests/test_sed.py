def test_sed():
    import numpy as np
    from mesmer.seds import syncpl
    arr = syncpl(np.linspace(10, 100), 23., - 3.)
    arr += 1.
    return True
