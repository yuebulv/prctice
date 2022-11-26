import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import os
import numpy as np
import sys

def test(path):
    pass


if __name__ == "__main__":
    sys.path.append(r"./road")
    # sys.path.append(r"d:/lvcode/prctice/road")
    print(sys.path)
    from Road.chain_age import start_end_chainage_split
    res = start_end_chainage_split("ak0+000")
    print(res)
