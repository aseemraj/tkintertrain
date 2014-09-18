class Platform(object):
    def __init__(self, w, platformNo):
        self.platformNo = platformNo
        self.occupied = False
        self.status = True
        self.train = None
        if self.platformNo%2==0:
            self.body = w.create_rectangle(350, 30*self.platformNo, 850,
                                30*self.platformNo+15, fill="#444")
        else:
            self.body = w.create_rectangle(350, 60*self.platformNo-45, 850,
                                60*self.platformNo-30, fill="#444")
