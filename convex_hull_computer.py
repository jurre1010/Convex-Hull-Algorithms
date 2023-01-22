import matplotlib.pyplot as plt
from copy import copy
from random import random
from functools import cmp_to_key

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "\n (% s, % s)" % (self.x, self.y)

    def __str__(self):
        return "(% s, % s)" % (self.x, self.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y-other.y)


def generate_points(n, a, d):
    points = []
    for i in range(n):
        points.append(Point(x = round(a * random(), ndigits=d), y = round(a * random(), ndigits=d)))
    return points

def show_points(points, a, hull_points):
    x = []
    y = []
    for i in range(len(points)):
        x.append(points[i].x)
        y.append(points[i].y)
    plt.scatter(x, y)
    plt.xlim(0, a)
    plt.ylim(0, a)

    hx = []
    hy = []
    for i in hull_points:
        hx.append(i.x)
        hy.append(i.y)
    plt.scatter(hx, hy, color="orange")
    plt.plot(hx, hy, color="orange")

    plt.show()

p0 = Point(0, 0)

def nextToTop(S):
    return S[-2]

def distSq(p1, p2):
    return ((p1.x - p2.x) * (p1.x - p2.x) +
            (p1.y - p2.y) * (p1.y - p2.y))

def orientation(p, q, r):
    val = ((q.y - p.y) * (r.x - q.x) -
           (q.x - p.x) * (r.y - q.y))
    if val == 0:
        return 0  # collinear
    elif val > 0:
        return 1  # clock wise
    else:
        return 2  # counterclock wise

def compare(p1, p2):
    # return -1 when points are colinear and p2 > p1 or points are counterclock wise oriented
    o = orientation(p0, p1, p2)
    if o == 0:
        if distSq(p0, p2) >= distSq(p0, p1):
            return -1
        else:
            return 1
    else:
        if o == 2:
            return -1
        else:
            return 1

def convex_hull(points):
    n = len(points)

    points_on_convex_hull = []

    # Sort the points on y-coordinate and after that on x-coordinate. y[0] is bottom-most point.
    ymin = points[0].y
    minindex = 0
    for i in range(1, n):
        y = points[i].y
        if ((y < ymin) or
            (ymin == y and points[i].x < points[minindex].x)):
            ymin = points[i].y
            minindex = i

    points[0], points[minindex] = points[minindex], points[0]

    global p0
    p0 = points[0]

    # bottom-most point appended to convex hull.
    points_on_convex_hull.append(p0)

    # Sort resulting point on polar angle around y[0].
    sorted_points = sorted(points, key=cmp_to_key(compare))

    m = 1  # Initialize size of modified array
    for i in range(1, n):

        # Keep removing i while angle of i and i+1 is same
        # with respect to p0
        while ((i < n - 1) and
        (orientation(p0, sorted_points[i], sorted_points[i + 1]) == 0)):
            i += 1

        sorted_points[m] = sorted_points[i]
        m += 1  # Update size of modified array

        # If modified array of points has less than 3 points,
    # convex hull is not possible
    if m < 3:
        return

    # Create an empty stack and push first three points
    # to it.
    S = []
    S.append(sorted_points[0])
    S.append(sorted_points[1])
    S.append(sorted_points[2])

    # Process remaining n-3 points
    for i in range(3, m):

        # Keep removing top while the angle formed by
        # points next-to-top, top, and points[i] makes
        # a non-left turn
        while ((len(S) > 1) and
        (orientation(nextToTop(S), S[-1], sorted_points[i]) != 2)):
            S.pop()
        S.append(sorted_points[i])

    # Now stack has the output points,
    # print contents of stack
    while S:
        p = S[-1]
        points_on_convex_hull.append(p)
        S.pop()

    return sorted_points, points_on_convex_hull

def check_convex_hull(points, points_on_convex_hull):
    check_points_from_set = len(points_on_convex_hull) == (len([p for p in points_on_convex_hull if p in points]))

    # check if all points from the original set are to the right
    check = True
    for i in range(len(points_on_convex_hull) - 1):
        for p in [p for p in points if p not in points_on_convex_hull]:
            check = check and orientation(points_on_convex_hull[i], points_on_convex_hull[i+1], p) == 1

    return check_points_from_set and check

def main():
    points = generate_points(10, 10, 1)
    sorted_points, points_on_convex_hull = convex_hull(points)
    print(check_convex_hull(list(reversed(sorted_points)), points_on_convex_hull))
    show_points(points, 10, points_on_convex_hull)

if __name__== "__main__":
    main()
