import xpc
import threading
import time
import sys
sys.setrecursionlimit(360000)       # Program can run in an hour

class Simulation:
    drefs = ["sim/flightmodel/position/latitude",  # Latitude in degrees
             "sim/flightmodel/position/longitude",  # Longitude in degrees
             "sim/flightmodel/position/elevation",  # Altitude in meter(Mean Sea Level)
             "sim/flightmodel/position/phi",  # Roll in degrees
             "sim/flightmodel/position/theta",  # Pitch in degrees
             "sim/flightmodel/position/psi",  # Heading in degrees
             "sim/flightmodel/position/P",  # Roll rates in deg/s
             "sim/flightmodel/position/Q",  # Pitch rates in deg/s
             "sim/flightmodel/position/R",  # Yaw rates in deg/s
             "sim/flightmodel/position/P_dot",  # Roll acceleration in deg/s^2
             "sim/flightmodel/position/Q_dot",  # Pitch acceleration in deg/s^2
             "sim/flightmodel/position/R_dot",  # Yaw acceleration in deg/s^2
             "sim/flightmodel/position/local_vx",  # Velocity of X axis in m/s
             "sim/flightmodel/position/local_vy",  # Velocity of Y axis in m/s
             "sim/flightmodel/position/local_vz"]  # velocity of Z axis in m/s

    def __init__(self):
        pass

    def Xplane(self):
        with xpc.XPlaneConnect() as client:
            while True:
                #start = time.time()
                '''
                drefs = ["sim/flightmodel/position/latitude",  # Latitude in degrees
                         "sim/flightmodel/position/longitude",  # Longitude in degrees
                         "sim/flightmodel/position/elevation",  # Altitude in meter(Mean Sea Level)
                         "sim/flightmodel/position/phi",  # Roll in degrees
                         "sim/flightmodel/position/theta",  # Pitch in degrees
                         "sim/flightmodel/position/psi",  # Heading in degrees
                         "sim/flightmodel/position/P",  # Roll rates in deg/s
                         "sim/flightmodel/position/Q",  # Pitch rates in deg/s
                         "sim/flightmodel/position/R",  # Yaw rates in deg/s
                         "sim/flightmodel/position/P_dot",  # Roll acceleration in deg/s^2
                         "sim/flightmodel/position/Q_dot",  # Pitch acceleration in deg/s^2
                         "sim/flightmodel/position/R_dot",  # Yaw acceleration in deg/s^2
                         "sim/flightmodel/position/local_vx",  # Velocity of X axis in m/s
                         "sim/flightmodel/position/local_vy",  # Velocity of Y axis in m/s
                         "sim/flightmodel/position/local_vz"]  # velocity of Z axis in m/s
                '''

                values = client.getDREFs(self.drefs)

                print("Roll: {}, Pitch: {}, Yaw: {}, P: {}, Q: {}, R: {}".format(values[3][0], values[4][0], values[5][0],
                                                                               values[6][0], values[7][0],
                                                                               values[8][0]))
                data = [[8, 0, 0, 0, -998.0, -998.0, -998.0, -998.0, -998.0]]
                client.sendDATA(data)
                '''
                controlvalues = [8, 0, 0, 0, 0]
                client.getDATA()
                '''



                #threading.Timer(0.02, self.Xplane()).start()
                #end = time.time()
                #print("FPS: {}".format(1 / (end - start)))


def main():
    print("START")
    simulation = Simulation()
    simulation.Xplane()






if __name__ == "__main__":
    main()