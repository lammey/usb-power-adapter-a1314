class Vec3(tuple):
    def add(self, other):
        return Vec3(sum(i) for i in zip(self,other))

    @classmethod
    def fromFloats(x,y,z):
        return Vec3([x,y,z])