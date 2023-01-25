import json
from math import sqrt
import time
import convex_hull_graham as ch
from copy import copy

points_on_convex_hull = []

def quickhull(pts):
  # remove duplicates
  pts = list(set(pts))

  # get left- and rightmost points
  l = min(pts, key=lambda k: k.x)
  r = max(pts, key=lambda k: k.x)
  pts.remove(l), pts.remove(r)

  #split points in two; top and bottom. anything colinear can be discarded
  top_pts = [p for p in pts if ch.orientation(l,r,p) == 2] # to the left of the line
  bot_pts = [p for p in pts if ch.orientation(l,r,p) == 1] # to the right of the line

  conshull(top_pts, l, r)
  conshull(bot_pts, r, l)

  # close the chain
  points_on_convex_hull.append(l)

def conshull(pts, l, r):
  if len(pts) == 0:
    # if we won't recurse any further, add only the leftmost point
    # the rightmost point will be added as another left later and the
    # last will be added in the caller-function
    points_on_convex_hull.append(l)
    return

  # distance from point p to line segment l-r
  lineDist = lambda p: abs(((r.x-l.x)*(l.y-p.y))-((l.x-p.x)*(r.y-l.y)))

  # furthest point from the line segment
  c = max(pts, key=lineDist)

  # remove any points in pts that are contained by triangel lrc
  pts = [p for p in pts if p != c and not pt_in_triangle(l, c, r, p)]

  # get the points to the right of line segments, also include colinear points
  pts_1 = [p for p in pts if ch.orientation(l,c,p) == 2]
  pts_2 = [p for p in pts if ch.orientation(c,r,p) == 2]

  conshull(pts_1, l, c)
  conshull(pts_2, c, r)

# could consider barycentric check but might be harder to prove
# require cw winding, checks for all lines if point is to the right
def pt_in_triangle(x,y,z,p):
  d1 = ch.orientation(x,y,p) == 1
  d2 = ch.orientation(y,z,p) == 1
  d3 = ch.orientation(z,x,p) == 1
  return d1 and d2 and d3

def main():
  # issues: colinear points, duplicate points

  # 4 colinear:
  # jss = r'[{"x": 6.1, "y": 5.7}, {"x": 4.2, "y": 0.6}, {"x": 4.9, "y": 1.1}, {"x": 1.5, "y": 1.8}, {"x": 5.3, "y": 3.5}, {"x": 3.1, "y": 4.4}, {"x": 8.7, "y": 5.6}, {"x": 8.6, "y": 3.1}, {"x": 5.8, "y": 7.0}, {"x": 8.9, "y": 4.5}, {"x": 2.4, "y": 2.9}, {"x": 1.5, "y": 6.4}, {"x": 1.9, "y": 3.6}, {"x": 0.7, "y": 8.5}, {"x": 4.5, "y": 4.4}, {"x": 6.5, "y": 5.4}, {"x": 10.0, "y": 2.0}, {"x": 8.5, "y": 4.5}, {"x": 8.1, "y": 9.8}, {"x": 7.2, "y": 1.4}, {"x": 0.5, "y": 1.4}, {"x": 4.2, "y": 1.1}, {"x": 5.8, "y": 0.4}, {"x": 0.6, "y": 2.9}, {"x": 5.2, "y": 1.1}, {"x": 5.0, "y": 6.4}, {"x": 3.7, "y": 8.7}, {"x": 4.4, "y": 1.8}, {"x": 4.4, "y": 4.1}, {"x": 3.1, "y": 10.0}, {"x": 5.6, "y": 9.4}, {"x": 9.7, "y": 9.5}, {"x": 9.0, "y": 1.5}, {"x": 2.2, "y": 1.2}, {"x": 5.0, "y": 6.9}, {"x": 3.5, "y": 1.1}, {"x": 5.3, "y": 4.4}, {"x": 1.4, "y": 9.3}, {"x": 3.3, "y": 3.5}, {"x": 6.6, "y": 4.5}, {"x": 8.9, "y": 9.2}, {"x": 4.3, "y": 6.8}, {"x": 4.8, "y": 4.0}, {"x": 0.4, "y": 1.9}, {"x": 4.8, "y": 9.0}, {"x": 6.9, "y": 6.1}, {"x": 1.1, "y": 0.3}, {"x": 7.1, "y": 0.9}, {"x": 4.0, "y": 2.8}, {"x": 8.8, "y": 4.5}, {"x": 2.7, "y": 4.0}, {"x": 3.0, "y": 5.4}, {"x": 5.9, "y": 8.1}, {"x": 6.7, "y": 6.4}, {"x": 9.3, "y": 9.5}, {"x": 2.5, "y": 6.0}, {"x": 6.9, "y": 7.2}, {"x": 6.5, "y": 6.2}, {"x": 3.8, "y": 0.6}, {"x": 0.8, "y": 6.7}, {"x": 2.7, "y": 8.4}, {"x": 2.9, "y": 9.2}, {"x": 4.4, "y": 7.9}, {"x": 3.7, "y": 3.1}, {"x": 5.7, "y": 6.7}, {"x": 9.2, "y": 10.0}, {"x": 0.4, "y": 0.2}, {"x": 8.7, "y": 6.0}, {"x": 9.3, "y": 0.4}, {"x": 1.4, "y": 4.9}, {"x": 7.5, "y": 3.6}, {"x": 9.4, "y": 7.4}, {"x": 8.0, "y": 1.6}, {"x": 7.3, "y": 3.0}, {"x": 7.4, "y": 9.9}, {"x": 8.0, "y": 3.1}, {"x": 6.5, "y": 1.4}, {"x": 8.8, "y": 10.0}, {"x": 7.5, "y": 1.4}, {"x": 6.9, "y": 10.0}, {"x": 5.3, "y": 7.6}, {"x": 6.3, "y": 8.3}, {"x": 2.0, "y": 7.8}, {"x": 7.0, "y": 7.1}, {"x": 3.1, "y": 8.7}, {"x": 3.4, "y": 9.8}, {"x": 3.8, "y": 7.5}, {"x": 0.5, "y": 3.2}, {"x": 9.4, "y": 5.4}, {"x": 9.3, "y": 3.0}, {"x": 2.4, "y": 4.8}, {"x": 2.0, "y": 5.4}, {"x": 6.0, "y": 8.5}, {"x": 3.4, "y": 7.0}, {"x": 8.8, "y": 8.5}, {"x": 7.2, "y": 6.0}, {"x": 4.7, "y": 3.7}, {"x": 9.9, "y": 5.2}, {"x": 4.1, "y": 3.7}, {"x": 6.6, "y": 6.5}]'

  # points = json.loads(jss, object_hook=lambda d:ch.Point(d['x'], d['y']))

  # check = True
  # while check:
  #   points_on_convex_hull.clear()
  #   points = ch.generate_points(100, 10, 1)

  #   quickhull(copy(points))
  #   check = ch.check_convex_hull(points, points_on_convex_hull)

  # points = ch.generate_points(100, 10, 1)
  # quickhull(copy(points))

  # ch.show_points(points, 10, points_on_convex_hull)

  ns = [1000,2500,10000,25000,100000,250000,1000000]
  # ns = [10, 100, 1000]
  for n in ns:
      total_time = []
      for _ in range(10):
          points = ch.generate_points(n, 1000000, 1)

          start_time = time.time()
          quickhull(points)
          run_time = time.time() - start_time

          total_time.append(run_time)

      average_time = sum(total_time)/len(total_time)
      print("For {} points, the total time average is: {} seconds".format(n, round(average_time, ndigits=6)))


if __name__== "__main__":
    main()
