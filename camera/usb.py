import cv2


class USBCam(object):

    def __init__(this,
                 resolution=(1024, 1080)):
        this.resolution = resolution

        this.camera = cv2.VideoCapture(0)

        #this.camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        #this.camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        #this.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    def get_frame(this):
        ret_val, img = this.camera.read()
        return cv2.flip(img, 1)
