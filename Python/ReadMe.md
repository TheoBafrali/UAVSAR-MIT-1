# Workflow for processing and forming a SAR image: #
  
  ## Outside of Python: ##
  * Film .tak file in Motive to get approximate motion start and end frames
  * Open reference .csv of single reflector and calculate average position
  
  ## Read in data: ##
  * Unpack RADAR data using unpack(), saving into data.pkl
  * Read in RADAR from data.pkl trimming with defaults trim = 580, rangeshift = 0.3
  * Compute RCS scaled version of RADAR data using rcs()
  * Read in motion data from .csv file
  
  ## Align data: ##
  * Plot RTI graph using plotRTI() to estimate start RADAR data
  * Plug in motion start and end frames from Step 1 and start RADAR data at frame from previous step
  * Run aligndata() with 0 and 3500 as initial inputs
  * Plot aligned data using AlignedGraph() 
  * Play around with parameters to form the best alignment as shown in AlignedGraph()
  
  ## Backproject: ##
  * Use BackProjection(), with any interval/step size, to generate the image 
    * First use relatively large step sizes, but make them smaller as you go
    
  ## Deconvolute and plot: ##
  * Run Richardson-Lucy deconvolution using deconvolute()
    * Plot images, and export data as an array
