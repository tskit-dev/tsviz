# PyGame-based visualisations

## Installing PyGame
You can use `python -m pip install pygame` or `python -m pip install --user pygame` if on a cluster to install PyGame.

TODO: add instructions for using PyGame through an SSH tunnel.

Here are some links that may help with troubleshooting.
- [Installation instructions for Windows 10 and Mac OS X](https://cs.hofstra.edu/docs/pages/guides/InstallingPygame.html)
- [Blank image on Mac OS X](https://github.com/pygame/pygame/issues/1250)
- [SDL libraries on Mac](http://pygame-users.25799.x6.nabble.com/SDL-for-Pygame-Mac-64-Almost-there-Please-help-td1827.html#a1836)
- [CGContextDrawImage: invalid context 0x0](https://stackoverflow.com/questions/40210152/pygame-in-macosx-cgcontextdrawimage-invalid-context-0x0)

## Description

`python art.py` displays a simple drawing of a blue circle and some black lines, useful for debugging a PyGame setup.

`python viz.py` is the main program to run. `python viz.py --help` will display options. A video of the behaviour as of November 25, 2019 is here:

![Demo video](https://github.com/brianzhang01/tskit-viz/raw/master/static/tskit-viz-demo.gif)

`sort.py` contains a simple function that sorts the tree's leaves in minimum lexicographic order when drawing the marginal trees. This usually leads neighbouring trees to be more consistent with each other. This behaviour can be toggled by passing `--sort 0` (no sorting) or `--sort 1` (with sorting, default if nothing is passed) into the `viz.py` script. As an extreme example where minimum lexicographic (minlex) sorting is not that helpful, run `python make_example.py` to produce an `example.trees` file, then run `python viz.py --file example.trees` to display the example.
