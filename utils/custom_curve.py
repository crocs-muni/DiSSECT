def montgomery_to_short_weierstrass(F, A, B, x, y):
    a = F( (3 -A**2 )/(3 *B**2 ) )
    b = F( (2 *A**3  - 9 *A)/(27 *B**3 ) )
    u = F( (3 *x+A)/(3 *B) )
    v = F( y/B )
    assert (u, v) in EllipticCurve(F, [a,b])
    return (a, b, u, v)

def twisted_edwards_to_montgomery(F, a, d, u, v, scaling = True):
    A = F( (2 *a + 2 *d)/(a- d) )
    B = F( 4 /(a - d) )
    if not B.is_square():
        scaling = False
    s = F(1 /B).sqrt()
    x = F( (1  + v)/(1  - v) )
    y = F( (1  + v)/((1  - v) * u) )
    if scaling:
        assert (x, y/s) in EllipticCurve(F, [0 , A, 0 , 1 , 0 ])
        return (A, 1 , x, y/s)
    return (A, B, x, y)

def twisted_edwards_to_short_weierstrass(F, aa, d, x, y, composition = False):
    if composition:
        A, B, x, y = twisted_edwards_to_montgomery(F, a, d, u, v, True)
        a, b, u, v = montgomery_to_short_weierstrass(F, A, B, x, y)
    else:
        a = F((aa**2  + 14  * aa * d + d**2 ) )/F(-48)
        b = F((aa+d) * (-aa**2  + 34  * aa * d - d**2 ) )/F(864 )
        u = (5 *aa + aa*y - 5 *d*y - d)/(12  - 12 *y)
        v = (aa + aa*y - d*y -d)/(4 *x - 4 *x*y)
    assert (u, v) in EllipticCurve(F, [a,b])
    return (a, b, u, v)

class CustomCurve:
    
    def __init__(self, db_curve):
        '''the "fixed" part of attributes'''
        self.name = db_curve['name']
        self.order = ZZ(db_curve['order'])
        self.source = db_curve['category']
        self.field = db_curve['field']
        self.form = db_curve['form']
        self.params = db_curve['params']
        self.desc = db_curve['desc']
        self.cofactor = ZZ(db_curve['cofactor'])
        self.nbits =  self.order.nbits()
        self.EC = None
        self.generator = None
        self.q = None
        self.trace = None
        '''the "variable" part of attributes'''    
        try:
            self.seed = db_curve['seed']
        except KeyError:
            self.seed = None
        try:
            self.x = ZZ(db_curve['generator']['x'])
            self.y = ZZ(db_curve['generator']['y'])
        except TypeError:
            self.x = None
            self.y = None
    #         self.characteristics = db_curve['characteristics']
        self.set()

    def set_generator(self, coord1, coord2, binary = False):
        if self.x == None or self.y == None:
            self.generator = None
        else:
            if binary:
                self.generator = self.EC(K.fetch_int(coord1), K.fetch_int(coord2))
            else:
                self.generator = self.EC(coord1, coord2)

    def set(self):
        x = self.x
        y = self.y
        if self.form == "Weierstrass":
            a = ZZ(self.params['a'])
            b = ZZ(self.params['b'])
            if self.field['type'] == "Prime":
                p = ZZ(self.field['p'])
                self.EC = EllipticCurve(GF(p), [a,b])
                self.set_generator(x,y)
            elif self.field['type'] == "Binary":
                exponents = list(self.field['poly'].values())
                exponents.append(0 )
                F = GF(2 )['w']; (w,) = F._first_ngens(1)
                modulus = 0 
                for e in exponents:
                    modulus += w**e
                m = ZZ(self.field['poly']['m'])
                K = GF(2 **m, 'w', modulus)
                self.EC = EllipticCurve(K, [1 ,K.fetch_int(ZZ(a)),0 ,0 ,K.fetch_int(ZZ(b))]) #xy, x^2, y, x, 1
                # print(self.EC)
                self.generator = None
                # self.set_generator(x,y)
                # needs fixing, originally:
                # self.generator = self.EC(K.fetch_int(x), K.fetch_int(y))

        elif self.form == "Montgomery":
            A = ZZ(self.params['a'])
            B = ZZ(self.params['b'])
            p = ZZ(self.field['p'])
            F = GF(p)
            a, b, u, v = montgomery_to_short_weierstrass(F, A, B, x, y)
            self.EC = EllipticCurve(F, [a,b])
            self.set_generator(u,v)

        elif self.form in ["Edwards", "TwistedEdwards"]:
            #we assume c=1
            if self.form == "Edwards":
                aa = 1 
            if self.form == "TwistedEdwards":
                aa = ZZ(self.params['a'])
            d = ZZ(self.params['d'])
            p = ZZ(self.field['p'])
            F = GF(p)
            a, b, xx, yy = twisted_edwards_to_short_weierstrass(F, aa, d, x, y)
            self.EC = EllipticCurve(F, [a,b])
            self.set_generator(xx,yy)
        else:
            self.EC = "Not implemented"

        self.q = self.EC.base_field().order()
        self.trace = self.q + 1  - self.order * self.cofactor

    def __repr__(self):
        return self.name + ": " + str(self.nbits) + "-bit curve in " + self.form + " form over " + self.field['type'] + " field" 
    
    def __str__(self):
        return self.name + ": " + str(self.nbits) + "-bit curve in " + self.form + " form over " + self.field['type'] + " field" 

    def __lt__(self, other):
        return (self.order, self.name) < (other.order, other.name)

class SimulatedWeierstrassCurve():
    def __init__(self, F, a, b, seed):
        self.F = F
        self.nbits = self.F.order().nbits()
        self.a = F(a)
        self.b = F(b)
        self.seed = seed
        self.EC = EllipticCurve(F, [a, b])
        self.order = self.EC.order()

    def __repr__(self):
        return str(self.nbits) + "-bit Weierstrass curve"
    
    def __str__(self):
        return str(self.nbits) + "-bit Weierstrass curve"

    def __lt__(self, other):
        return (self.order) < (other.order)