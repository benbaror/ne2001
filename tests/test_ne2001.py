
import os

import numpy as np
from click.testing import CliRunner
from numpy.random import rand
from numpy.random import randint

from ne2001 import density
from ne2001.cli import main

PARAMS = density.PARAMS
r_sun = 8.5

def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output == '()\n'
    assert result.exit_code == 0


def test_density():
    xyz = (1-2*rand(3, 100)) * 20

    ne_disk1 = density.NEobject(xyz, density.thick_disk, r_sun=r_sun,
                                **PARAMS['thick_disk']).ne
    assert len(ne_disk1) == 100
    assert all(ne_disk1 >= 0)

    ne_disk2 = density.NEobject(xyz, density.thin_disk,
                                **PARAMS['thin_disk']).ne
    assert len(ne_disk2) == 100
    assert all(ne_disk2 >= 0)

    ne_gc = density.NEobject(xyz, density.gc, **PARAMS['galactic_center']).ne
    assert len(ne_gc) == 100
    assert all(ne_gc >= 0)


def test_geometry():
    ellipsoid = rand(3)*20
    xyz = (1-2*rand(3, 100)) * 20
    theta = rand()*2*np.pi
    center = rand(3)*20
    assert density.in_ellipsoid(center, center, ellipsoid, theta)
    assert len(density.in_ellipsoid(xyz, center, ellipsoid, theta)) == 100

    cylinder = rand(3)*20
    xyz = (1-2*rand(3, 100)) * 20
    theta = rand()*2*np.pi
    center = rand(3)*20
    assert len(density.in_cylinder(xyz, center, cylinder, theta)) == 100

    assert all(density.in_half_sphere(xyz, center, 10)[xyz[-1] < 0] == 0)


def test_clumps():
    clumps_file = os.path.join(os.path.split(density.__file__)[0], "data",
                               "neclumpN.NE2001.dat")

    clumps = density.Clumps(clumps_file)

    clumps = density.Clumps()
    xyz = (clumps.xyz.T[randint(0, clumps.gl.size, 100)].T +
           (1-2*rand(3, 100))*0.01)

    ne_clumps = clumps.ne_clumps(xyz)
    assert len(ne_clumps) == 100
    ix = ne_clumps.argmax()
    assert ne_clumps[ix] == clumps.ne_clumps(xyz[:, ix])


def test_void():
    voids_file = os.path.join(os.path.split(density.__file__)[0], "data",
                              "nevoidN.NE2001.dat")

    voids = density.Voids(voids_file)

    voids = density.Voids()

    xyz = (voids.xyz.T[randint(0, voids.gl.size, 100)].T +
           (1-2*rand(3, 100))*0.01)

    ne_voids = voids.ne_voids(xyz)
    assert len(ne_voids) == 100

    ix = ne_voids.argmax()
    assert ne_voids[ix] == voids.ne_voids(xyz[:, ix])


def test_local_ism():
    xyz = (1-2*rand(3, 100)) * 20
    local_ism = density.LocalISM(xyz, **PARAMS)

    assert all(local_ism.electron_density >= 0)
    assert len(local_ism.electron_density) == 100
    assert len(local_ism.electron_density) == len(local_ism.wlism)
    assert all((local_ism.electron_density > 0) == local_ism.wlism)
    assert all((local_ism.flism > 0) == local_ism.wlism)
