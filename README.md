keyboard-viz
============

This is our final project for CS 467. We're going to visualize keylogger output!

To Run
======
Open index.html in a browser.

To Use Your Own Data
====================
We used data from Free Keylogger Pro (for Windows). If you have a keylog in
the same (or similar) format, run "python2 parse logfile" to parse the file
and "python2 genkeyboard" to generate the keyboard image for the visualization

Dependencies
============
You'll need PIL (the Python Imaging Library) in order to use your own data

Work Division
=============
Jay worked on the frontend, Nick did front-end bugfixing and generated the
keyboard layout for the frontend, and Welsh wrote the parser (and supplied
the data)

## License
This is licensed under the [MIT](http://www.opensource.org/licenses/mit-license.php "").

Frontend based on: http://www.patrick-wied.at/projects/heatmap-keyboard/ (released under MIT license)
