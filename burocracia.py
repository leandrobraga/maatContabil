#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Copyright 2008-2009 Rudá Moura & Elvis Pfützenreuter.
# All Rights Reserved.
# 

"""Classes e rotinas para tratar com a burocracia Brasileira.

Classes:
  - CPF -- Classe para manipular um Cadastro de Pessoas Físicas.
  - CNPJ -- Classe para manipular um Cadastro Nacional da Pessoa Jurídica.
  - PIS -- Classe para manipular o Programa de Integração Social.
  - TituloEleitor -- Classe para manipular o Título Eleitoral.

Rotinas:
  - validate_cpf() -- Valida um CPF.
  - validate_cnpj() -- Valida um CNPJ.
  - validate_pis() -- Valida um PIS/PASEP.
  - validate_titulo_eleitor() -- Valida um Título de Eleitor.
"""

d2c = lambda x: chr(ord('0')+x)		# yes, I love lambda (ruda)

class CPFError(ValueError):
	pass
class CNPJError(ValueError):
	pass
class PISError(ValueError):
	pass
class TituloEleitorError(ValueError):
	pass

class Validator(object):
	"""Classe abstrata de um validador."""
	
	def __init__(self, data):
		"""Parseia a string data e cria um novo objeto."""
		self.digits = []
		self.valid = None
		self._parse(data)

	def __eq__(self, other):
		equal = lambda x, y: x == y
		l = map(equal, self.digits, other.digits)
		return reduce(equal, l)
	
	def __repr__(self):
		return str(self.digits)

	def _parse(self, data):
		"""Parseia a string data, que contém os dígitos."""
		pass
	
	def _validate(self):
		"""Validação dos dígitos e guarda o resultado em valid."""
		pass
	
	def isValid(self):
		"""Verifica se os dígitos com o verificador são válidos."""
		if self.valid is not None:
			return self.valid
		self._validate()
		return self.valid

class CPF(Validator):
	"""Classe para manipular o Cadastro de Pessoas Físicas.
	
	Formato de entrada: ddd.ddd.ddd-dd.
	
	Exemplos:
	
	>>> cpf = CPF("12345678901")
	>>> print cpf.isValid()
	False
	>>> cpf = CPF("12345678909")
	>>> print cpf.isValid()
	True
	>>> print "CPF", cpf
	CPF 123.456.789-09
	>>> cpf = CPF("123.456.789-09")
	>>> print cpf.isValid()
	True
	>>> other = CPF("111.222.333.00")
	>>> print cpf == cpf
	True
	>>> print cpf == other
	False
	>>> try: cpf = CPF("123/456/789.00")
	... except CPFError, e: print "Oops:", e
	... 
	Oops: Unexpected symbol '/' found
	"""

	def _parse(self, s):
		for c in s:
			if c == '.' or c == ' ' or c == '\t': continue
			if c == '-':
				if len(self.digits) != 9:
					raise CPFError, "Not enough digits"
				continue
			if c.isdigit():
				self.digits.append(int(c))
				continue
			raise CPFError, "Unexpected symbol '%s' found" % c
		if len(self.digits) != 11:
			raise CPFError, "Wrong number of digits (11 expected)"

	def __str__(self):
		g1 = "".join([d2c(x) for x in self.digits[0:3]])
		g2 = "".join([d2c(x) for x in self.digits[3:6]])
		g3 = "".join([d2c(x) for x in self.digits[6:9]])
		v = "".join([d2c(x) for x in self.digits[9:11]])
		return "%s.%s.%s-%s" % (g1, g2, g3, v)
	
	def _validate(self):
		v = [None, None]
		v[0]  = 10*self.digits[0] + 9*self.digits[1] + 8*self.digits[2]
		v[0] +=  7*self.digits[3] + 6*self.digits[4] + 5*self.digits[5]
		v[0] +=  4*self.digits[6] + 3*self.digits[7] + 2*self.digits[8]
		v[0]  = 11 - v[0] % 11
		if v[0] >= 10: v[0] = 0
		v[1]  = 11*self.digits[0] + 10*self.digits[1] + 9*self.digits[2]
		v[1] +=  8*self.digits[3] +  7*self.digits[4] + 6*self.digits[5]
		v[1] +=  5*self.digits[6] +  4*self.digits[7] + 3*self.digits[8]
		v[1] += 2*v[0]
		v[1]  = 11 - v[1] % 11
		if v[1] >= 10: v[1] = 0
		self.valid = (self.digits[9] == v[0]) and (self.digits[10] == v[1])

class CNPJ(Validator):
	"""Classe para manipular o Cadastro Nacional da Pessoa Jurídica.
	
	Formato de entrada: dd.ddd.ddd/dddd-dd.
	
	Exemplos:
	
	>>> cnpj = CNPJ("11.222.333/0001-00")
	>>> print cnpj.isValid()
	False
	>>> bb = CNPJ("00.000.000/0001-91")
	>>> print bb.isValid()
	True
	"""
	def _parse(self, s):
		for c in s:
			if c == '.' or c == '/' or c == ' ' or c == '\t':
				continue
			if c == '-':
				if len(self.digits) != 12:
					raise CNPJError, "Not enough digits"
				continue
			if c.isdigit():
				self.digits.append(int(c))
				continue
			raise CNPJError, "Unexpected symbol '%s' found" % c
		if len(self.digits) != 14:
			raise CNPJError, "Wrong number of digits (14 expected)"

	def __str__(self):
		g1 = "".join([d2c(x) for x in self.digits[0:2]])
		g2 = "".join([d2c(x) for x in self.digits[2:5]])
		g3 = "".join([d2c(x) for x in self.digits[5:8]])
		g4 = "".join([d2c(x) for x in self.digits[8:12]])
		v = "".join([d2c(x) for x in self.digits[12:14]])
		return "%s.%s.%s/%s-%s" % (g1, g2, g3, g4, v)

	def _validate(self):
		v = [None, None]
		v[0]  =  6*self.digits[0] + 7*self.digits[1] + 8*self.digits[2]
		v[0] +=  9*self.digits[3] + 2*self.digits[4] + 3*self.digits[5]
		v[0] +=  4*self.digits[6] + 5*self.digits[7] + 6*self.digits[8]
		v[0] +=  7*self.digits[9] + 8*self.digits[10] + 9*self.digits[11]
		v[0] = v[0] % 11
		if v[0] == 10: v[0] = 0
		v[1]  =  5*self.digits[0] + 6*self.digits[1] + 7*self.digits[2]
		v[1] +=  8*self.digits[3] + 9*self.digits[4] + 2*self.digits[5]
		v[1] +=  3*self.digits[6] + 4*self.digits[7] + 5*self.digits[8]
		v[1] +=  6*self.digits[9] + 7*self.digits[10] + 8*self.digits[11]
		v[1] +=  9*self.digits[12]
		v[1] = v[1] % 11
		if v[1] == 10: v[1] = 0
		self.valid = (self.digits[12] == v[0]) and (self.digits[13] == v[1])

class PIS(Validator):
	"""Classe para manipular o Programa de Integração Social.

	Formato de entrada: ddd.ddddd.dd-d.

	Exemplos:

	>>> pis = PIS("12345678900")
	>>> print pis.isValid()
	True
	>>> pis = PIS("12345678901")
	>>> print pis.isValid()
	False

	Fonte: http://www.macoratti.net/dica66.htm
	"""

	def _parse(self, s):
		for c in s:
			if c == '.' or c == ' ' or c == '\t': continue
			if c == '-':
				if len(self.digits) != 10:
					raise PISError, "Not enough digits"
			if c.isdigit():
				self.digits.append(int(c))
				continue
			raise PISError, "Unexpected symbol '%s' found" % c
		if len(self.digits) != 11:
			raise PISError, "Wrong number of digits (11 expected)"

	def __str__(self):
		g1 = "".join([d2c(x) for x in self.digits[0:3]])
		g2 = "".join([d2c(x) for x in self.digits[3:8]])
		g3 = "".join([d2c(x) for x in self.digits[8:10]])
		v = "".join([d2c(x) for x in self.digits[10:11]])
		return "%s.%s.%s-%s" % (g1, g2, g3, v)

	def _validate(self):
		height = [int(x) for x in "3298765432"]
		sum = 0
		for i in range(10):
			sum += self.digits[i] * height[i]
		rest = sum % 11
		if rest != 0:
			rest = 11 - rest
		self.valid = (rest == self.digits[10])

class TituloEleitor(Validator):
	"""Classe para manipular o Título Eleitoral.
	
	Formato de entrada: dddddddddddd.

	Exemplos:

	>>> te = TituloEleitor("123456789012")
	>>> print te.isValid()
	False

	Fonte: http://www.exceldoseujeito.com.br/2008/12/19/validar-cpf-cnpj-e-titulo-de-eleitor-parte-ii/
	"""
	
	cod_states = {
		(0, 1): "SP", (1, 5): "PI",
		(0, 2): "MG", (1, 6): "RN",
		(0, 3): "RJ", (1, 7): "AL",
		(0, 4): "RS", (1, 8): "MT",
		(0, 5): "BA", (1, 9): "MS",
		(0, 6): "PR", (2, 0): "DF",
		(0, 7): "CE", (2, 1): "SE",
		(0, 8): "PE", (2, 2): "AM",
		(0, 9): "SC", (2, 3): "RS",
		(1, 0): "GO", (2, 4): "AC",
		(1, 1): "MA", (2, 5): "AP",
		(1, 2): "PB", (2, 6): "RR",
		(1, 3): "PA", (2, 7): "TO",
		(1, 4): "ES", (2, 8): "ZZ", # ZZ -> exterior
	}
	
	def _parse(self, s):
		for c in s:
			if c == '.' or c == '-' or c == ' ' or c == '\t':
				continue
			if c.isdigit():
				self.digits.append(int(c))
				continue
			raise TituloEleitorErrror, "Unexpected symbol '%s' found" % c
		if len(self.digits) != 12:
			raise TituloEleitorError, "Wrong number of digits (12 expected)"

	def __str__(self):
		return "".join([str(x) for x in self.digits])

	def _validate(self):
		heights = [int (x) for x in "23456789789"]
		sum = 0
		for i in range(8):
			sum += self.digits[i] * heights[i]
		rest1 = sum % 11
		if rest1 == 10: rest1 = 0
		sum = 0
		for i in range(8, 11):
			sum += self.digits[i] * heights[i]
		rest2 = sum % 11
		if rest2 == 10: rest2 = 0
		self.valid = (rest1 == self.digits[10] and rest2 == self.digits[11])

	def state(self):
		"""Retorna o estato emissor do título."""
		try:
			s = self.cod_states[tuple(self.digits[8:10])]
		except KeyError:
			self.valid = False
			raise TituloEleitorError, "State not valid"
		return s


def validate_cpf(entrada):
	"""Valida um CPF (retorna True ou False).
	Exemplo:
	>>> print validate_cpf("111.222.333-44")
	False
	"""
	try:
		cpf = CPF(entrada)
	except CPFError:
		return False
	return cpf.isValid()

def validate_cnpj(entrada):
	"""Valida um CNPJ (retorna True ou False).
	Exemplo:
	>>> print validate_cnpj("11.222.333/0001-00")
	False
	"""
	try:
		cnpj = CNPJ(entrada)
	except CNPJError:
		return False
	return cnpj.isValid()

def validate_pis(entrada):
	""" Valida um PIS (retorna True ou False).
	Exemplo:
	>>> print validate_pis("111.22222.33-4")
	False
	"""
	try:
		pis = PIS(entrada)
	except PISError:
		return False
	return pis.isValid()

def validate_titulo_eleitor(entrada):
	"""Valida um Título de Eleitor (retorna True ou False).
	Exemplo:
	>>> print validate_titulo_eleitor("106644440302")
	True
	"""
	try:
		te = TituloEleitor(entrada)
	except TituloEleitorError:
		return False
	return te.isValid()

def _test():
	import doctest
	doctest.testmod()

if __name__ == '__main__':
	_test()
