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


def test_range_inp1():
    with pytest.raises(ValueError):
         data_giver(np.array([[1, 1],[1,20]]))


def test_range_inp2():
    with pytest.raises(ValueError):
         data_giver(np.array([[20, 1],[1,1]]))

def test_range_inp3():
    with pytest.raises(ValueError):
         data_giver(np.array([[0.01, 1],[1,0.01]]))