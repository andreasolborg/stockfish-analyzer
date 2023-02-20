import random
import matplotlib.pyplot as plt

def DrawSample(minimumValue, maximumValue, mode, size):
    sample = []
    for _ in range(0, size):
        x = random.triangular(minimumValue, maximumValue, mode)
        sample.append(x)
    return sample

def ProcessSample(minimumValue, sample):
    sample.sort()
    times = []
    counts = []
    count = len(sample)
    times.append(minimumValue)
    counts.append(count)
    for x in sample:
        times.append(x)
        count -= 1
        counts.append(count)
    return (times, counts)
   
minimumValue = 100
maximumValue = 200
mode = 140
size = 100

sample1 = DrawSample(minimumValue, maximumValue, mode, size)
sample2 = DrawSample(minimumValue, maximumValue, mode, size)

(times1, counts1) = ProcessSample(sample1)
(times2, counts2) = ProcessSample(sample2)

plt.plot(times1, counts1, 'b')
plt.plot(times2, counts2, 'g')
plt.savefig("KaplanMeier.pdf")
plt.show()

















