Workflow for processing and forming a SAR image:
  
  Outside of Python:
  1. Film .tak file in Motive to get approximate motion start and end frames
  2. Open reference .csv of single reflector and calculate average position
  
  Read in data:
  3. Unpack RADAR data using unpack(), saving into data.pkl
  2. Read in RADAR from data.pkl trimming with defaults trim = 580, rangeshift = 0.3
  3. Compute RCS scaled version of RADAR data using rcs()
  4. Read in motion data from .csv file
  
  Align data:
  5. Plug in motion start and end frames from Step 1 and start RADAR data at frame 300
  6. Run aligndata() with 0 and 3500 as initial inputs
  7. Plot aligned data using AlignedGraph() 
  8. Play around with parameters to form the best alignment as shown in AlignedGraph()
  
  Backproject:
  9. Use BackProjection(), with any interval/step size, to generate the image 
     First use relatively large step sizes, but make them smaller as you go
    
  Deconvolute and plot:
  10. Run Richardson-Lucy deconvolution using deconvolute()
      Plot images, and export data as an array
