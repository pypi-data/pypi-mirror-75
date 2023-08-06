import matplotlib.pyplot as plt
import math

class FormatPlot:
	""" FormatPlot class to create well-formatted, well labeled visualizations
		based on matplotlib

	Attributes:
		None

	"""
	def __init__(self):
		x = []
		y = []

	def read_data_file(file_name1, file_name2):

		"""Function to read in data from a txt file. The txt file should have
		one number (float) per line. The numbers are stored in the data attribute.

		Args:
			file_name1 (string): name of a file1 to read from
			file_name2 (string): name of a file2 to read from

		Returns:
			x, data read from file_name1
			y, data read from file_name2

		"""

		with open(file_name1, file_name2) as file1, file2:
			data_list1 = []
			line1 = file1.readline()
			while line1:
				data_list1.append(int(line1))
				line1 = file1.readline()

			data_list2 = []
			line2 = file2.readline()
			while line2:
				data_list2.append(int(line2))
				line2 = file2.readline()
		file1.close()
		file2.close()

		x = data_list1
		y = data_list2

		return x, y

	# def reformat():
	#
	# 	"""Function to reformat the plotted figures.
	#
	# 	Args:
	# 		None
	#
	# 	Returns:
	# 		None
	#
	# 	"""
	# 	plt.xticks(fontsize=10)
	# 	plt.yticks(fontsize=10)
	# 	plt.box(True)
	# 	plt.grid(True)
	# 	plt.show()


	def plot(x , y):

		"""Function to calculate the standard deviation of the data set.

		Args:
			x, numpy 1d array
			y, function of x

		Returns:
			None

		"""

		plt.figure(figsize = (7,4))
		plt.plot(x, y, color='blue',linestyle='dashed')
		plt.title('xy relationship',fontsize=14)
		plt.ylabel('y', fontsize=12)
		plt.xlabel('x', fontsize=12)
		plt.xticks(fontsize=10)
		plt.yticks(fontsize=10)
		plt.box(True)
		plt.grid(True)
		plt.show()
		# reformat()



	def hist(x):
		"""Function to output a reformatted histogram of the instance variable data using
		matplotlib pyplot library.

		Args:
			x, numpy 1d array

		Returns:
			None
		"""
		plt.figure(figsize = (7,4))
		plt.hist(x, bins = round(len(x)/10), color = 'blue')
		plt.title('Histogram of Data', fontsize=14)
		plt.xlabel('data', fontsize=12)
		plt.ylabel('count', fontsize=12)
		plt.xticks(fontsize=10)
		plt.yticks(fontsize=10)
		plt.box(True)
		plt.grid(True)
		plt.show()
		# reformat()


	# def bar(x,y):
	# 	"""Function to output a reformatted bar plot of the instance variable data using
	# 	matplotlib pyplot library.
	#
	# 	Args:
	# 		None
	#
	# 	Returns:
	# 		None
	# 	"""
	# 	frequency = len(x)
	# 	plt.bar(x,y)
	# 	plt.title('Histogram of Data', fontsize=14)
	# 	plt.xlabel('data', fontsize=12)
	# 	plt.ylabel('count', fontsize=12)
	# 	plt.xticks(fontsize=10)
	# 	plt.yticks(fontsize=10)
	# 	plt.box(True)
	# 	plt.grid(True)
	# 	plt.show()
	# 	# reformat()
