/*
/ This .mod model file always writes in output.txt the value 42, on whichever instance .dat file it is called.
/ It is meant for two purposes:
/  1. as a template for the student. She can start her coding by editing from this template if she has not yet memorized the syntax for the reading in the data into her model.
/  2. as a testing/checking/debugging tool for the problem-maker when crafting the problem. A further piece of advice to the problem-maker il placed at the bottom of this file.
*/

param N integer, >= 1;  # number of rows and columns of the map
set Rows := 1..N;  # the set of row indexes
set Cols := 1..N;  # the set of column indexes
param MAP{Rows, Cols} binary; # 0 = free cell, 1 = cell containing a trap.

printf "42\n" > "output.txt";

end;

/*
/ Further advice to the problem-maker: try to write this file so that it complies both with GMPL and with AMPL. Use the free and readily installed glpsol to check whether it complies with GMPL. This can be done most convenienty from the command line as follows:
/    > glpsol -m map_always_answer_zero.mod -d ../examples/input_1.dat
/ To check compliance with AMPL use a local installation or the free online service:
/    https://ampl.com/cgi-bin/ampl/amplcgi
/
/ fill-in only the "Model and data" box (first the model ending with "end;" and print on console rather than on file).
/ Other links:
/     https://ampl.com/try-ampl/try-ampl-online/
/     https://ampl.com/try-ampl/start/
*/
