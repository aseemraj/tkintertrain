class Train(object):
    """Name of the train along with his trainCode, Arrival Time Departure Time"""
    def __init__(self, w, code, name, arrival, departure, platform=0, outerline=0, status="notarrived"):
        self.name = name
        self.code = code
        self.arrival = arrival
        self.departure = departure
        self.platform = platform
        self.outerline = outerline
        self.status = status
        self.vel = 0
        self.body = w.create_rectangle(-350, 30, 0, 45, fill="#e33")
        self.x = w.coords(self.body)[0]
        self.y = w.coords(self.body)[1]
        self.label = w.create_text(self.x+175, self.y+7, text=str(self.name))

    def update(self, w):
        """ Called each frame. """
        w.move(self.body, self.vel, 0)
        w.move(self.label, self.vel, 0)
        self.x = w.coords(self.body)[0]
        w.update()
