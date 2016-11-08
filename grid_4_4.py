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

N = 8
if rank == 0:
	uM = [[0 for x in range(N)] for y in range(N)]
	u1M = [[0 for x in range(N)] for y in range(N)]
	u2M = [[0 for x in range(N)] for y in range(N)]
	u1M[N/2][N/2] = 1

for itera in range(T):
	print("This is iteration "+str(itera)+" in rank "+str(rank))


	# This is beginning of step 1
	if rank == 0:
		dataN = [[] for _ in range(size)]
		print(dataN)
		for i in range(1,N-1):
			for j in range(1,N-1):
				if ((N-2)*(N-2)/size) > 0:
					# print("This is rank "+str(rank)+" and u1M "+str(u1M)+" and u1M[i-1][j] ="+str(u1M[i-1][j]))
					dataList = []
					dataList.append(u1M[i-1][j])
					dataList.append(u1M[i+1][j])
					dataList.append(u1M[i][j-1])
					dataList.append(u1M[i][j+1])
					dataList.append(u1M[i][j])
					dataList.append(u2M[i][j])
					print(" ************* This is rank "+str(rank)+" and id is "+str((j-1)+(N-2)*(i-1)) +" / "+str(((N-2)*(N-2)/size)+ ((N-2)*(N-2) % size > 0))+" with result: "+str(((j-1)+(N-2)*(i-1))/(((N-2)*(N-2)/size)+ ((N-2)*(N-2) % size > 0))))
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
					# print(" ************* This is rank "+str(rank)+" and dataN "+str(dataN))
	else:
		dataN = None

	# if rank == 0:
	# 	print("This is rank "+str(rank)+" and dataN "+str(dataN))
	dataR = comm.scatter(dataN,root = 0)
	# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the data received "+str(dataR))
	result = None
	count = 0
	resultList = []
	for i in range(0,len(dataR)):
		result = ((p * (dataR[i][0] + dataR[i][1] + dataR[i][2] + dataR[i][3] - 4 * dataR[i][4])) + (2 * dataR[i][4]) - ((1-eta) * dataR[i][5])) / (1+eta)
		resultList.append(result)
		# print("----------This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the results 1 "+str(resultList)+" with dataR "+str(dataR[count]))


	results = comm.gather(resultList, root = 0)
	# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the results 1 "+str(results))
	if rank == 0:
		print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the results 1 "+str(results))
		count2 = 0
		for i in range(1,N-1):
			for j in range(1,N-1):
				if ((N-2)*(N-2)/size) > 0 :
					count2Mod = count2%((N-2)*(N-2)/size)+ ((N-2)*(N-2) % size > 0)
					count2Val = count2/((N-2)*(N-2)/size)+ ((N-2)*(N-2) % size > 0)
					print("these are the indexes: "+str(count2Val)+" and "+str(count2Mod))
					uM[i][j] = results[count2Val][count2Mod]
				else:
					uM[i][j] = results[count2][0]
				count2 += 1


	# This is the end of step 1

	# if rank == 0:
	# 	print("u")
	# 	for i in range(0,N):
	# 		for j in range(0,N):
	# 			print('u('+str(i)+","+str(j)+") : "+str(uM[i][j])+" |"),
	# 		print("")
	# 	print("u1")
	# 	for i in range(0,N):
	# 		for j in range(0,N):
	# 			print('u1('+str(i)+","+str(j)+") : "+str(u1M[i][j])+" |"),
	# 		print("")
	# 	print("u2")
	# 	for i in range(0,N):
	# 		for j in range(0,N):
	# 			print('u2('+str(i)+","+str(j)+") : "+str(u2M[i][j])+" |"),
	# 		print("")

	# This is the beginning of step 2

	if rank == 0:
		dataN1 = [[] for _ in range(size)]
		# print("This is rank "+str(rank)+" and dataN1 "+str(dataN1))
		for i in range(1,N-1):
			if (4*(N-2)/size) > 0 :
				dataN1[((i-1)*4 + 0) / (4*(N-2)/size)].append(uM[1][i])
				dataN1[((i-1)*4 + 1) / (4*(N-2)/size)].append(uM[N - 2][i])
				dataN1[((i-1)*4 + 2) / (4*(N-2)/size)].append(uM[i][1])
				dataN1[((i-1)*4 + 3) / (4*(N-2)/size)].append(uM[i][N-2])
				# print(">0*********This is rank "+str(rank)+" and dataN1 "+str(dataN1))
			else:
				dataN1[((i-1)*4 + 0)].append(uM[1][i])
				dataN1[((i-1)*4 + 1)].append(uM[N - 2][i])
				dataN1[((i-1)*4 + 2)].append(uM[i][1])
				dataN1[((i-1)*4 + 3)].append(uM[i][N-2])
	else:
		dataN1 = None

	# if rank == 0:
		# print("This is rank "+str(rank)+" and dataN1 "+str(dataN1))

	dataR1 = comm.scatter(dataN1,root = 0)
	# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the data received 1 "+str(dataR1))

	result1 = None
	result1List = []
	for i in range(0,len(dataR1)):
		result1 = G * dataR1[i]
		result1List.append(result1)
		# print("---------This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the result1List "+str(result1List)+" with this dataR1: "+str(dataR1))

	results1 = comm.gather(result1List, root = 0)
	# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the results1 "+str(results1))
	if rank == 0:
		# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the results1 "+str(results1))
		count3 = 0
		for i in range(1,N-1):
			if (4*(N-2)/size) > 0 :
				count3Mod = count3%((4*(N-2)/size))
				count3Val = count3/((4*(N-2)/size))
				uM[0][i] = results1[count3Val][count3Mod]
				count3 += 1
				count3Mod = count3%((4*(N-2)/size))
				count3Val = count3/((4*(N-2)/size))
				uM[N - 1][i] = results1[count3Val][count3Mod]
				count3 += 1
				count3Mod = count3%((4*(N-2)/size))
				count3Val = count3/((4*(N-2)/size))
				uM[i][0] = results1[count3Val][count3Mod]
				count3 += 1
				count3Mod = count3%((4*(N-2)/size))
				count3Val = count3/((4*(N-2)/size))
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

	# if rank == 0:
	# 	print("u")
	# 	for i in range(0,N):
	# 		for j in range(0,N):
	# 			print('u('+str(i)+","+str(j)+") : "+str(uM[i][j])+" |"),
	# 		print("")
	# 	print("u1")
	# 	for i in range(0,N):
	# 		for j in range(0,N):
	# 			print('u1('+str(i)+","+str(j)+") : "+str(u1M[i][j])+" |"),
	# 		print("")
	# 	print("u2")
	# 	for i in range(0,N):
	# 		for j in range(0,N):
	# 			print('u2('+str(i)+","+str(j)+") : "+str(u2M[i][j])+" |"),
	# 		print("")


	# This is the beginning of step 3

	if rank == 0:
		dataN2 = [[] for _ in range(size)]
		if (4*(N-2)/size) > 0 :
			dataN2[0 / (4*(N-2)/size)].append(uM[1][0])
			dataN2[1 / (4*(N-2)/size)].append(uM[N - 2][0])
			dataN2[2 / (4*(N-2)/size)].append(uM[0][N - 2])
			dataN2[3 / (4*(N-2)/size)].append(uM[N - 1][N - 2])
			# print("This is rank "+str(rank)+" and dataN2 "+str(dataN2))
		else:
			dataN2[0].append(uM[1][0])
			dataN2[1].append(uM[N - 2][0])
			dataN2[2].append(uM[0][N - 2])
			dataN2[3].append(uM[N - 1][N - 2])
	else:
		dataN2 = None

	
	dataR2 = comm.scatter(dataN2,root = 0)
	# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the data received 2 "+str(dataR2))

	result2 = None
	result2List = []
	for i in range(0,len(dataR2)):
		result2 = G * dataR2[i]
		result2List.append(result2)

	# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the result2List "+str(result2List))
	results2 = comm.gather(result2List, root = 0)
	# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the results1 "+str(results2))

	if rank == 0:
		# print("This is iteration "+str(itera)+" in rank "+str(rank)+" and here is the results2 "+str(results2))
		for i in range(0,4):
			if (4*(N-2)/size) > 0 :
				count5Mod = i%((4*(N-2)/size))
				count5Val = i/((4*(N-2)/size))
				# print("This is count5Val: "+str(count5Val)+" and this is count5Mod: "+str(count5Mod))
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
		print("u")
		for i in range(0,N):
			for j in range(0,N):
				print('u('+str(i)+","+str(j)+") : "+str(uM[i][j])+" |"),
			print("")
		# print("u1")
		# for i in range(0,N):
		# 	for j in range(0,N):
		# 		print('u1('+str(i)+","+str(j)+") : "+str(u1M[i][j])+" |"),
		# 	print("")
		# print("u2")
		# for i in range(0,N):
		# 	for j in range(0,N):
		# 		print('u2('+str(i)+","+str(j)+") : "+str(u2M[i][j])+" |"),
		# 	print("")




