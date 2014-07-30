from __future__ import division
import math

EARTH_R = 6400
ISS_ALT = 300
G = 9.81
STEEL_D = 8050
SAFETY_FACTOR = 2

def gcm2_to_kgm2(gcm2):
    return gcm2 * 0.0000001
    
def gcm_to_kgm(gcm):
    return gcm * 0.001 * 0.01

def kgcm_to_kgm(kgcm):
    return kgcm / 100
    
def kgm_to_kgcm(kgm):
    return kgm * 100
    
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
        self.own_moi = self.weight_kg * (pow(l, 2) + pow(w, 2)) / 12
        self.moi = self.own_moi + (self.weight_kg * pow(self.com_m, 2))

class CW:
    def __init__(self, m, r):
        self.mass = m
        self.volume = m / STEEL_D
        self.s = pow(self.volume, 1/3)
        self.own_moi = pow(self.s, 2) * self.mass / 6
        self.loc = -r
        self.moment = self.loc * self.mass
        self.moi = self.own_moi + (pow(self.loc,2) * self.mass)
        
class ISS:
    def __init__(self):
        self.altitude = ISS_ALT
        self.orbit = EARTH_R + ISS_ALT
        self.transit_time_s = (2 * 60)
        
    @property
    def max_angular_velocity(self):
        return math.pi / self.transit_time_s

class Motor:
    ## All torque values stored in kgm!
    def __init__(self, name, base_spr, rotor_inertia_gcm2, detent_torque_gcm, max_torque_gcm):
        self.name = name
        self.base_spr = base_spr
        self.rotor_inertia = gcm2_to_kgm2(rotor_inertia_gcm2)
        self.detent_torque = gcm_to_kgm(detent_torque_gcm)
        self.max_torque_kgm = gcm_to_kgm(max_torque_gcm)
    
    def meetsTorqueRequirement(self, max_torque_kgm):
        return self.max_torque_kgm >= max_torque_kgm
        
    @property
    def getMaxTorque(self):
        return self.max_torque_kgm
           
class Drive:

    def __init__(self, motor, microstep, gearing):
        self.motor = motor
        self.gearing = gearing
        self.microstep = microstep
        
    @property
    def spr(self):
        return self.motor.base_spr * self.gearing * self.microstep
        
    def angularv_to_steprate(self, w):
        revs_per_s = w / ( 2 * math.pi)
        return revs_per_s * self.motor.base_spr * self.microstep

    @property
    def rads_per_step(self):
        return 2 * math.pi / self.spr

    @property
    def stepping_safety_factor(self):
        return 1 / math.sin(math.pi / (2 * self.microstep))
        
    def getDetails(self):
        return (
            "Motor name: %s" % self.motor.name,
            "Motor spr: %d" % self.motor.base_spr,
            "Gearing %.2f" % self.gearing,
            "Microstepping %d (safety factor %.2f)" % (self.microstep, self.stepping_safety_factor),
            "Rads per step %f" % self.rads_per_step
            )
            

class MassSystem:
    def __init__(self, arm, cw):
        self.arm = arm
        self.cw = cw
            
    @property
    def ArmMOI(self):
        return self.arm.moi
    
    @property
    def CwMOI(self):
        try:
            return self.cw.moi
        except:
            return 0
    
    @property
    def TotalMOI(self):
        return self.ArmMOI + self.CwMOI

    @property
    def LoadMoment(self):
        try:
            return abs(self.arm.moment + self.cw.moment)
        except AttributeError:
            return self.arm.moment
            
    def hasCW(self):
        return self.cw is not None

#For a particular system, get the torque requirement of the motor
def getTorqueRequirement(load_torque, moi, drive, max_angular_v, SAFETY_FACTOR):
    f_max = drive.angularv_to_steprate(max_angular_v)
    Tload = load_torque
    Taccel = ((drive.motor.rotor_inertia * pow(drive.gearing, 2)) + moi) * drive.rads_per_step * pow(f_max,2)
    Ttotal = (Tload + Taccel + drive.motor.detent_torque) * SAFETY_FACTOR
    return (Tload , Taccel, Ttotal)

def printSummary(sys, iss, drive):

    max_angular_v = iss.max_angular_velocity
    arm = sys.arm
    f_max = drive.angularv_to_steprate(max_angular_v)
    
    arm_data_string = "Arm of weight %.1fkg, length %.1fm (moment %.1fkgm)." % (arm.weight_kg, arm.length_m, arm.moment)
    if (sys.hasCW()):
        cw_string_1 = "Stabilised by mass of %.1fkg at %.1fm (system moment %0.1fkgm)." % (sys.cw.mass, sys.cw.loc, sys.LoadMoment)
        cw_string_2 = "Moments of inertia (kgm^2): Arm=%0.1f, CW=%0.1f, Total=%0.1f." % ( sys.ArmMOI, sys.CwMOI, sys.TotalMOI)
    else:
        cw_string_1 = "System has no counterweight."
        cw_string_2 = "Moments of inertia (kgm^2): Arm=%0.1f, Total=%0.1f." % ( sys.ArmMOI, sys.TotalMOI)

    print """
    %s
    %s
    %s
    Maximum ISS angular velocity %.1f deg/s -> %.1f steps per second
    Safety factor = %d
    Required torque is (%.1fkgcm + %.1fkgcm) * %d * %0.1f = %.1f kgcm (%.1fNm)
    Motor max. torque is %.1fkgm
    Drive details: """ % (
    arm_data_string,
    cw_string_1,
    cw_string_2,
    math.degrees(iss.max_angular_velocity),
    f_max,
    SAFETY_FACTOR,
    kgm_to_kgcm(torque[0]), kgm_to_kgcm(torque[1]), SAFETY_FACTOR, drive.stepping_safety_factor, kgm_to_kgcm(torque[2]), torque[2]*G,
    drive.motor.getMaxTorque
    )
    for s in drive.getDetails():
        print "\t%s" % s

if __name__ == "__main__":

    # Define the system components
    iss = ISS()    
    arm = Arm(1.2, 0.15, 0.012, 900)
    cw = CW(1, 1.1)

    # Integrate these components into a mass system
    sys = MassSystem(arm, cw)

    ## These are the drives to choose from
    drives = [
        Drive(Motor("3325_0 (43.74)", 200, 50, 150, 18000), 1, 5.18),
        Drive(Motor("3318_1 (42.00)", 200, 50, 150, 30000), 1, 26.85),
        Drive(Motor("3319_1 (49.20)", 200, 50, 150, 40000), 1, 99.51),
        
        Drive(Motor("3307_0 (34.99)", 200, 50, 150, 12500), 4, 1),
        Drive(Motor("3331_0 (21.86)", 200, 50, 150, 11000), 4, 1),
        Drive(Motor("3303_0 (16.40)", 200, 50, 150, 4800), 4, 1),
        
        Drive(Motor("3302_0 (16.40)", 400, 50, 150, 4800), 2, 1),
        Drive(Motor("3330_0 (30.61)", 400, 50, 150, 11200), 2, 1),      
    ]
    
    for drive in drives:
        torque = getTorqueRequirement(sys.LoadMoment, sys.TotalMOI, drive, iss.max_angular_velocity, SAFETY_FACTOR)
        motor = drive.motor
        
        if (motor.meetsTorqueRequirement(torque[2])):
            print "\nDrive %s meets requirement %0.1fkgcm with max of %0.1fkgcm. Drive details:" % (motor.name, kgm_to_kgcm(torque[2]), kgm_to_kgcm(motor.getMaxTorque))
            for s in drive.getDetails():
                print "\t%s" % s
        #else:
        #    print "\nDrive %s does not meet requirement %0.1fkgcm with max of %0.1fkgcm. Drive details:" % (motor.name, kgm_to_kgcm(torque[2]), kgm_to_kgcm(motor.getMaxTorque))
        #    for s in drive.getDetails():
        #        print "\t%s" % s
    #drive = drives[5]
    #torque = getTorqueRequirement(sys.LoadMoment, sys.TotalMOI, drive, iss.max_angular_velocity, SAFETY_FACTOR)
    #printSummary(sys, iss, drive)
    