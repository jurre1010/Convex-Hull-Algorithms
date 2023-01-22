import convex_hull_computer as ch
from copy import copy

def quickhull():
  return ""

def main():
    points = ch.generate_points(10, 10, 1)
    sorted_points, points_on_convex_hull = ch.convex_hull(points)
    print(ch.check_convex_hull(list(reversed(sorted_points)), copy(points_on_convex_hull)))
    ch.show_points(points, 10, points_on_convex_hull)

if __name__== "__main__":
    main()
