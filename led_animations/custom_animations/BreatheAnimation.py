import time
from adafruit_led_animation.animation import Animation

# Breathe
# Lights will gradually get dimmer than lighten again
# Similar to the pulse LED animation with more configuration

class BreatheAnimation(Animation):
    def __init__(
        self
        ,pixel_object
        ,speed
        ,colors
        ,rate=0.1
        ,step=0.04
        ,count=1
        ):

        super().__init__(pixel_object, speed, (0, 0, 0))

        self.direction = "forward"
        self.high_limit = 0.5
        self.low_limit = 0.025
        self.brightness = self.high_limit
        self.colors = colors
        self.rate = rate
        self.step = step
        self.count = count

    def cycle(self, color):
        for c in range(self.count):
            do_breathe = True
            while do_breathe:
                if self.direction is "forward":
                    self.pixel_object.brightness = self.brightness
                    self.pixel_object.fill(color)
                    self.pixel_object.show()
                    self.brightness -= self.step
                    if round(self.brightness, 2) < self.low_limit:
                        self.direction = "backward"
                        self.brightness += self.step
                    time.sleep(self.rate)
                elif self.direction is "backward":
                    self.pixel_object.brightness = self.brightness
                    self.pixel_object.fill(color)
                    self.pixel_object.show()
                    self.brightness += self.step
                    if round(self.brightness, 2) > self.high_limit:
                        self.direction = "forward"
                        self.brightness -= self.step
                        do_breathe = False

    def draw(self):
        for clr in self.colors:
            self.cycle(clr)