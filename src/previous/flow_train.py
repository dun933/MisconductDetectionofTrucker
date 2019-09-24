from darkflow.net.build import TFNet
import time

start = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# options = { "model": "cfg/truck-tiny-yolo.cfg", \
#             "train": "",\
#             "dataset":"../yolo_truck_driver/images/", \
#             "annotation":"../yolo_truck_driver/annotation/", \
#             "gpu":0.3, \
#             "epoch":1000}
options = { "model": "cfg/truck-yolo-test.cfg", \
            "train": True,\
            "dataset":"labels/cellphone/images/", \
            "annotation":"labels/cellphone/annotation/", \
            "gpu":0.0, \
            "epoch":10}
tfnet = TFNet(options)
tfnet.train()

print("Training ended !")
print(start)
print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
