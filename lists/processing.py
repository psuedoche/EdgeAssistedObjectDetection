text = open('terminal_output.txt', 'r')
lines = text.readlines()

latency_list = []
bandwidth_list = [] # bits per second
accuracy_list = []

avg_accuracy_list = []
avg_latency_list = []
avg_bandwidth_list = []

for l in lines:
    words = l.split(' ')

    if words[0] == 'Current':
        if words[1] == 'accuracy:':
           
            accuracy_list.append(float(words[2]))
        elif words[1] == 'bandwidth:':
            bandwidth_list.append(float(words[2]))
        elif words[1] == 'latency:':
            latency_list.append(float(words[2]))
    elif words[0] == 'Average':
        if words[1] == 'accuracy:':
            avg_accuracy_list.append(float(words[2]))
        elif words[1] == 'bandwidth:':
            avg_bandwidth_list.append(float(words[2]))
        elif words[1] == 'latency:':
            avg_latency_list.append(float(words[2]))


with open("accuracyClose.txt", "w") as output:
    output.write(str(accuracy_list))
with open("latencyClose.txt", "w") as output:
    output.write(str(latency_list))
with open("bandwidthClose.txt", "w") as output:
    output.write(str(bandwidth_list))

with open("avgAccuracyClose.txt", "w") as output:
    output.write(str(avg_accuracy_list))
with open("avgLatencyClose.txt", "w") as output:
    output.write(str(avg_latency_list))
with open("avgBandwidthClose.txt", "w") as output:
    output.write(str(avg_bandwidth_list))