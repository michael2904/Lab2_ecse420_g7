# Lab 2 ECSE 420 group 7
# Michael Abdallah-Minciotti
# Marco Manglaviti
# Assignment 2 Q4 test


from mpi4py import MPI
from PIL import Image
import sys

T = int(sys.argv[1])

comm = MPI.COMM_WORLD
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

print("This is the rank "+str(rank)+" with name "+str(name))

for iterations in range(T):
	print("This is iteration "+str(iterations)+" in rank "+str(rank))
	if rank == 0:
		u = [[0 for x in range(4)] for y in range(4)]
		for i in range(0,4):
			for j in range(0,4):
				chunks = [[] for _ in range(size)]
				print("output "+str(i)+","+str(j)+" val: "+str(u[i][j]))

		for i, chunk in enumerate(u):
			chunks[i % size].append(chunk)
	else:
		u = [[0 for x in range(4)] for y in range(4)]

