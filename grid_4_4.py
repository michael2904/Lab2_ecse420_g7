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
eta = 0.0002

print("This is the rank "+str(rank)+" with name "+str(name))

N = 4
if rank == 0:
	uM = [[0 for x in range(N)] for y in range(N)]
	u1M = [[0 for x in range(N)] for y in range(N)]
	u2M = [[0 for x in range(N)] for y in range(N)]
	u1M[2][2] = 1

for itera in range(T):
	print("This is iteration "+str(itera)+" in rank "+str(rank))
	if rank == 0:
		dataN = [[] for _ in range(size)]
		for i in range(1,N-1):
			for j in range(1,N-1):
				# print("This is rank "+str(rank)+" and u1M "+str(u1M)+" and u1M[i-1][j] ="+str(u1M[i-1][j]))
				dataN[(i+(N-2)*j) % size].append(u1M[i-1][j])
				dataN[(i+(N-2)*j) % size].append(u1M[i+1][j])
				dataN[(i+(N-2)*j) % size].append(u1M[i][j-1])
				dataN[(i+(N-2)*j) % size].append(u1M[i][j+1])
				dataN[(i+(N-2)*j) % size].append(u1M[i][j])
				dataN[(i+(N-2)*j) % size].append(u2M[i][j])
				# print("This is rank "+str(rank)+" and dataN "+str(dataN))
	else:
		dataN = None

	# print("This is rank "+str(rank)+" and dataN "+str(dataN))
	dataR = comm.scatter(dataN,root = 0)
	print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the data received "+str(dataR))
	result1 = None
	for i in range(1,N-1):
		for j in range(1,N-1):
			if rank == (i+(N-2)*j) % size:
				result1 = (p * (dataR[0] + dataR[1] + dataR[2] + dataR[3] - 4 * dataR[4]) + 2 * dataR[4] - (1-eta) * dataR[5]) / (1+eta)
				# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the result1 "+str(result1)+" at i,j "+str(i)+","+str(j))


	results = comm.gather(result1, root = 0)
	print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the results 1 "+str(results))
	if rank == 0:
		for i in range(1,N-1):
			for j in range(1,N-1):
				# print("This is uM[i][j] before"+str(uM[i][j]))
				uM[i][j] = results[(i+(N-2)*j) % size]
				# print("This is uM[i][j] before"+str(uM[i][j]))

		for i in range(0,N):
			for j in range(0,N):
				print('u('+str(i)+","+str(j)+") : "+str(uM[i][j])+" |"),
			print("")

	if rank == 0:
		dataN1 = [None for _ in range(size)]
		print("This is rank "+str(rank)+" and dataN1 "+str(dataN1))
		for i in range(1,N-1):
			dataN1[(i + 0*(N-2)) % size] = (uM[1][i])
			dataN1[(i + 1*(N-2)) % size] = (uM[N - 2][i])
			dataN1[(i + 2*(N-2)) % size] = (uM[1][i])
			dataN1[(i + 3*(N-2)) % size] = (uM[1][i])
			print("This is rank "+str(rank)+" and dataN1 "+str(dataN1))
	else:
		dataN1 = None

	print("This is rank "+str(rank)+" and dataN1 "+str(dataN1))
	dataR1 = comm.scatter(dataN1,root = 0)
	print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the data received 1 "+str(dataR1))


	# for i in range(1,N-1):
	# 	if rank < (2 * N):
	# 		if rank % 4 == 0:
	# 			u[0][i] = G * u[1][i]
	# 		elif rank % 4 == 1:
	# 			u[N - 1][i] = G * u[N - 2][i]
	# 		elif rank % 4 == 2:
	# 			u[i][0] = G * u[i][1]
	# 		elif rank % 4 == 3:
	# 			u[i][N - 1] = G * u[i][N - 2]



	# if rank < 4 :
	# 	if rank % 4 == 0:
	# 		u[0][0] = G * u[1][0]
	# 	elif rank % 4 == 1:
	# 		u[N - 1][0] = G * u[N - 2][0]
	# 	elif rank % 4 == 2:
	# 		u[0][N - 1] = G * u[0][N - 2]
	# 	elif rank % 4 == 3:
	# 		u[N - 1][N - 1] = G * u[N - 1][N - 2]

	if rank == 0:
		if itera >= 0:
			if itera >= 1:
				u2M = u1M
			u1M = uM
		for i in range(0,N):
			for j in range(0,N):
				print('u('+str(i)+","+str(j)+") : "+str(uM[i][j])+" |"),
			print("")



