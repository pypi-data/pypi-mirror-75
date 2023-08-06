# -*- coding: utf-8 -*-
'''
fefiphopy version 0.0.4
© N. Worley
https://github.com/NWorley01/FeFiPhoPy
'''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tqdm

from ._steps import z_score, scale_Isos, calc_dF_F, _help
from ._get_data import read_doric
from ._smooth import running_mean, butter_lowpass, butter_highpass
from ._smooth import butter_lowpass_filter, butter_highpass_filter
from ._baseline_correction import WhittakerSmooth, airPLS
from ._methods import dFF_martian, dFF_generic
