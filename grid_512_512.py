# Lab 2 ECSE 420 group 7
# Michael Abdallah-Minciotti
# Marco Manglaviti
# To build this code we wanted a process to have all the data together.
# So we built it such that the first process has all the data, it sets it up for the computations and
# scatters it to all the processes. After that each process runs the computation for its part of the data
# and then the first process gathers it. It gets all the data and updates all the grids.
# Lab 2 q2


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

N = 512




# Here, I am setting up the 3 grids on the first process
if rank == 0:
	# This is the print to copy the format in output.h
	print("float output[2000] = {")

	uM = [[0 for x in range(N)] for y in range(N)]
	u1M = [[0 for x in range(N)] for y in range(N)]
	u2M = [[0 for x in range(N)] for y in range(N)]
	u1M[N/2][N/2] = 1

# Here, I am looping for every iteration
for itera in range(T):

	# This is beginning of step 1
	if rank == 0:
		# dataN is the array where I am putting all the data need for each process do the computation
		dataN = [[] for _ in range(size)]
		# I am going through each point that I will need to compute and preparing the data for it
		for i in range(1,N-1):
			for j in range(1,N-1):
				# Here I am verifiyng that the number of divisions of data is positive such that I do not divide by 0.
				if ((N-2)*(N-2)/size) > 0:
					dataList = []
					dataList.append(u1M[i-1][j])
					dataList.append(u1M[i+1][j])
					dataList.append(u1M[i][j-1])
					dataList.append(u1M[i][j+1])
					dataList.append(u1M[i][j])
					dataList.append(u2M[i][j])
					# For every point I sequentially add the data needed to the corresponding spot in the array for computation
					dataN[((j-1)+(N-2)*(i-1))/(((N-2)*(N-2)/size)+ ((N-2)*(N-2) % size > 0))].append(dataList)
				else:
					dataList = []
					dataList.append(u1M[i-1][j])
					dataList.append(u1M[i+1][j])
					dataList.append(u1M[i][j-1])
					dataList.append(u1M[i][j+1])
					dataList.append(u1M[i][j])
					dataList.append(u2M[i][j])
					dataN[((j-1)+(N-2)*(i-1))].append(dataList)
	else:
		dataN = None

	# When I am done preparing the data, I scatter it through every process
	dataR = comm.scatter(dataN,root = 0)

	# Every process does the computation on its data
	result = None
	resultList = []
	for i in range(0,len(dataR)):
		result = ((p * (dataR[i][0] + dataR[i][1] + dataR[i][2] + dataR[i][3] - 4 * dataR[i][4])) + (2 * dataR[i][4]) - ((1-eta) * dataR[i][5])) / (1+eta)
		resultList.append(result)

	# Here I am gathering back the computed data and saving it to the grid
	results = comm.gather(resultList, root = 0)
	if rank == 0:
		count2 = 0
		for i in range(1,N-1):
			for j in range(1,N-1):
				if ((N-2)*(N-2)/size) > 0 :
					count2Mod = count2%(((N-2)*(N-2)/size) + ((N-2)*(N-2) % size > 0))
					count2Val = count2/(((N-2)*(N-2)/size) + ((N-2)*(N-2) % size > 0))
					uM[i][j] = results[count2Val][count2Mod]
				else:
					uM[i][j] = results[count2][0]
				count2 += 1
	# This is the end of step 1

	# This is the beginning of step 2
	# I use the same process as the first step to prepare the data for computation, scatter it, compute, gather and save.

	if rank == 0:
		dataN1 = [[] for _ in range(size)]
		for i in range(1,N-1):
			if (4*(N-2)/size) > 0 :
				dataN1[((i-1)*4 + 0) / ((4*(N-2)/size)+ (4*(N-2) % size > 0))].append(uM[1][i])
				dataN1[((i-1)*4 + 1) / ((4*(N-2)/size)+ (4*(N-2) % size > 0))].append(uM[N - 2][i])
				dataN1[((i-1)*4 + 2) / ((4*(N-2)/size)+ (4*(N-2) % size > 0))].append(uM[i][1])
				dataN1[((i-1)*4 + 3) / ((4*(N-2)/size)+ (4*(N-2) % size > 0))].append(uM[i][N-2])
			else:
				dataN1[((i-1)*4 + 0)].append(uM[1][i])
				dataN1[((i-1)*4 + 1)].append(uM[N - 2][i])
				dataN1[((i-1)*4 + 2)].append(uM[i][1])
				dataN1[((i-1)*4 + 3)].append(uM[i][N-2])
	else:
		dataN1 = None

	dataR1 = comm.scatter(dataN1,root = 0)

	result1 = None
	result1List = []
	for i in range(0,len(dataR1)):
		result1 = G * dataR1[i]
		result1List.append(result1)

	results1 = comm.gather(result1List, root = 0)

	if rank == 0:
		count3 = 0
		for i in range(1,N-1):
			if (4*(N-2)/size) > 0 :
				count3Mod = count3%((4*(N-2)/size) + (4*(N-2) % size > 0))
				count3Val = count3/((4*(N-2)/size) + (4*(N-2) % size > 0))
				uM[0][i] = results1[count3Val][count3Mod]
				count3 += 1
				count3Mod = count3%((4*(N-2)/size) + (4*(N-2) % size > 0))
				count3Val = count3/((4*(N-2)/size) + (4*(N-2) % size > 0))
				uM[N - 1][i] = results1[count3Val][count3Mod]
				count3 += 1
				count3Mod = count3%((4*(N-2)/size) + (4*(N-2) % size > 0))
				count3Val = count3/((4*(N-2)/size) + (4*(N-2) % size > 0))
				uM[i][0] = results1[count3Val][count3Mod]
				count3 += 1
				count3Mod = count3%((4*(N-2)/size) + (4*(N-2) % size > 0))
				count3Val = count3/((4*(N-2)/size) + (4*(N-2) % size > 0))
				uM[i][N - 1] = results1[count3Val][count3Mod]
				count3 += 1
			else:
				uM[0][i] = results1[count3][0]
				count3 += 1
				uM[N - 1][i] = results1[count3][0]
				count3 += 1
				uM[i][0] = results1[count3][0]
				count3 += 1
				uM[i][N - 1] = results1[count3][0]
				count3 += 1

	# This is the end of step 2


	# This is the beginning of step 3
	# I use the same process as the first step to prepare the data for computation, scatter it, compute, gather and save.

	if rank == 0:
		dataN2 = [[] for _ in range(size)]
		if (4*(N-2)/size) > 0 :
			dataN2[0 / ((4*(N-2)/size) + (4*(N-2) % size > 0))].append(uM[1][0])
			dataN2[1 / ((4*(N-2)/size) + (4*(N-2) % size > 0))].append(uM[N - 2][0])
			dataN2[2 / ((4*(N-2)/size) + (4*(N-2) % size > 0))].append(uM[0][N - 2])
			dataN2[3 / ((4*(N-2)/size) + (4*(N-2) % size > 0))].append(uM[N - 1][N - 2])
			# print("This is rank "+str(rank)+" and dataN2 "+str(dataN2))
		else:
			dataN2[0].append(uM[1][0])
			dataN2[1].append(uM[N - 2][0])
			dataN2[2].append(uM[0][N - 2])
			dataN2[3].append(uM[N - 1][N - 2])
	else:
		dataN2 = None

	
	dataR2 = comm.scatter(dataN2,root = 0)

	result2 = None
	result2List = []
	for i in range(0,len(dataR2)):
		result2 = G * dataR2[i]
		result2List.append(result2)

	results2 = comm.gather(result2List, root = 0)

	if rank == 0:
		for i in range(0,4):
			if (4*(N-2)/size) > 0 :
				count5Mod = i%((4*(N-2)/size) + (4*(N-2) % size > 0))
				count5Val = i/((4*(N-2)/size) + (4*(N-2) % size > 0))
				if i == 0:
					uM[0][0] = results2[count5Val][count5Mod]
				elif i == 1:
					uM[N-1][0] = results2[count5Val][count5Mod]
				elif i == 2:
					uM[0][N-1] = results2[count5Val][count5Mod]
				elif i == 3:
					uM[N-1][N-1] = results2[count5Val][count5Mod]
			else:
				if i == 0:
					uM[0][0] = results2[i][0]
				elif i == 1:
					uM[N-1][0] = results2[i][0]
				elif i == 2:
					uM[0][N-1] = results2[i][0]
				elif i == 3:
					uM[N-1][N-1] = results2[i][0]

	# This is the end of step 3

	if rank == 0:
		u2M = deepcopy(u1M)
		u1M = deepcopy(uM)
		if itera < T-1:
			print("%.6f," % uM[N/2][N/2])
		else:
			print("%.6f\n};" % uM[N/2][N/2])





