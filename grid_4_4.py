# Lab 2 ECSE 420 group 7
# Michael Abdallah-Minciotti
# Marco Manglaviti
# Lab 2 q1


from mpi4py import MPI
from PIL import Image
from math import exp
from copy import copy,deepcopy
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
	u1M[N/2][N/2] = 1

for itera in range(T):
	print("This is iteration "+str(itera)+" in rank "+str(rank))
	if rank == 0:
		dataN = [[] for _ in range(size)]
		for i in range(1,N-1):
			for j in range(1,N-1):
				# print("This is rank "+str(rank)+" and u1M "+str(u1M)+" and u1M[i-1][j] ="+str(u1M[i-1][j]))
				dataList = []
				dataList.append(u1M[i-1][j])
				dataList.append(u1M[i+1][j])
				dataList.append(u1M[i][j-1])
				dataList.append(u1M[i][j+1])
				dataList.append(u1M[i][j])
				dataList.append(u2M[i][j])
				dataN[(i+(N-2)*j) % size].append(dataList)
				# print("This is rank "+str(rank)+" and dataN "+str(dataN))
	else:
		dataN = None

	# print("This is rank "+str(rank)+" and dataN "+str(dataN))
	dataR = comm.scatter(dataN,root = 0)
	# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the data received "+str(dataR))
	result = None
	count = 0
	resultList = []
	for i in range(1,N-1):
		for j in range(1,N-1):
			if rank == (i+(N-2)*j) % size:
				result = ((p * (dataR[count][0] + dataR[count][1] + dataR[count][2] + dataR[count][3] - 4 * dataR[count][4])) + (2 * dataR[count][4]) - ((1-eta) * dataR[count][5])) / (1+eta)
				resultList.append(result)
				count++
				# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the result "+str(result)+" at i,j "+str(i)+","+str(j))


	results = comm.gather(resultList, root = 0)
	# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the results 1 "+str(results))
	if rank == 0:
		count2 = 0
		for i in range(1,N-1):
			for j in range(1,N-1):
				uM[i][j] = results[(i+(N-2)*j) % size][count2]
				count2++

	if rank == 0:
		dataN1 = [None for _ in range(size)]
		# print("This is rank "+str(rank)+" and dataN1 "+str(dataN1))
		for i in range(1,N-1):
			dataN1[(i + 0*(N-2)) % size] = (uM[1][i])
			dataN1[(i + 1*(N-2)) % size] = (uM[N - 2][i])
			dataN1[(i + 2*(N-2)) % size] = (uM[i][1])
			dataN1[(i + 3*(N-2)) % size] = (uM[i][N-2])
			# print("This is rank "+str(rank)+" and dataN1 "+str(dataN1))
	else:
		dataN1 = None

	# print("This is rank "+str(rank)+" and dataN1 "+str(dataN1))
	dataR1 = comm.scatter(dataN1,root = 0)
	# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the data received 1 "+str(dataR1))

	result1 = None
	for i in range(1,N-1):
		for j in range(0,N):
			if rank == (i + j*(N-2)) % size:
				result1 = G * dataR1
				# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the result1 "+str(result1)+" at i,j "+str(i)+","+str(j))

	results1 = comm.gather(result1, root = 0)
	# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the results1 "+str(results1))
	if rank == 0:
		for i in range(1,N-1):
			uM[0][i] = results1[(i + 0*(N-2)) % size]
			uM[N - 1][i] = results1[(i + 1*(N-2)) % size]
			uM[i][0] = results1[(i + 2*(N-2)) % size]
			uM[i][N - 1] = results1[(i + 3*(N-2)) % size]

	if rank == 0:
		dataN2 = [None for _ in range(size)]
		dataN2[0] = uM[1][0]
		dataN2[1] = uM[N - 2][0]
		dataN2[2] = uM[0][N - 2]
		dataN2[3] = uM[N - 1][N - 2]
	else:
		dataN2 = None

	# print("This is rank "+str(rank)+" and dataN2 "+str(dataN2))
	dataR2 = comm.scatter(dataN2,root = 0)
	# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the data received 2 "+str(dataR2))

	result2 = None
	if rank == 0:
		result2 = G * dataR2
	elif rank == 1:
		result2 = G * dataR2
	elif rank == 2:
		result2 = G * dataR2
	elif rank == 3:
		result2 = G * dataR2

	results2 = comm.gather(result2, root = 0)
	# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the results1 "+str(results2))

	if rank == 0:
		uM[0][0] = results2[0]
		uM[N-1][0] = results2[1]
		uM[0][N-1] = results2[2]
		uM[N-1][N-1] = results2[3]

	if rank == 0:
		u2M = deepcopy(u1M)
		u1M = deepcopy(uM)
		print("u")
		for i in range(0,N):
			for j in range(0,N):
				print('u('+str(i)+","+str(j)+") : "+str(uM[i][j])+" |"),
			print("")
		print("u1")
		for i in range(0,N):
			for j in range(0,N):
				print('u1('+str(i)+","+str(j)+") : "+str(u1M[i][j])+" |"),
			print("")
		print("u2")
		for i in range(0,N):
			for j in range(0,N):
				print('u2('+str(i)+","+str(j)+") : "+str(u2M[i][j])+" |"),
			print("")




