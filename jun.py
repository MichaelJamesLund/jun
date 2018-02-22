from __future__ import division
import math, random

class jun:
	
	def __init__(self,size):
		self.list          = range(size)
		self.list_backup   = []  
		self.stats         = []
		self.sort_spectrum = []
		# Binary log of math.factorial(size).  Uses Stirling's approximation.
		self.min_entropy = math.ceil(size * math.log( size / math.e, 2) + .5 * math.log(2 * math.pi * size, 2))

	def backup(self):
		self.list_backup = self.list[:]

	def restore(self):
		self.list = self.list_backup[:]

	"""
	def mix(self):
		size = len(self.list)
		step = 1
		while step < size:
			for i in xrange(step):
				for j in xrange(i, size - step, step):
					if random.random() < .5:
						self.list[j], self.list[j + step] = self.list[j + step], self.list[j]
			step *= 2
	"""
	def mix(self):
		random.shuffle(self.list)

	# Estimates Shannon entry
	def estimate_entropy_in_shell(self,interval):
		interval = int(interval)
		size = len(self.list)
		flips, stays = 0, 0
		for i in xrange(size - interval):
			print "{0} {1}".format(i, i + interval)
			if self.list[i] > self.list[i + interval]:
				flips += 1
			else:
				stays += 1
		self.calculate_entropy(flips,stays)

	def calculate_entropy(self,flips,stays):
		total = flips + stays
		if total != 0:
			flip_fraction = flips / total
			stay_fraction = stays / total
			flip_entropy, stay_entropy, entropy = 0, 0, 0
			if flip_fraction != 0 and flip_fraction != 1:
				flip_entropy = -(flips * flip_fraction * math.log(flip_fraction,2))
			if stay_fraction != 0 and stay_fraction != 1:
				stay_entropy = -(stays * stay_fraction * math.log(stay_fraction,2))
			entropy = flip_entropy + stay_entropy
			print "flips: {0}; stays: {1}; total: {2}; flip_fraction: {3}; stay_fraction: {4}; flip_entropy: {5}; stay_entropy: {6}".\
			 format(flips,stays,total,flip_fraction,stay_fraction,flip_entropy,stay_entropy)
			return entropy
		else:
			print "Entropy calculation is impossible!  All values zero!"
			return None


	def estimate_entropy(self):
		size = len(self.list)
		entropy_vector = [0]
		interval = 1
		while interval < size:
			shell_entropy = self.estimate_entropy_in_shell(interval)
			entropy_vector[0] += shell_entropy
			entropy_vector.append(shell_entropy)
			interval <<= 1
		return entropy_vector


	def count_info(self,list,interval):
		size = len(list)
		totals  = { 'flips' : 0, 'stays' : 0 }
		# In this subroutine, the values of all lists are indexes of the list
		# we are trying to sort.
		previously_determined = []
		for elem in list:
			previously_determined.append( { 'ascents' : [], 'descents' : [] }  )
		for i in range(0, size - interval):
			descents, ascents = [], []
			for j in xrange(i + interval, size):
				if list[i] < list[j]:
					unique = True
					for k in ascents:
						if list[j] > list[k]:
							unique = False
							break
					if unique == True:
						ascents.append(j)
				elif list[i] > list[j]:
					unique = True
					for k in descents:
						if list[j] < list[k]:
							unique = False
							break
					if unique == True:
						descents.append(j)
			for j in range(0, len(ascents) - 2 ):
				k = j + 1
				if not ascents[k] in previously_determined[ascents[j]]['descents']:
					previously_determined[ascents[j]]['descents'].append(ascents[k])
			for j in range(0, len(descents) - 2 ):
				k = j + 1
				if not descents[k] in previously_determined[descents[j]]['ascents']:
					previously_determined[descents[j]]['ascents'].append(descents[k])
			previously_determined_descents = self.all_previously_determined(previously_determined,'descents',i,[])
			previously_determined_ascents = self.all_previously_determined(previously_determined,'ascents',i,[])
			for j in descents:
				if not j in previously_determined_descents:
					totals['flips'] += 1
			for j in ascents:
				if not j in previously_determined_ascents:
					totals['stays'] += 1
			totals_from_previously_determined_ascents = self.count_info_by_proxy(previously_determined_ascents,previously_determined)
			totals_from_previously_determined_descents = self.count_info_by_proxy(previously_determined_descents,previously_determined)
			totals['flips'] += totals_from_previously_determined_ascents['flips']
			totals['flips'] += totals_from_previously_determined_descents['flips']
			totals['stays'] += totals_from_previously_determined_ascents['stays']
			totals['stays'] += totals_from_previously_determined_descents['stays']
		return totals
				

	def count_unique_info(self,list,interval):
		size = len(list)
		totals  = { 'flips' : 0, 'stays' : 0 }
		for i in range(0, size - interval):
			descents, ascents = [], []
			for j in xrange(i + interval, size):
				if list[i] < list[j]:
					if len(ascents) == 0 or list[j] < list[ascents[-1]]:
						ascents.append(j)
				elif list[i] > list[j]:
					if len(descents) == 0 or list[j] > list[descents[-1]]:
						descents.append(j)
			totals['stays'] += len(ascents)
			totals['flips'] += len(descents)
		return totals
				

	def count_info_by_proxy(self,list,previously_determined):
		size = len(list)
		totals  = { 'flips' : 0, 'stays' : 0 }
		# In this subroutine, the values of all lists are indexes of the list
		# we are trying to sort.
		for i in range(0, size):
			descents, ascents = [], []
			for j in xrange(i + 1, size):
				if self.list[list[i]] < self.list[list[j]]:
					unique = True
					for k in ascents:
						if self.list[list[j]] > self.list[k]:
							unique = False
							break
					if unique == True:
						ascents.append(list[j])
				elif self.list[list[i]] > self.list[list[j]]:
					unique = True
					for k in descents:
						if self.list[list[j]] < self.list[k]:
							unique = False
							break
					if unique == True:
						descents.append(list[j])
			for j in range(0, len(ascents) - 2 ):
				k = j + 1
				try:
					if not ascents[k] in previously_determined[ascents[j]]['descents']:
						previously_determined[ascents[j]]['descents'].append(ascents[k])
				except IndexError:
					print ascents
					print previously_determined[j]
			for j in range(0, len(descents) - 2 ):
				k = j + 1
				if not descents[k] in previously_determined[descents[j]]['ascents']:
					previously_determined[descents[j]]['ascents'].append(descents[k])
			previously_determined_descents = self.all_previously_determined(previously_determined,'descents',i,[])
			previously_determined_ascents = self.all_previously_determined(previously_determined,'ascents',i,[])
			for j in descents:
				if not j in previously_determined_descents:
					totals['flips'] += 1
			for j in ascents:
				if not j in previously_determined_ascents:
					totals['stays'] += 1
			totals_from_previously_determined_ascents = self.count_info_by_proxy(previously_determined_ascents,previously_determined)
			totals_from_previously_determined_descents = self.count_info_by_proxy(previously_determined_descents,previously_determined)
			totals['flips'] += totals_from_previously_determined_ascents['flips']
			totals['flips'] += totals_from_previously_determined_descents['flips']
			totals['stays'] += totals_from_previously_determined_ascents['stays']
			totals['stays'] += totals_from_previously_determined_descents['stays']
		return totals
				

	def all_previously_determined(self,previously_determined,kind,idx,return_array):
		local_previously_determined = previously_determined[idx][kind]
		return_array += local_previously_determined
		for i in local_previously_determined:
			self.all_previously_determined(previously_determined,kind,i,return_array)
		return return_array

	def measure_entropy(self,interval):
		unique_info = self.count_unique_info(self.list,interval)
		return unique_info['stays'] + unique_info['flips']

	def gauge_energy(self,start,end):
		pass
