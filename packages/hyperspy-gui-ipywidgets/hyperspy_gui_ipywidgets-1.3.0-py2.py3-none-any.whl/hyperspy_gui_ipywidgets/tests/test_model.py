
import numpy as np
from numpy.random import random

import hyperspy.api as hs
from hyperspy.component import Component, Parameter
from hyperspy_gui_ipywidgets.tests.utils import KWARGS
from hyperspy.models.model1d import ComponentFit


def test_parameter():
    p = Parameter()
    p.bmin = None
    p.bmax = 10
    p.value = 1.5
    wd = p.gui(**KWARGS)["ipywidgets"]["wdict"]
    assert wd["value"].value == p.value
    assert wd["max"].value == p.bmax
    wd["value"].value = -4
    p.bmin = -10
    p.bmax = 0
    assert wd["value"].value == p.value
    assert wd["min"].value == p.bmin
    assert wd["max"].value == p.bmax


def test_multivalue_parameter():
    p = Parameter()
    p._number_of_elements = 2
    p.value = (1.5, 3)
    wd = p.gui(**KWARGS)["ipywidgets"]["wdict"]
    assert wd["element0"]["value"].value == p.value[0]
    assert wd["element1"]["value"].value == p.value[1]
    wd["element0"]["value"].value = -4
    wd["element1"]["value"].value = -3
    assert wd["element0"]["value"].value == p.value[0]
    assert wd["element1"]["value"].value == p.value[1]
    # TODO: update button
    # TODO: bounds


def test_component():
    c = Component(["a", "b"])
    c.a.value = 3
    c.b.value = 2
    c.active = False
    wd = c.gui(**KWARGS)["ipywidgets"]["wdict"]
    assert wd["active"].value == c.active
    assert wd["parameter_a"]["value"].value == c.a.value
    assert wd["parameter_b"]["value"].value == c.b.value
    wd["active"].value = True
    wd["parameter_b"]["value"].value = 34
    wd["parameter_a"]["value"].value = 31
    assert wd["active"].value == c.active
    assert wd["parameter_a"]["value"].value == c.a.value
    assert wd["parameter_b"]["value"].value == c.b.value


def test_model():
    s = hs.signals.Signal1D([0])
    m = s.create_model()
    c = Component(["a", "b"])
    d = Component(["a", "b"])
    m.extend((c, d))
    c.name = "c"
    d.name = "d"
    c.active = False
    d.active = True
    wd = m.gui(**KWARGS)["ipywidgets"]["wdict"]
    assert wd["component_c"]["active"].value == c.active
    assert wd["component_d"]["active"].value == d.active


def test_eels_component():
    s = hs.signals.EELSSpectrum(np.empty((500,)))
    s.add_elements(("C",))
    s.set_microscope_parameters(100, 10, 10)
    m = s.create_model(auto_background=False)
    c = m.components.C_K
    c.active = False
    c.fine_structure_smoothing = 0.1
    c.fine_structure_active = True
    wd = m.gui(**KWARGS)["ipywidgets"]["wdict"]["component_C_K"]
    assert wd["active"].value == c.active
    assert wd["fs_smoothing"].value == c.fine_structure_smoothing
    assert wd["fine_structure"].value == c.fine_structure_active
    assert "parameter_fine_structure_coeff" not in wd
    wd["active"].value = not c.active
    wd["fs_smoothing"].value = 0.2
    wd["fine_structure"].value = not c.fine_structure_active
    assert wd["active"].value == c.active
    assert wd["fs_smoothing"].value == c.fine_structure_smoothing
    assert wd["fine_structure"].value == c.fine_structure_active


def test_scalable_fixed_pattern():
    s = hs.signals.Signal1D(np.empty((500,)))
    m = s.create_model()
    c = hs.model.components1D.ScalableFixedPattern(s)
    c.name = "sfp"
    m.append(c)
    c.intepolate = not c.interpolate
    wd = m.gui(**KWARGS)["ipywidgets"]["wdict"]["component_sfp"]
    assert wd["interpolate"].value == c.interpolate
    wd["interpolate"].value = not c.interpolate
    assert wd["interpolate"].value == c.interpolate


def test_fit_component():
    np.random.seed(0)
    s = hs.signals.Signal1D(np.random.normal(size=1000, loc=1)).get_histogram()
    s = hs.stack([s, s], axis=0)
    m = s.create_model()
    m.extend([hs.model.components1D.Gaussian(),
              hs.model.components1D.Gaussian()])
    g1, g2 = m
    g1.centre.value = 0
    g2.centre.value = 8
    fc = ComponentFit(model=m, component=g1)
    fc.ss_left_value = -2
    fc.ss_right_value = 4
    fc.only_current = not fc.only_current
    wd = fc.gui(**KWARGS)["ipywidgets"]["wdict"]
    wd["fit_button"]._click_handlers(wd["fit_button"])    # Trigger it
    assert wd["only_current"].value == fc.only_current
    wd["only_current"].value = not fc.only_current
    assert wd["only_current"].value == fc.only_current
    assert g2.centre.value == 8
    np.testing.assert_allclose(g1.centre.value, 0.804, rtol=1E-2)
    np.testing.assert_allclose(g1.sigma.value, 0.965, rtol=1E-2)
