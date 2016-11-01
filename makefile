CC = gcc
CFLAGS  = -I. -lm

# typing 'make' will invoke the first target entry in the file 
# (in this case the default target entry)
# you can name this target entry anything, but "default" or "all"
# are the most commonly used names by convention
#
default: all

all: test_equality rectify pool convolve

# To create the executable file count we need the object files
#
test_equality:  test_equality.o lodepng.o
	$(CC) -o test_equality test_equality.o lodepng.o $(CFLAGS)

rectify:  test_rectification.o lodepng.o
	$(CC) -fopenmp -o rectify test_rectification.o lodepng.o $(CFLAGS)

test_rectification.o: test_rectification.c
	$(CC) -fopenmp -c test_rectification.c -I.

rectify_MPI:  test_rectification_MPI.o lodepng.o
	$(CC) -fopenmp -o rectify test_rectification_MPI.o lodepng.o $(CFLAGS)

test_rectification_MPI.o: test_rectification_MPI.c
	$(CC) -fopenmp -c test_rectification_MPI.c -I.

lodepng.o: lodepng.c
	$(CC)  -c lodepng.c

pool:  test_pooling.o lodepng.o
	$(CC) -fopenmp -o pool test_pooling.o lodepng.o $(CFLAGS)

test_pooling.o: test_pooling.c
	$(CC) -fopenmp -c test_pooling.c -I.

convolve:  test_convolution.o lodepng.o
	$(CC) -fopenmp -o convolve test_convolution.o lodepng.o $(CFLAGS)

test_convolution.o: test_convolution.c wm.h
	$(CC) -fopenmp -c test_convolution.c -I.

# To start over from scratch, type 'make clean'.  This
# removes the executable file, as well as old .o object
# files and *~ backup files:
#
clean: 
	$(RM) count *.o *~
