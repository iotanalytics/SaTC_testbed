import chardet
from scipy.signal import butter, lfilter
from scipy import signal
from datetime import datetime, date
import numpy
import random
import time
import sys
import logging
from scipy.stats import kurtosis
import nitime.algorithms as nt_alg
import numpy as np
from numpy import array
import scipy as sp
import ast
from statsmodels.tsa.stattools import acf
import statsmodels.api as sm
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import time, datetime
import pytz
import pandas as pd


def predict(signal, fs, cutoff,nlags,order):
    # add algorithm details
    return np.random.randint(60, 90, 1),np.random.randint(10, 20, 1), np.random.randint(120, 150, 1), np.random.randint(90, 120, 1)

