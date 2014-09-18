class Platform(object):
    def __init__(self, w, platformNo):
        self.platformNo = platformNo
        self.occupied = False
        self.status = True
        self.train = None
        self.x = 350
        if self.platformNo%2==0:
            self.body = w.create_rectangle(350, 35*self.platformNo, 850,
                                35*self.platformNo+15, fill="#444")
            self.trainy = 35*self.platformNo-15
        else:
            self.body = w.create_rectangle(350, 35*(self.platformNo)-20, 850,
                                35*(self.platformNo)-5, fill="#444")
            self.trainy = 35*self.platformNo-5
