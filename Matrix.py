#!/usr/bin/python3
# -*- encoding UTF-8 -*-

"""
@author Lucas Elvira Martín
@size september 2018
@version 2.1
"""
from functools import reduce

class Matrix:
	"""Clase matriz. Sirve para definir las propiedades de un matrix y manipularla con cierta facilidad"""

	def __init__(self, col = 1, row=1, val = 0, diagonal=False):
		
		if (type(col) == list or type(col) == tuple) and (type(col[0]) == list or type(col[0]) == tuple):
				self.__matrix = [[i for i in j] for j in col]
		elif (type(col) == list or type(col) == tuple) and (type(row) != list or type(row) != tuple):
			if diagonal:		
				#self.__matrix = [col[i] if i == j else val for i in range(len(col))]for j in range(len(col))]
				self.__matrix = col
			else:
				self.__matrix = [[c for c in col] for i in range(row)]
		elif (type(row) == list or type(row) == tuple) and (type(col) != list or type(col) != tuple):
			if col>1:
				self.__matrix = [list(v) for v in zip(*[[r for r in row] for i in range(col)])]
			else:
				self.__matrix = [[r] for r in row for i in range(col)]
		else:
			self.__matrix = [[val for i in range(col)]for j in range(row)]
		self.errors = {"size": "the size of the operators are incompatible with this operations", "notSquare": "the matrix is not sqare. This operation is not allowed"}
		self.diagonal = diagonal
	def __str__(self):
		"""
		Metodo encargado de definir como se debe ver la matriz a la hora de imprimirse.
		Si es el tablero o se usa como contenedor, eso determina como se va a mostrar
		Por defecto, el jugador uno tiene una x y el jugador dos una o 
		"""
		return "\n".join("  ".join([str(i) for i in r]) for r in self.__matrix) if not self.diagonal else "\n".join("  ".join([str(self.__matrix[i]) if i == j else "0" for i in range(len(self.__matrix))]) for j in range(len(self.__matrix)))

	def __setitem__(self, k, value):
		"""
			metodo encargado de determinar como debe sobreescribirse un elemento de la matriz.
			k (tuple) posiciones j e i de la matriz
			value (int) nuevo valor de dicha posición			
		"""
		if not self.diagonal:
			self.__matrix[k[0]][k[1]] = value
		else:
			if k[0] == k[1]:
				self.__matrix[k[1]] = value
			else:
				m = [[self.__matrix[i] if i == j else 0 for i in range(len(self.__matrix))]for j in range(len(self.__matrix))]
				m[k[0]][k[1]] = value
				self.__matrix = m;
				self.diagonal = False;
	def __getitem__(self, n):
		"""
		metodo encargado de devolver un valor de la posición
		n (tuple) | (int)
		if type(n) tuple
			return (int) n[0] |-> j || n[1] |-> i
		if type (n) int
			return (list) n |-> j
		"""
		if self.diagonal:
			if isinstance(n, tuple):
				return 0 if n[0] != n[1] else self.__matrix[n[0]]
			elif isinstance(n, int):
				return [0 if n!=i else self.__matrix[n] for i in range(len(self.__matrix))]

		if isinstance(n, tuple):
			return self.__matrix[n[0]][n[1]]
		elif isinstance(n, int):
			return self.__matrix[n]

	def __len__(self):
		"""
		metodo encargado de devolver la logitud en columnas de la matrix
		"""
		return len(self.__matrix)

	def __iter__(self):
		"""
		metodo encargado de unir todas las filas de una matriz en una sola
		"""
		m = []
		for j in self.__matrix:
			m += j
		return iter(m)

	def __add__(self, k):
		"""
		Suma dos matrices. Para que se puedan sumar deben tener el mismo tamaño es decir el mismo
		numero de filas por el mismo numero de columnas.
		En caso contrartio salta una excepcion
		"""
		if self.diagonal:
			if len(self.__matrix) == len(k) == len(k[0]):
				return Matrix([[k[j][i] + self.__matrix[i] if i==j else k[j][i] for i in range(len(k[j]))]for j in range(len(k))])
		else:
			if len(self.__matrix) == len(k) == len(self.__matrix[0]):
				return Matrix([[k.__matrix[i] + self.__matrix[j][i] if i==j else self.__matrix[j][i] for i in range(len(k[j]))]for j in range(len(k))])
		if len(k) == len(self) or len(k[0]) != len(self.__matrix[0]):
			return Matrix([[k[j][i] + self.__matrix[j][i] for i in range(len(k[j]))]for j in range(len(k))])
		else:
			return self.errors["size"]
	
	def __mul__(self, k=1):
		
		#return [[sum([self.__matrix[z][i]*k[i][z] for i in range(len(self.__matrix), z)]) for z in range(len(self.__matrix))]for j in range(len(self.__matrix))]
		if type(k) == int:
			return Matrix([[i*k for i in j] for j in self.__matrix]) if not self.diagonal else Matrix([[0 if i!=j else self.__matrix[i]*k for i in range(len(self.__matrix))] for j in range(len(self.__matrix))])
		if self.diagonal:
			if len(k) == len(k[0]) == len(self.__matrix):
				return Matrix([[self.__matrix[j]*k[j][i] for i in range(len(self.__matrix))]for j in range(len(self.__matrix))])
		elif k.diagonal:
			if len(k) == len(self.__matrix[0]) == len(self.__matrix):
				return Matrix([[k.__matrix[j]*self.__matrix[j][i] for i in range(len(self.__matrix))]for j in range(len(self.__matrix))])
		elif len(self.__matrix[0]) == len(k):
			return Matrix([[sum([self.__matrix[j][l]*k[l][i] for l in range(len(k))]) for i in range(len(k[0]))]for j in range(len(self.__matrix))])
		else:
			return self.errors["size"]

	#Generadores
	def index(self, value, dimensions = 2):
		"""
		metdo encargado de buscar un valor en una matriz y
		devolver todas las posiciones en las que se encuentra
		"""		
		if dimensions is 1:
			for i in range(len(l)):
				if l[i] is n:
					yield i
		elif dimensions is 2:
			for j in range(len(self.__matrix)):
				for i in range(len(self.__matrix[j])):
					if self.__matrix[j][i] is value:
						yield j, i

	def get_combine(self):
		return [self.__matrix, self.transpuest(), self.getDiagonal()]

	def transpuest(self):
		m = []
		for i in range(len(self.__matrix[0])):			
			m.append([])
			for h in range(len(self.__matrix)):
				m[-1].append(self.__matrix[h][i])
		return Matrix(m)

	def get_diagonal(self):
		if not len(self.__matrix) == len(self.__matrix[0]):
			return [],[]
		d1, d2 = [], []
		for j in range(len(self.__matrix)):
			d1.append(self.__matrix[j][j])
			d2.append(self.__matrix[j][-j-1])
		self.d1 = d1
		self.d2 = d2
		return [d1, d2]

	def sum(self):
		"""
		Este metodo se encarga de analizar la matriz y devolver un array con la suma de todas las
		combinaciones de 3 posibles
		"""
		the_sum = []
		tables = [self.__matrix, self.t, [self.d1, self.d2]]
		zeros, iterations = 0, 0
		for j in tables:
			for i in j:
				iterations+=1
				a = [p for p in i]
				the_sum.append(reduce(lambda x, y : x+y, a))
				if 0 not in a:
					zeros+=1
		return the_sum if zeros != iterations else False

	def determinante(self):
		if len(self) !=len(self.__matrix[0]):
			return self.errors["notSquare"]
		m = self.__matrix
		n, det = len(m), 0
		if n==2:
			return m[0][0]*m[1][1]-m[0][1]*m[1][0]
		elif n == 3:
			for i in range(n):
				a = reduce((lambda x, y : x*y), [m[x][i+x-n] for x in range(n)])
				b = reduce((lambda x, y: x*y), [m[x][n-1-x-i] for x in range(n)])
				det += a-b
			return det
		#Primero buscamos la fila o columna con más 0
		t = transversa(m)
		zeros = tuple(row.count(0) for row in m) + tuple(row.count(0) for row in t)
		i = zeros.index(max(zeros))		
		if i >= len(m):
			i-=len(m)
			m = t

		fila = m[i]
		m = [m[x] for x in range(len(m)) if x != i]	
		for j in range(len(m[0])):		
			adj = [[row[f] for f in range(len(row)) if f != j] for row in m]		
			if fila[j] != 0:
				det += (-1)**(i+j)*fila[j]*determinante(adj)
		return det

	def __gauss_jordan(self, jordan = True):
		if self.diagonal:
			return [[1 if i==j else 0 for i in range(len(self.__matrix))]for j in range(len(self.__matrix))]
		m = self.__matrix
		#En este for realiza gauss
		for i in range(len(m[0])):
			for j in range(len(m)-1,i,-1):
				d = m[i][i]/m[j][i]
				m[j] = [sum(v) for v in list(zip(m[i], list(map(lambda x: x*-d, m[j]))))]
		if not jordan:
			return m
		#Comenzaos con la reduccion por jordan también
		
		for j in range(len(m)-1, -1, -1):			
			for i in range(len(m[0])-1, j-1, -1):				
				if j != i:
					d = m[i][i]/m[j][i]
					m[j] = [sum(v) for v in list(zip(m[i], list(map(lambda x: x*-d, m[j]))))]
		return m
				#d = m[i][i]/m[j][i]
				#print(sum(list(zip(m[0], list(map(lambda x: x*-d, m[j]))))))
				#m[j][i] = sum(zip(m[j], [j]))
		
	def getRange(self):
		m = self.__gauss_jordan()
		print(m)
		n = len(m)
		for i in range(n-1, -1, -1):
			if all(m[i]):
				n-=1
			else:
				break
		return n

