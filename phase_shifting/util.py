import numpy
import operator


'''finds the shannon entropy of an non normalized array'''

def ent_of(array):
    entropy = 0

    for ii in range(len(array)):
        for jj in range(len(array(ii))):
            entropy += array[ii][jj]
    return entropy / np.amax(array)

'''
    takes as an argument the list of ideal scats from find_indicatice_scatts
    and the newly processed image and returns the total entropy of that 10%
    of the image
'''
def fast_ent(SAR_img, sigs):
    ent_of_scatts = 0
    for scatt in sigs:
        ent_of_scatts += ent_of(array[sigs[0]:sigs[0] + sigs[2]][sigs[1]:sigs[1] + sigs[3])
    return ent_of_scatts

'''
identifies the most indicate scatterers the image, in order to
facilatte the efficient computation of image entropy
legit just segments array into 100 squares and sort them based on entropy,
takes top 10% of arrays and returns an array of their top left corner and length and
width precondition, the image is of dimensiosn 10 (l x w)


returns list of tuples of the form (x_top_l, y_top_l, width, height, entropy)
'''

def find_indicative_scatterers(array, num_scatts):

    C_DIM = (int(len(array) / 10), int(len(array[0]) / 10)
    chunk_list = []


    if len(array) % 10 == 0 and len(array[0]) % 10 == 0
        for ii in np.arange(0, len(array), C_dim[0], dtype=int):
            for jj in np.arange(0, len(array), C_dim[0], dtype=int):
                # generate stats on this chunk
                chunk =  (C_DIM[0] * ii, C_DIM[1] * jj, C_DIM[0], C_DIM[1])
                # add entropy of the unfocused image to the column vector
                chunk.extend(ent_of(array[chunk[0]:chunk[0] + C_DIM[0]][chunk[1]:chunk[1] + C_DIM[1]]))
                # append this chunk to the list
                chunk_list.append(chunk)

        chunk_list.sort(key=operator.itemgetter(4))
        reversed(chunk_list)
        return chunk_list[0: num_scatts]


    else:
        print("NO!")

'''
   implementation of dumd dumb dumb gradient descent

   takes in the important scatts, imparts phi_shifts in all the directions
   computes cost, lather rinse repeat until num_iterations is reached
'''


def descend_the_gradient(scatts, )


