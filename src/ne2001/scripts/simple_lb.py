""" Simple calculations along a Galactic lb to 'infinite' distance
"""

import pdb

def parser(options=None):

    import argparse

    parser = argparse.ArgumentParser(description='Calculate quantities along a Galactic sightline v0.1')
    parser.add_argument("l", type=float, help="Galactic longitude (deg)")
    parser.add_argument("b", type=float, help="Galactic latitude (deg)")
    parser.add_argument("-d", type=float, default=100., help="Distance (kpc)")

    if options is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(options)
    return args


def main(pargs, unit_test=False, **kwargs):
    """ Run
    """
    from ne2001 import density
    from ne2001 import io as ne_io
    # init
    PARAMS = ne_io.read_params()
    ne = density.ElectronDensity(**PARAMS)

    # DM
    DM = ne.DM(pargs.l, pargs.b, pargs.d)
    print("----------------------------------------------")
    print("DM:")
    print("  Along l={:g} deg and b={:g} deg to d={:g} kpc".format(pargs.l, pargs.b, pargs.d))
    print("  DM = {:g} pc cm^-3".format(DM))
    print("----------------------------------------------")
    #


