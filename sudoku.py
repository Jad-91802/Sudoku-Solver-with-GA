import sys
import time
import random
import matplotlib.pyplot as plot
import os


POPULATION_SIZE = 100 		# an even value such that its quotient is also divisible by 2.
TOURNAMENT_MATCH_SIZE = 10 	# must not be less than 1, no need to be more than POPULATION_SIZE.
CROSSOVER_CHANCE = 2 		# set of (0..10) 0 or 10 = 100% or 0% chance of crossover of genes, 5 = 50% chance of mutation.
MUTATION_CHANCE = 9 		# set of (0..10) 0 = 100% chance of mutation of digits in genes, 10 = 0% chance of mutation.

num_generations = int(sys.argv[2])

population = []
parents = []
offspring = []
given_puzzle = []
txt_file = sys.argv[1]
with open(txt_file) as f:
	for i in range(9):
		line = f.readline()
		stripped = line.strip()
		listed = stripped.split()
		for j in range(9):
			listed[j] = int(listed[j])
		given_puzzle.append(listed)

def duplicate_individual(ind):
	new_ind = []
	for i in range(9):
		new_ind.append(ind[i].copy())
	return new_ind

def initialize_population(given, pop_size):
	pop = []
	for i in range(pop_size):
		copy = duplicate_individual(given)
		for i in range(9):

			set = list(range(1, 10))
			random.seed(time.time())
			random.shuffle(set)
			for j in range(9):
				# fill temp with a random ordered set(1..9)
				if set[j] not in copy[i]:
					index = copy[i].index(0)
					copy[i][index] = set[j]

		pop.append(copy)
	return pop

def selection_operator(pop):
	paren = []
	for x in range(int(POPULATION_SIZE/2)):
		tour_winner_index = 0
		tour_winner_fitness = 999
		for y in range(TOURNAMENT_MATCH_SIZE):
			random.seed(time.time())
			match_index = random.randint(0,len(pop)-1)
			match_fitness = cal_fitness(pop[match_index])
			if match_fitness < tour_winner_fitness:
				tour_winner_index = match_index
				tour_winner_fitness = match_fitness
		paren.append(duplicate_individual(pop[tour_winner_index]))
	return paren

def crossover_operator(paren):
	offs = []
	for i in range(0, len(paren), 2):
		parent_1 = duplicate_individual(paren[i])
		parent_2 = duplicate_individual(paren[i+1])
		offspring_1 = []
		offspring_2 = []
		for i in range(9):
			random.seed(time.time())
			chance = random.randint(0,9)
			if chance >= CROSSOVER_CHANCE:
				offspring_1.append(parent_2[i].copy())
				offspring_2.append(parent_1[i].copy())
			else:
				offspring_1.append(parent_1[i].copy())
				offspring_2.append(parent_2[i].copy())
		offs.append(offspring_1)
		offs.append(offspring_2)
	return offs

def mutation_operator(offs):
	for x in range(len(offs)):
		for i in range(9):
			for j in range(9):
				if given_puzzle[i][j] == 0:
					random.seed(time.time())
					chance = random.randint(0,9)
					if chance >= MUTATION_CHANCE:
						random.seed(time.time())
						swap_with_index = random.randint(0,8)
						while swap_with_index == j or given_puzzle[i][swap_with_index] != 0:
							random.seed(time.time())
							swap_with_index = random.randint(0,8)
						temp = offs[x][i][swap_with_index]
						offs[x][i][swap_with_index] = offs[x][i][j]
						offs[x][i][j] = temp

def cal_fitness(ind):
	subgrid_score = 0
	column_score = 0

	temp_subgrid_1_list = []
	temp_subgrid_2_list = []
	temp_subgrid_3_list = []
	for i in range(0, 3):
		for j in range(0, 3):
			temp_subgrid_1_list.append(ind[i][j])
		for j in range(3, 6):
			temp_subgrid_2_list.append(ind[i][j])
		for j in range(6, 9):
			temp_subgrid_3_list.append(ind[i][j])
	subgrid_score = subgrid_score + 9 - len(set(temp_subgrid_1_list))
	subgrid_score = subgrid_score + 9 - len(set(temp_subgrid_2_list))
	subgrid_score = subgrid_score + 9 - len(set(temp_subgrid_3_list))
	# if [x for x in temp_subgrid_1_list if temp_subgrid_1_list.count(x) > 1]:
		# subgrid_score = subgrid_score + [x for x in temp_subgrid_1_list if temp_subgrid_1_list.count(x) > 1]
	# if [x for x in temp_subgrid_2_list if temp_subgrid_2_list.count(x) > 1]:
		# subgrid_score = subgrid_score + 1
	# if [x for x in temp_subgrid_3_list if temp_subgrid_3_list.count(x) > 1]:
		# subgrid_score = subgrid_score + 1
	
	temp_subgrid_1_list = []
	temp_subgrid_2_list = []
	temp_subgrid_3_list = []
	for i in range(3, 6):
		for j in range(0, 3):
			temp_subgrid_1_list.append(ind[i][j])
		for j in range(3, 6):
			temp_subgrid_2_list.append(ind[i][j])
		for j in range(6, 9):
			temp_subgrid_3_list.append(ind[i][j])
	subgrid_score = subgrid_score + 9 - len(set(temp_subgrid_1_list))
	subgrid_score = subgrid_score + 9 - len(set(temp_subgrid_2_list))
	subgrid_score = subgrid_score + 9 - len(set(temp_subgrid_3_list))
	# if [x for x in temp_subgrid_1_list if temp_subgrid_1_list.count(x) > 1]:
		# subgrid_score = subgrid_score + 1
	# if [x for x in temp_subgrid_2_list if temp_subgrid_2_list.count(x) > 1]:
		# subgrid_score = subgrid_score + 1
	# if [x for x in temp_subgrid_3_list if temp_subgrid_3_list.count(x) > 1]:
		# subgrid_score = subgrid_score + 1
	
	temp_subgrid_1_list = []
	temp_subgrid_2_list = []
	temp_subgrid_3_list = []
	for i in range(6, 9):
		for j in range(0, 3):
			temp_subgrid_1_list.append(ind[i][j])
		for j in range(3, 6):
			temp_subgrid_2_list.append(ind[i][j])
		for j in range(6, 9):
			temp_subgrid_3_list.append(ind[i][j])
	subgrid_score = subgrid_score + 9 - len(set(temp_subgrid_1_list))
	subgrid_score = subgrid_score + 9 - len(set(temp_subgrid_2_list))
	subgrid_score = subgrid_score + 9 - len(set(temp_subgrid_3_list))
	# if [x for x in temp_subgrid_1_list if temp_subgrid_1_list.count(x) > 1]:
		# subgrid_score = subgrid_score + 1
	# if [x for x in temp_subgrid_2_list if temp_subgrid_2_list.count(x) > 1]:
		# subgrid_score = subgrid_score + 1
	# if [x for x in temp_subgrid_3_list if temp_subgrid_3_list.count(x) > 1]:
		# subgrid_score = subgrid_score + 1

	for j in range(9):
		temp_column_list = []
		for i in range(9):
			temp_column_list.append(ind[i][j])
		column_score = column_score + 9 - len(set(temp_column_list))
		# if [x for x in temp_column_list if temp_column_list.count(x) > 1]:
			# column_score = column_score + 1	
	fitness = subgrid_score + column_score
	return fitness

# print("Initial pop:")
# population = initialize_population(given_puzzle, POPULATION_SIZE)
# for i in range(POPULATION_SIZE):
	# for j in range(9):
		# print(population[i][j])
	# print(cal_fitness(population[i]))
	# print("")
	
# parents = selection_operator(population)
# print(parents)
# for i in range(len(parents)):
	# for j in range(9):
		# print(parents[i][j])
	# print(cal_fitness(parents[i]))
	# print("")

# offspring = crossover_operator(population)
# print(offspring)
# for i in range(len(offspring)):
	# for j in range(9):
		# print(offspring[i][j])
	# print(cal_fitness(offspring[i]))
	# print("")

# mutation_operator(population)
# print(population)
# for i in range(POPULATION_SIZE):
	# for j in range(9):
		# print(population[i][j])
	# print(cal_fitness(population[i]))
	# print("")

lowest_fitness = 999
lowest_fitness_index = 0
total_fitness = []
min_fitness = []
population = initialize_population(given_puzzle, POPULATION_SIZE)
generation = 0
while (generation < num_generations) and (lowest_fitness > 0):
	generation = generation + 1
	print("Generation : ", generation)
	parents = selection_operator(population)
	offspring = crossover_operator(parents)
	mutation_operator(offspring)
	population = []
	for i in range(len(parents)):
		population.append(parents[i])
		population.append(offspring[i])
	lowest_fitness = 999
	lowest_fitness_index = 0
	total = 0
	for i in range(POPULATION_SIZE):
		check_fitness = cal_fitness(population[i])
		total = total + check_fitness
		if check_fitness < lowest_fitness:
			lowest_fitness = check_fitness
			lowest_fitness_index = i
	total_fitness.append(total)
	min_fitness.append(lowest_fitness)
	print("Lowest fitness:",lowest_fitness)
	print("Total fitness:",total)
print("Solution:")
sol = duplicate_individual(population[lowest_fitness_index])
for j in range(9):
	print(sol[j])
print("Solution fitness score:",lowest_fitness)
print("In generation:", generation)

min_value = min(total_fitness)
max_value = max(total_fitness)
plot.rcParams.update({'font.size': 24})
plot.plot(total_fitness, color='blue')
plot.title("Total fitness per generation")
plot.ylabel("Total fitness")
plot.xlabel("Generation")
plot.margins(0)
plot.ylim(min_value - 0.05 * abs(min_value), max_value + 0.05 * abs(max_value))
figure = plot.gcf()
figure.set_size_inches(20, 11)
figure.savefig('Total_Fitness_Plot.png', dpi=300)
plot.close("all")
with open('Total_Fitness_Plot_Data.txt', "w") as file:
	for value in total_fitness:
		file.write(str(value))
		file.write("\n")

with open('Solution_with_best_fitness.txt', "w") as file:
	for i in range(9):
		for j in range(9):
			file.write(str(sol[i][j]))
			file.write(" ")
		file.write("\n")