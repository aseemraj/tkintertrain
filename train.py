class Train(object):
    """Name of the train along with his trainCode, Arrival Time Departure Time"""
    def __init__(self, w, code, name, arrival, departure, platform=0, status=0):
        self.name = name
        self.code = code
        self.arrival = arrival
        self.departure = departure
        self.platform = platform
        self.status = status
        self.vel = 2
        self.body = w.create_rectangle(0, 30, 350, 40, fill="#e33")
        self.x = w.coords(self.body)[0]
        self.y = w.coords(self.body)[1]

    def update(self, w):
        """ Called each frame. """
        w.move(self.body, self.vel, 0)
        self.x = w.coords(self.body)[0]
        w.update()
        # self.tempi += 1
        # if self.vel>0:
        #     self.bogies = int(bogies + 1 - math.ceil((self.x-200)/bogielength))
        # elif self.vel<0:
        #     self.bogies = 20 - (self.x+100)/bogielength
