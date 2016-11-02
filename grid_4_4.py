# Lab 2 ECSE 420 group 7
# Michael Abdallah-Minciotti
# Marco Manglaviti
# Assignment 2 Q4 test


from mpi4py import MPI
from PIL import Image
from math import exp
import sys

T = int(sys.argv[1])

comm = MPI.COMM_WORLD
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

p = 0.5
G = 0.75
eta = 2* exp(1e-4)
print("This is eta "+str(eta))

print("This is the rank "+str(rank)+" with name "+str(name))

N = 4

	u = [[0 for x in range(N)] for y in range(N)]
	u1 = [[0 for x in range(N)] for y in range(N)]
	u2 = [[0 for x in range(N)] for y in range(N)]

for itera in range(T):
	# print("This is iteration "+str(itera)+" in rank "+str(rank))
	for i in range(0,4):
		for j in range(0,4):
			if rank == (i+4*j):
				if (i>0 and i<N-1 and j>0 and j<N-1):
					u[i][j]= (p(u1[i-1][j] + u1[i+1][j] + u1[i][j-1] + u1[i][j+1] - 4 * u1[i][j]) + 2 * u1[i][j] - (1-eta) * u2[i][j]) / (1+eta)

	for i in range(1,N-1):
		if rank < (2 * N)
			if rank % 4 == 0:
				u[0][i] = G * u[1][i]
			elif rank % 4 == 1:
				u[N - 1][i] = G * u[N - 2][i]
			elif rank % 4 == 2:
				u[i][0] = G * u[i][1]
			elif rank % 4 == 3:
				u[i][N - 1] = G * u[i][N - 2]

	if rank < 4 :
		if rank % 4 == 0:
			u[0][0] = G * u[1][0]
		elif rank % 4 == 1:
			u[N - 1][0] = G * u[N - 2][0]
		elif rank % 4 == 2:
			u[0][N - 1] = G * u[0][N - 2]
		elif rank % 4 == 3:
			u[N - 1][N - 1] = G * u[N - 1][N - 2]

	if itera >= 0:
		if itera >= 1:
			u2 = u1
		u1 = u0
