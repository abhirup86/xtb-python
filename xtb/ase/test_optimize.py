# This file is part of xtb.
#
# Copyright (C) 2020 Sebastian Ehlert
#
# xtb is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# xtb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with xtb.  If not, see <https://www.gnu.org/licenses/>.
"""Tests for some higher level functionality of ASE using the xtb Calculator"""

from xtb.ase.calculator import XTB
from ase.atoms import Atoms
from ase.optimize.bfgs import BFGS
from ase.optimize.lbfgs import LBFGS
from ase.md.verlet import VelocityVerlet
from ase.units import fs
from pytest import approx
import numpy as np


def test_gfn1xtb_bfgs():
    """Perform geometry optimization with GFN1-xTB and BFGS"""

    thr = 1.0e-5

    atoms = Atoms(
        symbols = "NHCHC2H3OC2H3ONHCH3",
        positions = np.array([
            [ 1.40704587284727, -1.26605342016611, -1.93713466561923],
            [ 1.85007200612454, -0.46824072777417, -1.50918242392545],
            [-0.03362432532150, -1.39269245193812, -1.74003582081606],
            [-0.56857009928108, -1.01764444489068, -2.61263467107342],
            [-0.44096297340282, -2.84337808903410, -1.48899734014499],
            [-0.47991761226058, -0.55230954385212, -0.55520222968656],
            [-1.51566045903090, -2.89187354810876, -1.32273881320610],
            [-0.18116520746778, -3.45187805987944, -2.34920431470368],
            [ 0.06989722340461, -3.23298998903001, -0.60872832703814],
            [-1.56668253918793,  0.00552120970194, -0.52884675001441],
            [ 1.99245341064342, -1.73097165236442, -3.08869239114486],
            [ 3.42884244212567, -1.30660069291348, -3.28712665743189],
            [ 3.87721962540768, -0.88843123009431, -2.38921453037869],
            [ 3.46548545761151, -0.56495308290988, -4.08311788302584],
            [ 4.00253374168514, -2.16970938132208, -3.61210068365649],
            [ 1.40187968630565, -2.43826111827818, -3.89034127398078],
            [ 0.40869198386066, -0.49101709352090,  0.47992424955574],
            [ 1.15591901335007, -1.16524842262351,  0.48740266650199],
            [ 0.00723492494701,  0.11692276177442,  1.73426297572793],
            [ 0.88822128447468,  0.28499001838229,  2.34645658013686],
            [-0.47231557768357,  1.06737634000561,  1.52286682546986],
            [-0.70199987915174, -0.50485938116399,  2.28058247845421],
        ]),
    )

    atoms.calc = XTB(method="GFN1-xTB", accuracy=2.0, cache_api=False)
    opt = BFGS(atoms)
    opt.run(fmax=0.1)

    assert approx(atoms.get_potential_energy(), thr) == -951.9006674709672
    assert approx(np.linalg.norm(atoms.get_forces(), ord=2), thr) == 0.2052117803208497


def test_gfn2xtb_lbfgs():
    """Perform geometry optimization with GFN2-xTB and L-BFGS"""

    thr = 1.0e-5

    atoms = Atoms(
        symbols = "NHCHC2H3OC2H3ONHCH3",
        positions = np.array([
            [ 1.40704587284727, -1.26605342016611, -1.93713466561923],
            [ 1.85007200612454, -0.46824072777417, -1.50918242392545],
            [-0.03362432532150, -1.39269245193812, -1.74003582081606],
            [-0.56857009928108, -1.01764444489068, -2.61263467107342],
            [-0.44096297340282, -2.84337808903410, -1.48899734014499],
            [-0.47991761226058, -0.55230954385212, -0.55520222968656],
            [-1.51566045903090, -2.89187354810876, -1.32273881320610],
            [-0.18116520746778, -3.45187805987944, -2.34920431470368],
            [ 0.06989722340461, -3.23298998903001, -0.60872832703814],
            [-1.56668253918793,  0.00552120970194, -0.52884675001441],
            [ 1.99245341064342, -1.73097165236442, -3.08869239114486],
            [ 3.42884244212567, -1.30660069291348, -3.28712665743189],
            [ 3.87721962540768, -0.88843123009431, -2.38921453037869],
            [ 3.46548545761151, -0.56495308290988, -4.08311788302584],
            [ 4.00253374168514, -2.16970938132208, -3.61210068365649],
            [ 1.40187968630565, -2.43826111827818, -3.89034127398078],
            [ 0.40869198386066, -0.49101709352090,  0.47992424955574],
            [ 1.15591901335007, -1.16524842262351,  0.48740266650199],
            [ 0.00723492494701,  0.11692276177442,  1.73426297572793],
            [ 0.88822128447468,  0.28499001838229,  2.34645658013686],
            [-0.47231557768357,  1.06737634000561,  1.52286682546986],
            [-0.70199987915174, -0.50485938116399,  2.28058247845421],
        ]),
    )

    atoms.calc = XTB(method="GFN2-xTB", solvent="water", accuracy=0.1)
    opt = LBFGS(atoms)
    opt.run(fmax=0.1)

    assert approx(atoms.get_potential_energy(), thr) == -897.4533662470938
    assert approx(np.linalg.norm(atoms.get_forces(), ord=2), thr) == 0.19359647527783497


def test_gfn2xtb_velocityverlet():
    """Perform molecular dynamics with GFN2-xTB and Velocity Verlet Integrator"""

    thr = 1.0e-5

    atoms = Atoms(
        symbols = "NHCHC2H3OC2H3ONHCH3",
        positions = np.array([
            [ 1.40704587284727, -1.26605342016611, -1.93713466561923],
            [ 1.85007200612454, -0.46824072777417, -1.50918242392545],
            [-0.03362432532150, -1.39269245193812, -1.74003582081606],
            [-0.56857009928108, -1.01764444489068, -2.61263467107342],
            [-0.44096297340282, -2.84337808903410, -1.48899734014499],
            [-0.47991761226058, -0.55230954385212, -0.55520222968656],
            [-1.51566045903090, -2.89187354810876, -1.32273881320610],
            [-0.18116520746778, -3.45187805987944, -2.34920431470368],
            [ 0.06989722340461, -3.23298998903001, -0.60872832703814],
            [-1.56668253918793,  0.00552120970194, -0.52884675001441],
            [ 1.99245341064342, -1.73097165236442, -3.08869239114486],
            [ 3.42884244212567, -1.30660069291348, -3.28712665743189],
            [ 3.87721962540768, -0.88843123009431, -2.38921453037869],
            [ 3.46548545761151, -0.56495308290988, -4.08311788302584],
            [ 4.00253374168514, -2.16970938132208, -3.61210068365649],
            [ 1.40187968630565, -2.43826111827818, -3.89034127398078],
            [ 0.40869198386066, -0.49101709352090,  0.47992424955574],
            [ 1.15591901335007, -1.16524842262351,  0.48740266650199],
            [ 0.00723492494701,  0.11692276177442,  1.73426297572793],
            [ 0.88822128447468,  0.28499001838229,  2.34645658013686],
            [-0.47231557768357,  1.06737634000561,  1.52286682546986],
            [-0.70199987915174, -0.50485938116399,  2.28058247845421],
        ]),
    )

    atoms.calc = XTB(method="GFN2-xTB", cache_api=False)

    dyn = VelocityVerlet(atoms, timestep=1.0*fs)
    dyn.run(20)

    assert approx(atoms.get_potential_energy(), thr) == -896.9772346260584
    assert approx(atoms.get_kinetic_energy(), thr) == 0.022411127028842362

    atoms.calc.set(cache_api=True)
    dyn.run(20)

    assert approx(atoms.get_potential_energy(), thr) == -896.9913862530841
    assert approx(atoms.get_kinetic_energy(), thr) == 0.036580471363852810
