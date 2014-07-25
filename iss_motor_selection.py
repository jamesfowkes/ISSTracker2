from __future__ import division
import math

EARTH_R = 6400
ISS_ALT = 300
G = 9.81

class Arm:
    def __init__(self, l, w, h, D):

        self.length_m = l
        self.width_m = w
        self.depth_m = h
        self.volume_m3 = l * w  * h
        self.density_kg_p_m3 = D
        self.weight_kg = D * self.volume_m3
        self.com_m = l / 2
        self.moment = self.com_m * self.weight_kg
        self.moi = self.com_m * self.com_m * self.weight_kg

class CW:
    def __init__(self, m, arm):

        self.mass = m
        self.loc = -arm.moment / m
        self.moi = self.loc * self.loc * m

class ISS:
    def __init__(self):
        self.altitude = ISS_ALT
        self.orbit = EARTH_R + ISS_ALT
        self.transit_time_s = (2 * 60)
        
    @property
    def max_angular_velocity(self):
        return math.pi / self.transit_time_s

class Motor:
    def __init__(self, spr):
        self.spr = spr
    
class Drive:

    def __init__(self, motor, gearing):
        self.motor = motor
        self.gearing = gearing

    @property
    def spr(self):
        return self.motor.spr * self.gearing
        
    def angularv_to_steprate(self, w):
        revs_per_s = w / ( 2 * math.pi)
        return revs_per_s * self.spr

    def rads_per_step(self):
        return 2 * math.pi / self.spr
        
arm = Arm(1.5, 0.15, 0.006, 900)
cw = CW(2, arm)
total_moi = arm.moi + cw.moi
iss = ISS()

drive = Drive(Motor(800), 16)

print "Arm of weight %.1fkg, length %.1fm is stablised by mass of %.1fkg at %.1fm" % (arm.weight_kg, arm.length_m, cw.mass, cw.loc)
print "MOI of arm is %.1fkgm^2, MOI of counterweight is %.1fkgm^2, total is %.1fkgm^2" % (arm.moi, cw.moi, total_moi)
print "Maximum ISS angular velocity %.1f deg/s" % math.degrees(iss.max_angular_velocity)
print "Max. step rate = %.1f steps per second" % drive.angularv_to_steprate(iss.max_angular_velocity)
