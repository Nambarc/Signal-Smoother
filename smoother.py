
"""
The purpose of this script is to demonstrate how a sampled signal can be
smoothed.

The original signal is a perfect sin wave. Values are generated every cycle
and plotted.

The sampled signal value only updates every n cycles. It then continues to
output the same sampled value until the next update.

The smoothed value counts how many sampled values we recieved before the
sampled value changes. It then calculates the gradient between the previous
sampled value and the latest value. It then outputs values that follow a
linear interpolation between the previous and current sampled values.

The smoothed value is not perfect, but it does a pretty good job at
approximating the original signal. The main drawback is that the smoothed
value has to be n cycles behind real signal value, where n is the sample rate.
This is unavoidable.

It should be possible to better approximate the values of the original signal.
But this is only achievable if we know the "shape" of the original signal e.g.
the characteristics of a sin wave are well known but if we were trying to
interpolate the values of CPU usage, we don't know what pattern it will take.

I pinched some code from this example to get the animation working:
https://towardsdatascience.com/plotting-live-data-with-matplotlib-d871fac7500b

"""

# Library imports.
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Core Python imports.
import math

# Initialise figures and plots.
fig = plt.figure(figsize=(12,6), facecolor="#DEDEDE")
ax = plt.subplot()
ax.set_facecolor("#DEDEDE")

# Initialise lists and populate with zeros.
signal_list = []
sample_list = []
smooth_list = []
x = 0
while x < 1000:
    signal_list.append(0)
    sample_list.append(0)
    smooth_list.append(0)
    x += 1

# Initialise plots.
ax.plot(signal_list)
ax.plot(sample_list)

# Global variables we need.
index = 0
current_x = 0
sampled_value = 0
sampled_count = 0
old_sampled_value = 0
current_gradient = 0
current_smoothed = 0
smooth_count = 0

# Function to be called by MatPlotLib
def UpdateData(i):

    # Get all the globals we need.
    global index
    global current_x
    global sampled_value
    global sampled_count
    global current_gradient
    global smooth_count
    global current_smoothed
    global old_sampled_value

    # Update signal list
    signal_list.pop(0)
    signal_value = math.sin(current_x)
    signal_list.append(signal_value)
    current_x += 0.01
    ax.cla()
    ax.plot(signal_list)

    # Update the sampled list. Only grab the latest value after n cycles.
    if (index % 40) == 0:
        sampled_value = signal_value
    sample_list.pop(0)
    sample_list.append(sampled_value)
    ax.plot(sample_list)

    # Finally, generate our behind time "smoothed" data.
    sampled_count += 1
    if sampled_value != old_sampled_value:

        # Work out gradient for next set of data.
        current_gradient = (sampled_value - old_sampled_value) / sampled_count

        # Remember how many data points to output at this value.
        smooth_count = sampled_count

        # Reset our sampled count so we can count the next set.
        sampled_count = 1

        # Update the old sampled value.
        old_sampled_value = sampled_value

    # Update the smoothed data set.
    current_smoothed += current_gradient
    smooth_list.pop(0)
    smooth_list.append(current_smoothed)
    ax.plot(smooth_list)

    # Update index.
    index += 1

# Now run the animation.
ani = FuncAnimation(fig, UpdateData, interval=40)
plt.show()
