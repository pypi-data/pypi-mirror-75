def test_fmatrix():
    import numpy as np
    from mesmer.seds import FMatrix

    freqs = np.logspace(1, 3, 100)
    components = ["cmb", "syncpl", "dustmbb"]
    fmatrix = FMatrix(components)

    parameters = {
        "nu": freqs,
        "nu_ref_d": 353.0,
        "nu_ref_s": 23.0,
        "beta_d": 1.5,
        "beta_s": -3.0,
        "T_d": 20.0,
    }

    output1 = fmatrix(**parameters)

    assert output1.shape == (len(components), len(freqs))

    parameters.pop("nu")
    # Check that the same answer is achieved by calling FMatrix
    # in a different way.
    output2 = fmatrix(nu=freqs, **parameters)
    np.testing.assert_array_equal(output1, output2)
    return
