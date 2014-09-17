class Platform(object):
    def __init__(self, w, platformNo):
        self.platformNo = platformNo
        self.occupied = False
        self.status = True
        self.train = None
        self.body = w.create_rectangle(350, (self.platformNo/2)*60+(self.platformNo%2)*15,
         850, (self.platformNo/2)*60+(self.platformNo%2)*15+15, fill="#444")