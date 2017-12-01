from jun import jun
import sys

length = int(sys.argv[1])

a = jun (length)
#print a.measure_entropy(1)
a.mix()
#entropy = a.gauge_entropy()
#print entropy
print a.min_entropy
print a.measure_entropy(1)
