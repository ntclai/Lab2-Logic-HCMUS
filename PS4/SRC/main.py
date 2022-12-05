  
#-------------------------------------- MAIN -----------------------------------------
from pl_resolution import pl_resolution
from helper_functions import read_input_file, write_output_file
import os

def get_clauses_per_loop(number_clauses_step, list_clauses_step):
	clauses_per_loop=[]
	for i in range(1, len(number_clauses_step)):
		number_clauses_step[i] = number_clauses_step[i] + number_clauses_step[i - 1]
	for i in range(1, len(number_clauses_step)):
		temp = list_clauses_step[number_clauses_step[i-1]: number_clauses_step[i]]
		clauses_per_loop.append(temp)
	return clauses_per_loop

def main():
	inputs=[]
	input_path='./INPUT'
	files=os.listdir(input_path)
	inputs=[input_path+'/'+file for file in files]
	outputs=[i.replace('IN','OUT') for i in inputs]
	outputs=[o.replace('in','out') for o in outputs]

	for i in range(len(outputs)):
		file_in = read_input_file(inputs[i])
		alpha = file_in['query']
		KB = file_in['knowledge base']
		entail, number_clauses_step, list_clauses_step = pl_resolution(KB, alpha)
		clauses_per_loop=get_clauses_per_loop(number_clauses_step, list_clauses_step)
		#write result to file
		write_output_file('OUTPUT/output5.txt', clauses_per_loop,  entail)
	
if __name__ == '__main__':
	main()






























