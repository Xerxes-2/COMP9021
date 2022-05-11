# Written by Shupeng Xue for COMP9021
#
# At stage 0, start with a toothpick centered at (0, 0).
# There is a free tip at the top, at coordinates (0, 2),
# and a free tip at the bottom, at coordinates (0, -2):
# 
#         *
#         *
#         *
#         *
#         *
#         
# At stage 1, perpendically place toothpicks on those tips.
# So there are now 3 toothpicks and 4 free tips,
# a top left one at coordinates (-2, 2),
# a top right one at coordinates (2, 2),
# a bottom left one at coordinates (-2, -2), and
# a bottom right one at coordinates (2, -2):
# 
#     * * * * *
#         *
#         *
#         *
#     * * * * *
#     
# At stage 2, perpendically place toothpicks on those tips.
# So there are now 7 toothpicks and 4 free tips,
# a top left one at coordinates (-2, 4),
# a top right one at coordinates (2, 4),
# a bottom left one at coordinates (-2, -4), and
# a bottom right one at coordinates (2, -4):
# 
# 
#     *       * 
#     *       *
#     * * * * *
#     *   *   *
#     *   *   *
#     *   *   *
#     * * * * *
#     *       *
#     *       *
# 
# Implements a function
# tooth_picks(stage, top_left_corner, bottom_right_corner)
# that displays, using black and white squares,
# that part of the plane that fits in a rectangle
# whose top left and bottom right corners are provided by the
# second and third arguments, respectively, at the stage of the
# construction provided by the first argument.
# You can assume that stage is any integer between 0 and 1000;
# top_left_corner and bottom_right_corner are arbitrary pairs
# of integers, but practically such that the output can fit
# on the screen.
# 
# For a discussion about the construction, see
# https://www.youtube.com/watch?v=_UtCli1SgjI&t=66s
# The video also points to a website that you might find useful:
# https://oeis.org/A139250/a139250.anim.html


# Written by *** for COMP9021
#
# At stage 0, start with a toothpick centered at (0, 0).
# There is a free tip at the top, at coordinates (0, 2),
# and a free tip at the bottom, at coordinates (0, -2):
#
#         *
#         *
#         *
#         *
#         *
#
# At stage 1, perpendically place toothpicks on those tips.
# So there are now 3 toothpicks and 4 free tips,
# a top left one at coordinates (-2, 2),
# a top right one at coordinates (2, 2),
# a bottom left one at coordinates (-2, -2), and
# a bottom right one at coordinates (2, -2):
#
#     * * * * *
#         *
#         *
#         *
#     * * * * *
#
# At stage 2, perpendically place toothpicks on those tips.
# So there are now 7 toothpicks and 4 free tips,
# a top left one at coordinates (-2, 4),
# a top right one at coordinates (2, 4),
# a bottom left one at coordinates (-2, -4), and
# a bottom right one at coordinates (2, -4):
#
#
#     *       *
#     *       *
#     * * * * *
#     *   *   *
#     *   *   *
#     *   *   *
#     * * * * *
#     *       *
#     *       *
#
# Implements a function
# tooth_picks(stage, top_left_corner, bottom_right_corner)
# that displays, using black and white squares,
# that part of the plane that fits in a rectangle
# whose top left and bottom right corners are provided by the
# second and third arguments, respectively, at the stage of the
# construction provided by the first argument.
# You can assume that stage is any integer between 0 and 1000;
# top_left_corner and bottom_right_corner are arbitrary pairs
# of integers, but practically such that the output can fit
# on the screen.
#
# For a discussion about the construction, see
# https://www.youtube.com/watch?v=_UtCli1SgjI&t=66s
# The video also points to a website that you might find useful:
# https://oeis.org/A139250/a139250.anim.html
"""Program for Python Quiz 3"""


def free_tip_1(free_tip, stage):
    """first new free tip from old"""
    return (free_tip[0] + 2*(stage % 2), free_tip[1] + 2 - 2*(stage % 2))


def free_tip_2(free_tip, stage):
    """second new free tip from old"""
    return (free_tip[0] - 2*(stage % 2), free_tip[1] - 2 + 2*(stage % 2))


def tooth_picks(stage, top_left_corner, bottom_right_corner):
    """Main program"""
    free_tips = {(0, 0)}
    black_points = set()
    next_free_tips = set()  # free tips of next stage
    for current in range(stage+1):
        # dynamic x and y offset of current stage
        offset = [current % 2, 1-current % 2]
        for tip in free_tips:
            if free_tip_1(tip, current) in next_free_tips:
                next_free_tips.remove(free_tip_1(tip, current))
            else:
                if free_tip_1(tip, current) not in black_points:
                    next_free_tips.add(free_tip_1(tip, current))
            if free_tip_2(tip, current) in next_free_tips:
                next_free_tips.remove(free_tip_2(tip, current))
            else:
                if free_tip_2(tip, current) not in black_points:
                    next_free_tips.add(free_tip_2(tip, current))
            for i in range(-2, 3):
                # draw black points
                black_points.add((tip[0]+i*offset[0], tip[1]+i*offset[1]))
        free_tips.clear()
        free_tips.update(next_free_tips)
        next_free_tips.clear()
    for i in range(top_left_corner[1], bottom_right_corner[1]-1, -1):
        for j in range(top_left_corner[0], bottom_right_corner[0]+1):
            if (j, i) in black_points:
                print('\N{black large square}', end='')
            else:
                print('\N{white large square}', end='')
        print()
    return
