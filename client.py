import requests
from os import listdir
import os
from os.path import isfile, join, getsize, stat
import io
import PIL.Image as Image
import time


filePath = "coco/images/val2017" 
onlyfiles = [f for f in listdir(filePath) if isfile(join(filePath, f))]
labelPath = "coco/labels"
labels = [f for f in listdir(filePath) if isfile(join(filePath, f))]
# all possible labels our Yolov3 model can identify
listLabels =  ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple','sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone','microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear','hair drier', 'toothbrush']
idx = 0

result_list = []
prediction_list = []

# keeps track of data for all images
latency_list = [] # seconds
bandwidth_list = [] # bits per second
accuracy_list = []

avg_accuracy_list = []
avg_latency_list = []
avg_bandwidth_list = []

count = 0
for file in onlyfiles:
    count += 1
    print(count) 
    if count > 300:
        break
    print('new image: '+ file)
    image_size = os.stat(filePath + "/" + file).st_size / 8.0
    # get the text file with the true labels for the corresponding image
    trueLabelPath = "coco/labels/val2017/" + file.split(".")[0] + ".txt"
    # make sure there exists a file that contains the true labels
    if os.path.exists(trueLabelPath):
        trueLabels = open(trueLabelPath, 'r')
        lines = trueLabels.readlines()
        true_label_dict = {}
        # transfer data in the true label txt to a dictionary
        # the keys are the label names, the values are their frequency
        # the labels are formatted in rows-one label per row
        # the first number in each row is the index of the label in a list
        # the rest of the numbers represent the bounding boxes
        for l in lines:
            label_index = listLabels[int(l.split(" ")[0])]
            if label_index in true_label_dict:
                true_label_dict[label_index] = true_label_dict[label_index] + 1
            else:
                true_label_dict[label_index] = 1
        print(true_label_dict)
        dict_length = 0 # number of total labels in the image
        for key in true_label_dict:
            dict_length += true_label_dict[key]

        start_time = 0
        with open(join(filePath, file), "rb") as image:
            f = image.read()
            image_bytes = bytearray(f)
            # start timer to calculate latency and bandwidth
            start_time = time.time()
            r = requests.put("http://10.194.67.194:20000/image", data=image_bytes)
        time.sleep(0.1)

        while (True):
            # retrieve the prediction from the server
            result_prediction = requests.get('http://10.194.67.194:20000/prediction').content
            
            if result_prediction != b'':
                if result_prediction not in prediction_list and result_prediction != b'':
                    idx = idx + 1
                    print(result_prediction)
                    prediction_list.append(result_prediction) 
                    result_string = result_prediction.decode('UTF-8') # turn from bytes into string
                    result_string = result_string.split('-')[0]
            
                    # result.save("ResultFolder/result" + str(idx) +".jpg")
                    # end timer
                    end_time = time.time()
                    

                    result_string_list = result_string.split(', ')
                    # processing the returned prediction
                    for s in result_string_list:
                        label_frequency = s[0] # how many times a predicted label occurs 
                        label_predicted = s[2:] # the predicted label name
                        if label_predicted[-1] == 's':
                            label_predicted = label_predicted[:-1]
                        # find difference with the true labels
                        if label_predicted in true_label_dict:
                            for q in range(int(label_frequency)):
                                if true_label_dict[label_predicted] != 0:
                                    true_label_dict[label_predicted] = true_label_dict[label_predicted] - 1

                    new_dict_length = 0
                    for key in true_label_dict:
                        new_dict_length += true_label_dict[key]
                    # compare the lengths of the dictionarys to get the accuracy
                    accuracy = (dict_length - new_dict_length)/dict_length
                    accuracy_list.append(accuracy)
                    avg_accuracy = sum(accuracy_list)/ len(accuracy_list)
                    avg_accuracy_list.append(avg_accuracy)
                    # calculate latency
                    elapsed_time = end_time - start_time
                    latency_list.append(elapsed_time)
                    avg_latency = sum(latency_list) / len(latency_list)
                    avg_latency_list.append(avg_latency)
                    # calculate bandwidth
                    bandwidth = image_size / elapsed_time
                    bandwidth_list.append(bandwidth)
                    avg_bandwidth = sum(bandwidth_list) / len(bandwidth_list)
                    avg_bandwidth_list.append(avg_bandwidth)

                    # stats printed after every image
                    print("Current accuracy: {}".format(accuracy))
                    print("Current latency: {}".format(elapsed_time))
                    print("Current bandwidth: {}".format(bandwidth))
                    print("Average accuracy: {}".format(avg_accuracy))
                    print("Average latency: {}".format(avg_latency))
                    print("Average bandwidth: {}".format(avg_bandwidth))
                    break

# write the lists to external txt files          
with open("lists/accuracy.txt", "w") as output:
    output.write(str(accuracy_list))
with open("lists/latency.txt", "w") as output:
    output.write(str(latency_list))
with open("lists/bandwidth.txt", "w") as output:
    output.write(str(bandwidth_list))

with open("lists/avgAccuracy.txt", "w") as output:
    output.write(str(avg_accuracy_list))
with open("lists/avgLatency.txt", "w") as output:
    output.write(str(avg_latency_list))
with open("lists/avgBandwidth.txt", "w") as output:
    output.write(str(avg_bandwidth_list))

# final printout of the lists
print("accuracy list: ")
print(accuracy_list)
print("latency list: ")
print(latency_list)
print("bandwidth list: ")
print(bandwidth_list)

print("avg accuracy list: ")
print(avg_accuracy_list)
print("avg latency list: ")
print(avg_latency_list)
print("avg bandwidth list: ")
print(avg_bandwidth_list)
