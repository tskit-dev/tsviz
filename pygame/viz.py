"""tskit TreeSequence visualization
"""

import argparse
import tskit
import pygame
from pygame.locals import *  # TODO: change to selective import
# import time
from sort import minlex

# TODO: change this to an Enum
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

click_hand_strings = (               #sized 24x24
  "     XX                 ",
  "    X..X                ",
  "    X..X                ",
  "    X..X                ",
  "    X..X                ",
  "    X..XXX              ",
  "    X..X..XXX           ",
  "    X..X..X..XX         ",
  "    X..X..X..X X        ",
  "XXX X..X..X..X..X       ",
  "X..XX........X..X       ",
  "X...X...........X       ",
  " X..X...........X       ",
  "  X.X...........X       ",
  "  X.............X       ",
  "   X............X       ",
  "   X...........X        ",
  "    X..........X        ",
  "    X..........X        ",
  "     X........X         ",
  "     X........X         ",
  "     XXXXXXXXXX         ",
  "                        ",
  "                        ")

parser = argparse.ArgumentParser(description='Visualize tskit TreeSequence\'s.')
parser.add_argument("--file", help="Path to .trees file (default None)",
    action="store", default=None)
parser.add_argument("--num_samples", help="Number of samples to simulate (default 20)",
    action="store", default=20, type=int)
parser.add_argument("--length", help="Simulation length (default 3e3)",
    action="store", default=3e3, type=float)
parser.add_argument("--seed", help="Random seed (default None)",
    action="store", default=None, type=int)
parser.add_argument("--sort", help="Whether to sort samples using minlex (1=True, 0=False, default 1)",
    action="store", default=1, type=int)
parser.add_argument("--fontsize", help="Font size for labels (default None, dynamically chosen)",
    action="store", default=None, type=int)
args = parser.parse_args()

print("Command-line args:")
args_to_print = vars(args)
for k in sorted(args_to_print):
    print(k + ": " + str(args_to_print[k]))

sort_samples = (args.sort != 0)

if args.file is not None:
    ts = tskit.load(args.file)
else:
    import msprime
    if args.seed is None:
        import random
        seed = random.randint(1, 1000) # inclusive
    else:
        seed = args.seed
    print("Your seed is", seed)
    ts = msprime.simulate(sample_size=args.num_samples, length=args.length, random_seed=seed,
        mutation_rate=1.65e-8, recombination_rate=1.2e-8, Ne=20000)
if args.fontsize is None:
    if ts.num_samples < 30:
        fontsize=20
    else:
        fontsize=10
else:
    fontsize = args.fontsize

breakpoints = list(ts.breakpoints())
variants = list(ts.variants())
trees = ts.aslist()
max_height = max([tree.time(tree.root) for tree in trees])
print("Max height:", max_height)
print("Genome length:", ts.sequence_length)
print("Navigate with the left / right arrow keys")
# print(ts.draw_text())
# print(pygame.font.get_fonts())

pygame.init()
width = 1000
height = 750
linewidth = 3
edgelinewidth = linewidth*2 - linewidth % 2
margin = 50
genome_height = 2*margin # showing genome, positioned at bottom
tree_index = 0 # starting tree index
tree_width = 700
tree_canvas_height = height-genome_height-2*margin
tree_height = tree_canvas_height - margin
font_space = 20
ticks_delay = 500 # number of ticks before starting to rapidly move
ticks_move = 50 # number of ticks for rapidly moving between trees

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
genome = pygame.Surface((width, genome_height), 0)
genome_offset = (0, height-genome_height)
tree_canvas = pygame.Surface((tree_width, tree_canvas_height), 0)
tree_offset = ((width - tree_width) // 2, margin)
click_cursor = pygame.cursors.compile(click_hand_strings)

pygame.display.set_caption('tskit TreeSequence visualization') 
running = True
first_pass = True
ready_for_move = True
ready_for_click = False
pressed_ticks = -1
last_moved_ticks = -1
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    if ready_for_move or ready_for_click or first_pass:
        action_taken = False
        if ready_for_move and not (pressed_keys[K_LEFT] and pressed_keys[K_RIGHT]):
            if pressed_keys[K_LEFT]:
                if pressed_ticks == -1:
                    pressed_ticks = pygame.time.get_ticks()
                last_moved_ticks = pygame.time.get_ticks()
                tree_index -= 1
                if tree_index < 0:
                    tree_index = 0
                else:
                    ready_for_move = False
                    action_taken = True
            if pressed_keys[K_RIGHT]:
                if pressed_ticks == -1:
                    pressed_ticks = pygame.time.get_ticks()
                last_moved_ticks = pygame.time.get_ticks()
                tree_index += 1
                if tree_index >= len(breakpoints) - 1:
                    tree_index = len(breakpoints) - 2
                else:
                    ready_for_move = False
                    action_taken = True
        if ready_for_click and pygame.mouse.get_pressed()[0]:
            # There has been a mouse click, let's check if it's in the right region
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (mouse_x >= margin and mouse_x <= width - margin) and (mouse_y >= genome_offset[1] + margin / 2 and mouse_y <= height - margin / 2):
                action_taken = True
                genome_pos = float(mouse_x - margin) / float(genome_extent) * breakpoints[-1]
                for i in range(1, len(breakpoints)):
                    if genome_pos < breakpoints[i]:
                        assert genome_pos >= breakpoints[i - 1]
                        tree_index = i - 1
                        break

        if action_taken or first_pass:
            print("Region ", tree_index, ", [", breakpoints[tree_index], ", ",
                  breakpoints[tree_index+1], ")", sep="")
            for v in variants:
                if breakpoints[tree_index] <= v.position and v.position < breakpoints[tree_index + 1]:
                    print("Genotypes ", v.genotypes.tolist(), " from mutation at ", v.position, sep="")
            node_x_dict = {}
            node_y_dict = {}
            node_parent_dict = {}
            tree = trees[tree_index]
            if sort_samples:  # Toggle me!
                samples = minlex(tree)
            else:
                samples = list(tree.samples())
            n = len(samples)
            for i, sample in enumerate(samples):
                node_x_dict[sample] = int(i / (n - 1) * (tree_width - 1))
                node_y_dict[sample] = 0

            def fill_tree_positions(tree, node):
                children = tree.children(node)
                if len(children) == 0:
                    return node_x_dict[node], node_x_dict[node]
                running_min = None
                running_max = None
                for child in children:
                    child_min, child_max = fill_tree_positions(tree, child)
                    if running_min is None:
                        running_min = child_min
                        running_max = child_max
                    else:
                        running_min = min(running_min, child_min)
                        running_max = max(running_max, child_max)
                    node_parent_dict[child] = node
                node_x_dict[node] = int((running_min + running_max) / 2)
                node_y_dict[node] = tree.time(node) / max_height * tree_height
                return running_min, running_max

            node_parent_dict[tree.root] = -1
            fill_tree_positions(tree, tree.root)
            first_pass = False

    if not pressed_keys[K_LEFT] and not pressed_keys[K_RIGHT]:
        ready_for_move = True
        pressed_ticks = -1

    if pressed_keys[K_LEFT] and pressed_keys[K_RIGHT]:
        ready_for_move = True
        pressed_ticks = -1

    if pressed_ticks != -1:
        if last_moved_ticks > pressed_ticks and pygame.time.get_ticks() > last_moved_ticks + ticks_move:
            ready_for_move = True
        if last_moved_ticks <= pressed_ticks and pygame.time.get_ticks() > pressed_ticks + ticks_delay:
            ready_for_move = True

    screen.fill(WHITE)
    genome.fill(WHITE)
    tree_canvas.fill(WHITE)
    pygame.draw.line(
        genome,
        BLACK,
        (margin, margin),
        (width - margin, margin),
        linewidth)
    genome_extent = width - 2*margin
    for i, b in enumerate(breakpoints):
        x = int(margin + genome_extent * (b / breakpoints[-1]))
        vertical_color = BLACK
        tick_size = margin // 2
        pygame.draw.line(
            genome,
            vertical_color,
            (x, margin - tick_size),
            (x, margin + tick_size),
            linewidth)
    # Go back and draw red vertical lines
    for i in [tree_index, tree_index + 1]:
        b = breakpoints[i]
        x = int(margin + genome_extent * (b / breakpoints[-1]))
        vertical_color = RED
        tick_size = margin // 2
        pygame.draw.line(
            genome,
            vertical_color,
            (x, margin - tick_size),
            (x, margin + tick_size),
            linewidth)
    for v in variants:
        if breakpoints[tree_index] <= v.position and v.position < breakpoints[tree_index + 1]:
            mutation_color = RED
        else:
            mutation_color = BLACK
        x = int(margin + genome_extent * (v.position / breakpoints[-1]))
        cross_size = margin // 6
        pygame.draw.line(
            genome,
            mutation_color,
            (x - cross_size, margin - cross_size),
            (x + cross_size, margin + cross_size),
            linewidth)
        pygame.draw.line(
            genome,
            mutation_color,
            (x + cross_size, margin - cross_size),
            (x - cross_size, margin + cross_size),
            linewidth)

    tree_start = int(margin + genome_extent * (breakpoints[tree_index] / breakpoints[-1]))
    tree_end = int(margin + genome_extent * (breakpoints[tree_index + 1] / breakpoints[-1]))
    pygame.draw.line(
        genome,
        RED,
        (tree_start, margin),
        (tree_end, margin),
        linewidth)

    screen.blit(genome, genome_offset)
    # tree_canvas.fill(GREEN)
    # Draw the marginal tree!
    for node in node_parent_dict:
        if node == tree.root:
            xpos = node_x_dict[node]
            ypos = node_y_dict[node]
            pygame.draw.line(
                tree_canvas,
                BLACK,
                (xpos, tree_canvas_height - ypos),
                (xpos, tree_canvas_height - ypos - margin),
                linewidth)
            pass
        else:
            xpos = node_x_dict[node]
            ypos = node_y_dict[node]
            parent_xpos = node_x_dict[node_parent_dict[node]]
            parent_ypos = node_y_dict[node_parent_dict[node]]
            edgeline = xpos == 0 or xpos == tree_width - 1
            special_width = edgelinewidth if edgeline else linewidth
            # vertical line
            pygame.draw.line(
                tree_canvas,
                BLACK,
                (xpos, tree_canvas_height - ypos),
                (xpos, tree_canvas_height - parent_ypos),
                special_width)
            # horizontal line
            pygame.draw.line(
                tree_canvas,
                BLACK,
                (xpos, tree_canvas_height - parent_ypos),
                (parent_xpos, tree_canvas_height - parent_ypos),
                linewidth)
    for v in tree.mutations():
        xpos = node_x_dict[v.node]
        ypos = (node_y_dict[v.node] + node_y_dict[node_parent_dict[v.node]]) // 2
        cross_size = margin // 6
        pygame.draw.line(
            tree_canvas,
            BLACK,
            (xpos - cross_size, tree_canvas_height - (ypos - cross_size)),
            (xpos + cross_size, tree_canvas_height - (ypos + cross_size)),
            linewidth)
        pygame.draw.line(
            tree_canvas,
            BLACK,
            (xpos - cross_size, tree_canvas_height - (ypos + cross_size)),
            (xpos + cross_size, tree_canvas_height - (ypos - cross_size)),
            linewidth)
    screen.blit(tree_canvas, tree_offset)

    font = pygame.font.SysFont('arial', fontsize)
    for sample in samples:
        text = font.render(str(sample), True, BLACK)
        textRect = text.get_rect()
        textRect.center = (
            (width - tree_width) // 2 + node_x_dict[sample],
            margin + tree_canvas_height + font_space
        )
        screen.blit(text, textRect)

    # Decide whether to show arrow or hand cursor
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if (mouse_x >= margin and mouse_x <= width - margin) and (mouse_y >= genome_offset[1] + margin / 2 and mouse_y <= height - margin / 2):
        pygame.mouse.set_cursor((24, 24), (5, 0), *click_cursor)
        ready_for_click = not pygame.mouse.get_pressed()[0]
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

    pygame.display.flip()
    clock.tick(100)

# Done! Time to quit.
pygame.quit()
