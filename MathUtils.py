import numpy as np
import math

from Quaternion import Quaternion

def calculateQuaternion(v1, v2):
    cross_product = np.cross(v1, v2)
    n = -cross_product/np.linalg.norm(cross_product)

    # avoid upside-down
    # sign = np.cross([0, 1, 0], v2)[2]

    # q_norm = Quaternion(1, 0, 0, 0)
    # if sign < 0:
    #     q_norm = Quaternion(0, 1, 0, 0)
    # print(sign)

    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    q = Quaternion(np.cos(angle/2), *(np.sin(angle/2)*n))

    return q


def calculate_reflect_vector(v1, n):
    med = np.dot(v1, n)
    v2 = v1 - 2*med*n

    return v2
