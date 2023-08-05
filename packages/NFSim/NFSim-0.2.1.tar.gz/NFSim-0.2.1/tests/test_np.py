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


def test_none_inp():
    with pytest.raises(TypeError):
         data_giver(('dog','cat'))