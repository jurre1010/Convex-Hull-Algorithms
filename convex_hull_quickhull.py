from math import sqrt
import convex_hull_computer as ch
from copy import copy

points_on_convex_hull = []

def filter_proc(l,r,o):
  return lambda p: ch.orientation(l,r,p) == o

def quickhull(pts):
  n = len(pts)
  srt_pts = sorted(pts, key=lambda k: [k.x, k.y])

  # get left- and rightmost points
  l, r = srt_pts[0], srt_pts[-1]
  pts.remove(l), pts.remove(r)

  points_on_convex_hull.append(l),points_on_convex_hull.append(r)

  #split points in two; top and bottom. anything colinear can be discarded
  top_pts = [p for p in pts if ch.orientation(l,r,p) == 2]
  bot_pts = [p for p in pts if ch.orientation(l,r,p) == 1]

  conshull(top_pts, l, r)
  conshull(bot_pts, r, l)

  # close the chain
  points_on_convex_hull.insert(0,r)

def conshull(pts, l, r):
  if len(pts) == 0:
    return

  # distance from point p to line segment l-r
  dist = lambda p: abs(((r.x-l.x)*(l.y-p.y))-((l.x-p.x)*(r.y-l.y)))/sqrt(ch.distSq(r,l))

  c = max(pts, key=dist)

  points_on_convex_hull.insert(points_on_convex_hull.index(r), c)

  pts_1 = [p for p in pts if ch.orientation(l,c,p) == 2]
  pts_2 = [p for p in pts if ch.orientation(c,r,p) == 2]

  conshull(pts_1, l, c)
  conshull(pts_2, c, r)

def main():
    points = ch.generate_points(10, 10, 1)
    quickhull(copy(points))
    print(ch.check_convex_hull(points, points_on_convex_hull))
    ch.show_points(points, 10, points_on_convex_hull)

if __name__== "__main__":
    main()
