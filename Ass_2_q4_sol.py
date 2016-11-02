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
	image = Image.open(input)
	image.load()
	width, height = image.size
	pixels = list(image.getdata())
	for i in range(len(pixels)):
		pixels[i] = list(pixels[i])
	chunks = [[] for _ in range(size)]
	for i, chunk in enumerate(pixels):
		chunks[i % size].append(chunk)
else:
	pixels = []
	chunks = None

# Scatter image pixels
result = comm.scatter(chunks, root=0)
# Rectify
result = [(
	127 if (pixel[0] < 127) else pixel[0],
	127 if (pixel[1] < 127) else pixel[1],
	127 if (pixel[2] < 127) else pixel[2],
	255
	) for pixel in result]


# Gather separate pixels to image array
result = comm.gather(result, root=0)
if rank == 0:
	for i in range(len(pixels)):
		pixels[i] = tuple(result[i % size][i / size])

	# Save PNG
	image2 = Image.new("RGBA", (width, height))
	image2.putdata(pixels)
	image2.save(output, 'PNG', optimize=False, compress_level=0)

