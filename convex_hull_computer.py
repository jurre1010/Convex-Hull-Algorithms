import json
import time
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

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

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
    plt.xlim(-1, a + 1)
    plt.ylim(-1, a + 1)

    hx = []
    hy = []
    for i in hull_points:
        hx.append(i.x)
        hy.append(i.y)
    plt.scatter(hx, hy, color="orange")
    plt.plot(hx, hy, color="orange")

    is_convex_hull = check_convex_hull(points, hull_points)
    plt.title("Is convex hull: {}".format(is_convex_hull))

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
    not_ch_points = [p for p in points if p not in points_on_convex_hull]
    check = True

    for i in range(len(points_on_convex_hull) - 1):
        for p in not_ch_points:
            if orientation(points_on_convex_hull[i], points_on_convex_hull[i+1], p) != 2:
                continue # if it's colinear or to the right; accept
            print("Error: orientation of point ({}) incorrect! Orientation: {} with {} and {}".format(p, orientation(points_on_convex_hull[i], points_on_convex_hull[i+1], p), points_on_convex_hull[i], points_on_convex_hull[i+1]))
            check = False

    if not check:
        dmp = list(map(vars, points))
        print(json.dumps(dmp))

    return check_points_from_set and check
def main():
    # Error: orientation of point ((9.9, 9.3)) incorrect! Orientation: 2 with (9.8, 9.9) and (10.0, 5.2)
    # jss = r'[{"x": 0.7, "y": 0.1}, {"x": 8.4, "y": 7.7}, {"x": 7.7, "y": 9.3}, {"x": 3.4, "y": 6.1}, {"x": 6.6, "y": 6.5}, {"x": 5.6, "y": 0.8}, {"x": 7.2, "y": 5.8}, {"x": 0.5, "y": 9.7}, {"x": 7.2, "y": 0.8}, {"x": 1.9, "y": 1.7}, {"x": 6.4, "y": 7.8}, {"x": 6.5, "y": 6.9}, {"x": 4.1, "y": 1.6}, {"x": 9.2, "y": 0.6}, {"x": 5.5, "y": 3.3}, {"x": 9.9, "y": 9.3}, {"x": 2.6, "y": 7.1}, {"x": 6.5, "y": 5.2}, {"x": 9.5, "y": 3.3}, {"x": 2.1, "y": 3.0}, {"x": 2.3, "y": 8.9}, {"x": 1.0, "y": 7.0}, {"x": 6.2, "y": 9.0}, {"x": 10.0, "y": 5.2}, {"x": 3.5, "y": 7.7}, {"x": 9.0, "y": 1.4}, {"x": 9.8, "y": 7.4}, {"x": 8.6, "y": 7.9}, {"x": 1.1, "y": 1.5}, {"x": 0.7, "y": 4.2}, {"x": 8.0, "y": 4.3}, {"x": 2.4, "y": 1.1}, {"x": 3.7, "y": 10.0}, {"x": 4.4, "y": 9.6}, {"x": 8.3, "y": 6.5}, {"x": 3.0, "y": 8.8}, {"x": 5.2, "y": 6.6}, {"x": 9.3, "y": 4.6}, {"x": 3.5, "y": 0.2}, {"x": 2.6, "y": 4.0}, {"x": 0.1, "y": 1.1}, {"x": 3.0, "y": 1.3}, {"x": 4.0, "y": 5.5}, {"x": 2.9, "y": 0.8}, {"x": 1.4, "y": 2.5}, {"x": 1.5, "y": 1.1}, {"x": 4.4, "y": 1.8}, {"x": 9.8, "y": 9.9}, {"x": 9.1, "y": 6.6}, {"x": 5.5, "y": 4.9}, {"x": 4.4, "y": 8.3}, {"x": 4.9, "y": 7.3}, {"x": 6.2, "y": 3.3}, {"x": 6.8, "y": 4.1}, {"x": 5.4, "y": 2.4}, {"x": 9.2, "y": 4.7}, {"x": 1.8, "y": 0.1}, {"x": 5.2, "y": 3.9}, {"x": 4.8, "y": 2.6}, {"x": 9.5, "y": 5.3}, {"x": 6.5, "y": 8.0}, {"x": 9.5, "y": 8.3}, {"x": 8.4, "y": 9.1}, {"x": 9.6, "y": 6.3}, {"x": 6.4, "y": 6.6}, {"x": 1.1, "y": 4.2}, {"x": 1.6, "y": 6.6}, {"x": 5.8, "y": 7.2}, {"x": 1.2, "y": 9.5}, {"x": 8.8, "y": 6.4}, {"x": 6.0, "y": 0.6}, {"x": 7.6, "y": 2.2}, {"x": 2.0, "y": 7.3}, {"x": 4.5, "y": 3.2}, {"x": 3.0, "y": 8.4}, {"x": 2.0, "y": 8.4}, {"x": 8.4, "y": 1.8}, {"x": 8.8, "y": 5.3}, {"x": 2.1, "y": 3.9}, {"x": 8.4, "y": 4.3}, {"x": 9.6, "y": 1.2}, {"x": 5.8, "y": 3.4}, {"x": 0.0, "y": 6.6}, {"x": 4.3, "y": 9.0}, {"x": 8.0, "y": 2.5}, {"x": 2.0, "y": 0.7}, {"x": 6.0, "y": 8.9}, {"x": 1.5, "y": 5.2}, {"x": 1.6, "y": 6.6}, {"x": 9.5, "y": 1.4}, {"x": 1.0, "y": 1.2}, {"x": 4.1, "y": 4.1}, {"x": 0.0, "y": 4.8}, {"x": 4.2, "y": 2.8}, {"x": 7.9, "y": 0.5}, {"x": 6.4, "y": 1.4}, {"x": 2.0, "y": 2.3}, {"x": 7.5, "y": 1.4}, {"x": 7.2, "y": 1.4}, {"x": 0.5, "y": 4.2}]'

    # points = json.loads(jss, object_hook=lambda d:Point(d['x'], d['y']))

    n = 1000000
    total_time = []
    for _ in range(10):
        points = generate_points(n, 1000000, 1)

        start_time = time.time()
        convex_hull(points)
        run_time = time.time() - start_time

        total_time.append(run_time)

    average_time = sum(total_time)/len(total_time)
    print("The total time average is: % s seconds" % round(average_time, ndigits=6))


if __name__== "__main__":
    main()
