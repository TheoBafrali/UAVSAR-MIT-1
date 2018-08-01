import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.autoinit import context
from pycuda.compiler import SourceModule
import numpy as np 
from timeit import default_timer as get_time
from matplotlib import pyplot as plt
from sys import getsizeof

# pulses is the pulse range-bin data, positions the dtaa that coreespond with that, center is the 
# center of the image in the coordinate system of the UAS pxl_w is the size of each pixel
# dimensions refers to the size of the image in m, tuple plz

def back_project_CUDA(pulses, positions, center, dimensions, pxl_w, z_val):
    # assign block and grid dimensions for compute

    # BLOCK = (int(dimensions[0] / pxl_w), 1, 1)
    # GRID = (int(dimensions[1] / pxl_w), 1, 1)

    
    BLOCK = (100, 1, 1)



    # assign pulse constants
    NUM_PULSES = len(pulses )
    BINS_PER_PULSE = len(pulses[0])
    IMG_PXL_DIMENSIONS = (int(dimensions[0] / pxl_w), int(dimensions[1] / pxl_w))
    TOP_LEFT = (center[0] - int(dimensions[0] / 2), center[1] - int(dimensions[1] / 2))
    BIN_DELTA = .009148939758300667

    grid_num = int(IMG_PXL_DIMENSIONS[0] * IMG_PXL_DIMENSIONS[1] / 100)
    GRID = (grid_num, 1, 1)
    
 
    # dimensions in m
    DIMENSIONS = dimensions
    PXL_W = pxl_w

    # convert pulse data to proper format
    PULSES = np.array(pulses).astype(np.float32)
    POSITIONS = np.array(positions).astype(np.float32)

    # reshape pulses to 1D for each time the pulses are laid out
    PULSES.flatten(order = 'C')
    POSITIONS.flatten(order = 'C')

    # crate empty image 1D array, all val of column1, column2...
    img1D = np.zeros(100 * grid_num, dtype = np.float32)

    # allocate mem on GPU for target and pulses
    img1D_GPU = cuda.mem_alloc(4 * len(img1D))
    pulses_GPU = cuda.mem_alloc(PULSES.nbytes)
    positions_GPU = cuda.mem_alloc(POSITIONS.nbytes)

    Z_VAL_GPU = cuda.mem_alloc(getsizeof(z_val))
    NUM_PULSES_GPU = cuda.mem_alloc(getsizeof(NUM_PULSES))
    TOP_LEFT_X_GPU = cuda.mem_alloc(getsizeof(TOP_LEFT[0]))
    TOP_LEFT_Y_GPU = cuda.mem_alloc(getsizeof(TOP_LEFT[1]))
    BIN_DELTA_GPU = cuda.mem_alloc(getsizeof(BIN_DELTA))
    DIMENSION_X_GPU = cuda.mem_alloc(DIMENSIONS[0])
    DIMENSION_Y_GPU = cuda.mem_alloc(DIMENSIONS[1])
    PXL_W_GPU = cuda.mem_alloc(getsizeof(PXL_W))
    BINS_PER_PULSE_GPU = cuda.mem_alloc(BINS_PER_PULSE)

    # copy over data to GPU
    cuda.memcpy_htod(img1D_GPU, img1D)
    cuda.memcpy_htod(pulses_GPU, PULSES)
    cuda.memcpy_htod(positions_GPU, POSITIONS)

    cuda.memcpy_htod(Z_VAL_GPU, np.array(z_val))
    cuda.memcpy_htod(NUM_PULSES_GPU, np.array(NUM_PULSES))
    cuda.memcpy_htod(TOP_LEFT_X_GPU, np.array(TOP_LEFT[0]))
    cuda.memcpy_htod(TOP_LEFT_Y_GPU, np.array(TOP_LEFT[1]))
    cuda.memcpy_htod(BIN_DELTA_GPU, np.array(BIN_DELTA))
    cuda.memcpy_htod(DIMENSION_X_GPU, np.array(DIMENSIONS[0]))
    cuda.memcpy_htod(DIMENSION_Y_GPU, np.array(DIMENSIONS[1]))
    cuda.memcpy_htod(PXL_W_GPU, np.array(PXL_W))
    cuda.memcpy_htod(BINS_PER_PULSE_GPU, np.array(BINS_PER_PULSE))

    # kernel which computes the return of a single pixel
    # each block computes a row, with a core responsible for each pixel
    # bin gives the bin values given the range vector for the pulses
    # range computes the vector of distances for each a given pixel index

    projection_kernel = """

    // converts the range inputed to the correct bin number for indexing 
    __device__
    int bin(float range, float bin_delta) {
        return(int(range / bin_delta));
    }

    __device__
    float _range(float pxl_x, float pxl_y, float pxl_z, float* pos_data, int pulse_index) {
        return norm3df(pxl_x - pos_data[3 * pulse_index], pxl_y - pos_data[3 * pulse_index + 1], pxl_z - pos_data[3 * pulse_index + 2]);
    }

    // tl = top left, pxl_d_x/y is the dimensiosn of the image in pixels, bin delta the distance bewteen range bins
    __global__
    void project(int tl_x, int tl_y, int pxl_w, int pxl_d_x, int pxl_d_y, float z_val, float bin_delta, int bins_per_pulse, int num_pulses, float* pulse_data, float* pos_data, float* img) {
        
        // get thread info
        int tx = threadIdx.x;
        int bx = blockIdx.x;
        int bw = blockDim.x;
        int ID = tx + bx * bw;

        // initialize return value
        float return_val = 0;

        // use threadId info to determine image indices, x y
        int pixel_coordinateX = int(ID % pxl_d_x);
        int pixel_coordinateY = ID * ((ID % pxl_d_x) - int(ID % pxl_d_x));

        // get pixel coordinates in meters
        int Xcoord = tl_x + pixel_coordinateX * pxl_w;
        int Ycoord = tl_y + pixel_coordinateY * pxl_w;

        for(int i = 0; i < num_pulses; i++) {
            int range_current = _range(Xcoord, Ycoord, z_val, pos_data, i);
            return_val += pulse_data[bins_per_pulse * i + bin(range_current, bin_delta)];
        }

        img[ID] = return_val;    

    }
    """
    # create kernel
    func_kernel = SourceModule(projection_kernel).get_function("project")

    img1D_GPU_results = np.empty_like(img1D_GPU)

    # call kernel
    func_kernel(TOP_LEFT_X_GPU, TOP_LEFT_Y_GPU, PXL_W_GPU, DIMENSION_X_GPU, DIMENSION_Y_GPU, Z_VAL_GPU , BIN_DELTA_GPU, BINS_PER_PULSE_GPU, NUM_PULSES_GPU, pulses_GPU, positions_GPU, img1D_GPU, block =  BLOCK, grid = GRID)
    
    # context.synchronize()

    print("YAY is projected!!")

    # instantite target
    img1D_result = np.empty_like(img1D)
    print("target instantiated")

    # get img from GPU
    context.synchronize()
    # cuda.memcpy_dtoh(img1D_result, img1D_GPU)
    print("mem copied")

    # form 2d img
    img1D_result.reshape(IMG_PXL_DIMENSIONS, order = 'C')
    # img2D = np.reshape(img1D_result, (IMG_PXL_DIMENSIONS), order = 'C')

    plt.imshow(img1D_result)
    plt.plot()
    return img1D_result