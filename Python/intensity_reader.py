import pandas as pd
import numpy as np
def saved_intensity():
    df = pd.read_csv('intensity.csv', delimiter=',')
    shape = df.shape
    numpy_matrix = df.as_matrix()
    reshaped = np.reshape(numpy_matrix,(shape[0],shape[1]))
    return reshaped

