import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sympy import *
from scipy.optimize import fsolve
from Utils.helper_functions import *

# Solve the bicycle problem for a turn of given radius 
def get_turning_values(Vehicle, velocity, radius): 
    get_base_normal(Vehicle)
    for wheel in Vehicle.wheels.values(): 
        get_cornering_stiffness(wheel, wheel.pressure)
        get_RRcoeff(wheel, wheel.camber)
        wheel.fLongitudinal = wheel.RRcoeff * wheel.fNormal
    R = radius
    Xg = Vehicle.COG[0]
    Fc = Vehicle.total_mass * velocity ** 2 / R #centripetal contribution
    L = Vehicle.wheelbase
    Cf = (Vehicle.frontl.cornering_stiffness + Vehicle.frontr.cornering_stiffness) / 2
    Cr = Vehicle.rear.cornering_stiffness
    Fxf = (Vehicle.frontl.fLongitudinal + Vehicle.frontr.fLongitudinal) / 2
    Fxr = Vehicle.rear.fLongitudinal
    delta, alphaf, alphar, beta, e, fflateral, rflateral, T = symbols('delta, alphaf, alphar, beta, e, fflateral, rflateral, T')
    def func(x): 
        return [np.sin(x[3]) - (Xg - x[4])/R,
                np.tan(x[0] - x[1])-(L-x[4]) / (R * np.cos(x[3])),
                np.tan(x[2]) - x[4]/(R * np.cos(x[3])),
                x[5] - Cf * np.degrees(x[1]), 
                x[6] - Cr * np.degrees(x[2]),
                x[7] - Fxr - Fxf * np.cos(x[0]) + Fc * np.sin(x[3]) -x[5] * np.sin(x[0]),
                x[6] - Fxf * np.sin(x[0]) - Fc * np.cos(x[3]) +x[5] * np.cos(x[0]),
                -Xg * x[6] + (L - Xg) * (x[5] * np.cos(x[0]) - Fxf * np.sin(x[0]))]
    turning_values = fsolve(func, [0.1, 0.005, 0.005, 0.05, 1, 50, 50, 1])
    delta = turning_values[0]
    alphaf = turning_values[1]
    alphar = turning_values[2]
    beta = turning_values[3]
    e = turning_values[4]
    fflateral = turning_values[5]
    rflateral = turning_values[6]
    T = turning_values[7]