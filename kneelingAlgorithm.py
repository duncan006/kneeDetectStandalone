#!/usr/bin/env python3

class kneelingDetection:
    def __init__(self, NMKG, mass):
        self.NMKG = NMKG
        self.mass = mass
        
        #Inputs updated on the first loop
        self.thighAngleR = 0
        self.shankAngleR = 0
        
        self.thighAngleL = 0
        self.shankAngleL = 0
        
        self.thighRAngV  = 0
        self.shankRAngV  = 0
        
        self.thighLAngV  = 0
        self.shankLAngV  = 0
        
        self.kneeAngleR = 0
        self.kneeAngleL = 0
        
        #Perpetual variables for kneelingDetection()
        self.movingAvgLen = 50
        self.movingAvgGyThighR = []
        self.movingAvgGyThighL = []
        self.Rcounter = 0
        self.Lcounter = 0
        self.isKneeling = False
        self.stdMultiplier = 2
        self.counterDetectionLimit = 2
        self.startingToStand = False
        self.legWasForward = "X"
        
        #Perpetual values for torqueEstimation()
        self.A = 0.012
        self.B = -0.002
        self.C = -0.075
        
        #torqueWindow()
        self.deliverTorque = False
        self.timeLastKneeling = time.time()
    
    
    
    
    
    
    
    #Main function to run for third party input and export
    def getTorque(self, thighAngleR, shankAngleR, thighAngleL, shankAngleL, thighRAngV, shankRAngV, thighLAngV, shankLAngV, kneeAngleR, kneeAngleL):
        
        self.thighAngleR = thighAngleR
        self.shankAngleR = shankAngleR
        
        self.thighAngleL = thighAngleL
        self.shankAngleL = shankAngleL
        
        self.thighRAngV  = thighRAngV
        self.shankRAngV  = shankRAngV
        
        self.thighLAngV  = thighLAngV
        self.shankLAngV  = shankLAngV
        
        self.kneeAngleR = kneeAngleR
        self.kneeAngleL = kneeAngleL
        
        legForward = self.kneelingDetection()
        
        
        if legForward == "R" or (time.time() - self.timeLastKneeling < .5 and legForward == "X"):
            torque = self.torqueEstimation(self.kneeAngleR, self.thighRAngV)
        else:
            torque = 0
            
        return torque
        
        
    
    
    
    
    
    
    
    
    def torqueEstimation(self, kneeAngle, angVel):
        #NMKG - Newton-meters per kilogram (for initial tests, 0.15, 0.30, 0.45)
        #mass - kilograms of subject
        #angVel and kneeAngle are for leg with device. angVel is for thigh.
        
        torqueOutput = (self.A * (180-kneeAngle)) + (self.B * angVel) + self.C
        torqueOutput = torqueOutput * self.NMKG * self.mass * (12/15)
        
        if self.torqueWindow():
            return torqueOutput
        else:
            return 0
    
    
    
    
    
    
    
    
    
    
    
    def torqueWindow(self):
        import time
        if self.isKneeling == True or (time.time() - self.timeLastKneeling < .5 and self.kneeAngleR < 170):
            self.deliverTorque = True
            if self.isKneeling == True:
                self.timeLastKneeling = time.time()
        else:
            self.deliverTorque = False
            
        return self.deliverTorque
        
        
        
        
        
        
        
        
        
        
        
        
        
    def kneelingDetection(self):
        #Knee angles oriented with staight leg at 180 degrees
        
        import numpy as np
        
        kneelingGyLimit = 60
        
        legForward = ""
        
        
        
        
        
        
    #Calculate mean and standard deviation of gyroscope data outside of if statements so that moving array is not compromised.
        self.movingAvgGyThighR.append(self.thighRAngV)
        self.movingAvgGyThighL.append(self.thighLAngV)

        if len(self.movingAvgGyThighR) > self.movingAvgLen:
            self.movingAvgGyThighR.pop(0)
        if len(self.movingAvgGyThighL) > self.movingAvgLen:
            self.movingAvgGyThighL.pop(0)

        Rmean = np.mean(self.movingAvgGyThighR)
        Rsd = np.std(self.movingAvgGyThighR) * self.stdMultiplier
            
        Lmean = np.mean(self.movingAvgGyThighL)
        Lsd = np.std(self.movingAvgGyThighL) * self.stdMultiplier
        
        if Rsd < 5:
            Rsd = Rsd * 2
        if Lsd < 5:
            Lsd = Lsd * 2
            
        R_upper_limit = Rmean + Rsd
        R_lower_limit = Rmean - Rsd
        
        L_upper_limit = Lmean + Lsd
        L_lower_limit = Lmean - Lsd
        
        R_thighR_shankL_angV = self.shankLAngV - self.thighRAngV
        L_thighL_shankR_angV = self.shankRAngV - self.thighLAngV
        
        
        
        
        
    #Implement early kneeling down detection via gyroscopes
        
        
        
        
        
        
        
    #Test if angle is past a rather large and easy to determine threshold (60 degrees from straight)
    #re-work to use sum of angles for a closer detection
        if (self.kneeAngleL < 120) and (self.kneeAngleR < 120):
            self.isKneeling = True
        else:
            self.isKneeling = False
            legForward = "X"
            

            
            
            
    #Test which foot is forward (or if both are backwards) using the angle of the shin to the horizontal.
    #Leg with horizontal shin is backwards, if both shins horizontal then both legs down.
    #To expand for kneeling on an angle, use the difference between the shin angles with a window for how close they can be, and the lesser/greater one is forward once it passes the threshold
        
        if self.isKneeling == True:
            legForwardThreshold = 30
            if abs(self.shankAngleR - self.shankAngleL) < legForwardThreshold:
                legForward = "2"
            #deep flexion test
                #if (rightKneeAngle < 60) and (leftKneeAngle < 60):
                    #legForward += "d"
            else:
                if self.shankAngleL > self.shankAngleR:
                    legForward = "L"
                    self.legWasForward = "L"
                elif self.shankAngleR > self.shankAngleL:
                    legForward = "R"
                    self.legWasForward = "R"
                    
                    
                    
                    
                    

#Detect a spike as the moment that the subject starts to stand up.
            if (self.thighRAngV < R_lower_limit) and (R_thighR_shankL_angV > R_upper_limit) and len(self.movingAvgGyThighR) > 20:
                #self.movingAvgGyThighR.pop(len(self.movingAvgGyThighR)-1)
                self.Rcounter = self.Rcounter + 1
            else:
                self.Rcounter = 0
                
            if (self.thighLAngV < L_lower_limit) and (L_thighL_shankR_angV > L_upper_limit) and len(self.movingAvgGyThighL) > 20:
                #self.movingAvgGyThighL.pop(len(self.movingAvgGyThighL)-1)
                self.Lcounter = self.Lcounter + 1
            else:
                self.Lcounter = 0
               
            
            
            
            
#Check for consecutive signals before setting to "standing up" mode.
            if (self.Rcounter >= self.counterDetectionLimit and legForward == "R") or (self.Lcounter >= self.counterDetectionLimit and legForward == "L"):
                self.startingToStand = True
            #((self.Rcounter >=1 and self.Lcounter >=1) and legForward == "2")
            
        if self.startingToStand == True:
            if (self.legWasForward == "R" and self.kneeAngleR > 160) or (self.legWasForward == "L" and self.kneeAngleL > 160):
                self.startingToStand = False
                self.legWasForward = "X"
            #legForward += "s"
            
        return legForward
