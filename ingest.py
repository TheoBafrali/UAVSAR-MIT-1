import numpy
import pickle
import pylab

def ingest(string):
   print("ingesting")
   f = open(string, "rb")
   return pickle.load(f)



data = ingest("data.pkl")
Platform = data[0]
Pulses = data[1]
RangeAxis = data[1]

PulseMag = np.absolute(Pulses)

for i in PulseMag:

