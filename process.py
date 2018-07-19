import numpy as np
import matplotlib.pyplot as plt
import pickle


def ingest(string):
    f = open(string, "rb")
    return pickle.load(f)

def r_to_bin(r):
    proto_bin = int(r / .0185)
    if r > 0:
        return proto_bin + 1 if r % 0.0185 >= 0.00925 else proto_bin
    else:
        return proto_bin + 1 if r % 0.0185 >= 0.00925 else proto_bin

class Target():
    pixel_size = 0
    def __init__(self, height, width, center_point, pixel_size):
        self.height = height
        self.width = width
        self.center_point = center_point
        self.pixel_size = pixel_size
# returns x,y coordinates of pixel in final image
    def get_coordinates(self, pixel_index_X, pixel_index_Y):
        return [self.center_point[0] + self.width / 2 + self.pixel_size * pixel_index_X,
                self.center_point[1] + self.height/ 2 + self.pixel_size * pixel_index_Y]

class System_State():
    def __init__(self, pos_list, target):
        self.pos_list = pos_list
        self.target = target

    def get_range(self, UAS_index, pixel_index_X, pixel_index_Y):
        xy = target.get_coordinates(pixel_index_X, pixel_index_Y)
        return np.sqrt(np.square(self.pos_list[UAS_index][0] - xy[0]) + np.square(self.pos_list[UAS_index][1] - xy[1]) + np.square(self.pos_list[UAS_index][2]))
''' def get_azimuth(self, UAS_index, pixel_index_X, pixel_index_Y):
        xy = target.get_coordinates(pixel_index_X, pixel_index_Y)
        return np.atan2(self.pos_list[UAS_index][1] - xy[1], self.pos_list[UAS_index][0] - xy[0])
'''

def get_pixels(s_state, bin_data):

    x_range = int(s_state.target.width / s_state.target.pixel_size)
    y_range = int(s_state.target.height / s_state.target.pixel_size)

    pixelValues = np.zeros((x_range, y_range))

    # loop through the pixels
    for x in range(0, x_range):
        for y in range(0,y_range):

            # for this pixel, choose a reference pulse t = 0
            # for each pulse shift it by the difference in range to the reference pulse

            pxl_val = 0
            for UAS_i in range(0, 100):
                try:
                    r = s_state.get_range(UAS_i, x, y)
                    pxl_val += float(np.real(bin_data[UAS_i, int(r_to_bin(r))]))
                except:
                    print("exception")
                    break

            pixelValues[x][y] = pxl_val

    return np.array(pixelValues)

data = ingest("data.pkl")

target = Target(5, 5, [0, 15], .1)

system_state = System_State(data[0], target)

image = get_pixels(system_state, data[1])

fig = plt.figure()

plt.imshow(image)
plt.show()
