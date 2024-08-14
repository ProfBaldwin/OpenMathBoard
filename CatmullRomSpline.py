import numpy as np


def catmullRomSpline(
        P, 
        num_points: int = 10,
        half_alpha: float = 0.25,
        ):
    """
    Calculate the Catmull-Rom spline through four control points and returns the points on the
    portion of the spline through the center two points.
    Inputs:

    P - An m x 4 numpy array containing the four m-dimensional column vectors representing the
    four control points, in order. P[:, j] is the jth control point.

    num_points - The number of points on the spline to output.

    half_alpha - 0.25 for the centripetal spline, 0.0 for the uniform spline, 0.5 for the chordal
    spline. We save a calculation step by taking half_alpha instead of alpha.

    returns - An m x num_points matrix with the columns as points on the spline.
    """

    s = np.zeros((4, 1))
    Pdiff = P[:, 1:] - P[:, :-1]
    s[1:, 0] = np.einsum("ij, ij -> j", Pdiff, Pdiff)
    s = np.cumsum(s, axis = 0)

    t = np.linspace(s[1, 0], s[2, 0], num_points)

    A = np.empty((3, len(P), num_points))
    sdiffA = s[1:] - s[:-1]
    A = np.einsum("ij, jk -> jik", P[:, :-1], (s[1:] - t)/sdiffA) \
            + np.einsum("ij, jk -> jik", P[:, 1:], (t - s[:-1])/sdiffA)

    B = np.empty((2, len(P), num_points))
    sdiffB = s[2:] - s[:-2]
    B = np.einsum("ij, ikj -> ikj", (s[2:] - t)/sdiffB, A[:-1]) \
            + np.einsum("ij, ikj -> ikj", (t - s[:-2])/sdiffB, A[1:])

    C = np.empty((len(P), num_points))
    sdiffC = s[2] - s[1]
    C = np.einsum("j, ij -> ij", (s[2] - t)/sdiffC, B[0]) \
            + np.einsum("j, ij -> ij", (t - s[1])/sdiffC, B[1])

    return C
