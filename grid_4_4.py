# Lab 2 ECSE 420 group 7
# Michael Abdallah-Minciotti
# Marco Manglaviti
# Assignment 2 Q4 test


from mpi4py import MPI
from PIL import Image
import sys

input = sys.argv[1]
output = sys.argv[2]

comm = MPI.COMM_WORLD
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

if rank == 0:
	u = [4][4]
	for i in range(0,4):
		for j in range(0,4):
			u[i][j] = 0
			print("output "+i+","+j+" val: "+u[i][j])
else:
	u = [][]

