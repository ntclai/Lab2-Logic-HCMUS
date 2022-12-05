from copy import deepcopy

#Read from input file
def read_input_file(input_link):
	input_file = {}
	input_file['knowledge base'] = []
	content=[]
	with open(input_link, 'r') as fin:
		content = fin.read().splitlines()
	input_file['query'] = content[0]
	input_file['number of clauses'] = int(content[1])
	for i in range(2,len(content)):
		line = content[i].strip().split(' ')
		#filter out elements that are literals in line
		literals=[value for value in line if value !='OR' and value != '']
		literals.sort(key = inverse_literal)
		input_file['knowledge base'].append(' OR '.join(literals))
	fin.close()
	return input_file #dict

#Write to output file
def write_output_file(output_link, results_per_loop, entail):
	with open(output_link, 'w') as fout:
		for clauses in results_per_loop:
			fout.write('{}\n'.format(len(clauses)))
			for clause in clauses:
				fout.write('{}\n'.format(clause))
		fout.write('{}'.format('YES' if entail else '0\nNO'))
	fout.close()
	print('Finished writing to file!')

#Negate for literal
def negate_literal(literal):
	if(literal[0] == '-'):
		return literal[1:]
	else:
		return '-' + literal

#Negate the query clause
def negate_alpha(alpha):
	result=[]
	tokens=alpha.split(' ')
	for word in tokens:
		if (word == 'OR'):
			continue
		elif (word == 'AND'):
			result.append('OR')
		else: #word is a literal
			result.append(negate_literal(word))
	return result

def is_pointless(clause):
	temp = deepcopy(clause)
	if(len(temp) != 1):
		while (temp != []):
			literal = temp.pop()
			if ('-' + literal in temp) or (literal[1:] in temp):
				return True
	return False

def inverse_literal(literal):
	if (literal[0] == '-'):
		return literal[1:]
	return literal

#Check 2 inverses
def is_inverse(literal_a, literal_b):
	if(literal_a =='-'+literal_b or literal_b == '-'+ literal_a):
		return True

#Remove a literal from a clause
def remove_literal(clause, literal_need_remove):
	temp = deepcopy(clause)
	for literal in clause:
		if (literal == literal_need_remove):
			temp.remove(literal)
	return temp

#Create a new clause by connect 2 clauses
def create_new_clause(clause1, clause2):
	clause1.extend(clause2)
	new_clause = list(set(clause1))
	new_clause = [literal for literal in new_clause if literal != '']
	return new_clause

#Connect list to a clause
def combine(clause):
	clause.sort(key = inverse_literal)
	for literal in clause:
		if literal == '':
			clause.remove('')
	return ' OR '.join(clause) #list -> str

def resolve(clause1, clause2):
	clauses = set()
	literals_in_clause1 = [literal for literal in clause1.split(' ') if literal != 'OR']
	literals_in_clause2 = [literal for literal in clause2.split(' ') if literal != 'OR']	
	for i in literals_in_clause1:
		for j in literals_in_clause2:
			if(is_inverse(i, j)):
				new_i = remove_literal(literals_in_clause1, i)
				new_j = remove_literal(literals_in_clause2, j)
				new_clause = create_new_clause(new_i, new_j)
				if not is_pointless(new_clause):
					new_clause = combine(new_clause)
					clauses.update({new_clause})
	return clauses



