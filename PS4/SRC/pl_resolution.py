#-------------------------------------- PL-RESOLUTION ------------------------------------
from copy import deepcopy
from helper_functions import resolve, negate_alpha
import itertools

#Resolution algorithm for propositional logic
def pl_resolution(KB, alpha):
	#some initialization variables
	number_clauses_step=[]
	number_clauses_step.append(0)
	list_clauses_step=[]
	entail = False

	#start the algorithm
	negative_alpha=negate_alpha(alpha)#get nagatetive alpha
	clauses = deepcopy(KB)#existing clauses knowledge base
	clauses.extend(negative_alpha)#Set of clauses in KB and negation of alpha
	new_clauses = set()
	new_list_clauses=[]
	while True:
		count_steps = 0
		combinations=itertools.combinations(sorted(clauses), 2)
		for (clause1, clause2) in combinations:
			resolvents = resolve(clause1, clause2)
			if ('' in resolvents):
				entail = True
			for res in resolvents:
				if (res not in new_list_clauses):
					new_list_clauses.append(res)
		for n in new_list_clauses:
			new_clauses.add(n)
		set_clauses = set(clauses)
		if new_clauses <= set_clauses:
			return False, number_clauses_step, list_clauses_step
		for clause in new_list_clauses:
			if (clause not in clauses):
				count_steps = count_steps + 1
				if clause == '':
					list_clauses_step.append('{}')
				else:
					list_clauses_step.append(clause)
				clauses.append(clause)
		number_clauses_step.append(count_steps)
		if (entail):
			return True, number_clauses_step, list_clauses_step
