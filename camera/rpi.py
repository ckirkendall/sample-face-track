import picamera
import picamera.array


class RPICam(object):

    def __init__(this,
                 resolution=(640, 480)):
        this.resolution = resolution
        this.camera = picamera.PiCamera()

        this.stream = picamera.array.PiRGBArray(this.camera)
        this.camera.resolution = (640, 480)

    def get_frame(this):
        this.stream.seek(0)
        this.stream.truncate()

        this.camera.capture(this.stream,
                            'bgr',
                            use_video_port=True)

        return this.stream.array
