import numpy as np
import pytest
from project import *

from pathlib import Path
from mat4py import loadmat
from streamz import Stream
import pandas as pd
import pygame
from PIL import Image,ImageFilter
import time

def test_bool_inp1():
    with pytest.raises(TypeError):
         data_giver(np.array([[bool, 1],[1,bool]]))
