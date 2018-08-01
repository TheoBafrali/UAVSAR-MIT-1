import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def read_intensity(filename="../Raw_Data/intensity.csv"):
    df = pd.read_csv(filename)
    Intensities = df.as_matrix()
    sizes = df.shape
    
    plt.set_cmap('jet')
    resized_intensities = np.reshape(Intensities,(sizes[0],sizes[1]))
    plt.imshow(resized_intensities)
    plt.show()

    log_intensity = 20*np.log10(resized_intensities)
    max_log_intensity = max(log_intensity.flatten())
    plt.imshow(log_intensity)
    plt.clim(max_log_intensity-20,max_log_intensity)
    plt.axis('equal')
    plt.show() 
    return resized_intensities
