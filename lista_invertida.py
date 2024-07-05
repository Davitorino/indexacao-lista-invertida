from funcionario import Funcionario
from enum import Enum


class Criterio(Enum):
    CARGO = 1
    DEPARTAMENTO = 2
    SALARIO = 3


class ListaInvertida:

    def __init__(self):
        self.__registros: list[Funcionario] = []
        self._dir_cargo: dict[str, set[Funcionario]] = {}
        self._dir_departamento: dict[str, set[Funcionario]] = {}
        self._dir_salario: dict[str, set[Funcionario]] = {}

    @property
    def registros(self):
        return self.__registros

    def buscar(self, cpf: str):
        for funcionario in self.__registros:
            if funcionario.cpf == cpf:
                return funcionario

    def busca_criterio_simples(self, criterio: Criterio, valor: str):
        if criterio == Criterio.CARGO:
            return self._dir_cargo.get(valor.lower(), set())
        if criterio == Criterio.DEPARTAMENTO:
            return self._dir_departamento.get(valor.lower(), set())
        if criterio == Criterio.SALARIO:
            return self._dir_salario.get(valor.lower(), set())

    def busca_criterio_combinada(self, prim_criterio: Criterio, prim_valor: str, seg_criterio: Criterio, seg_valor: str):
        prim_registros: set[Funcionario] = self.busca_criterio_simples(prim_criterio, prim_valor)
        seg_registros: set[Funcionario] = self.busca_criterio_simples(seg_criterio, seg_valor)
        return prim_registros.intersection(seg_registros)

    def inserir(self, funcionario: Funcionario):
        self.__registros.append(funcionario)
        self.__adicionar_no_diretorio(self._dir_cargo, funcionario.cargo, funcionario)
        self.__adicionar_no_diretorio(self._dir_departamento, funcionario.departamento, funcionario)
        self.__adicionar_no_diretorio(self._dir_salario, self.obter_range_salario(funcionario.salario), funcionario)

    def remover(self, cpf: str):
        funcionario = self.buscar(cpf)
        if not funcionario:
            return False
        self.__registros.remove(funcionario)
        self.__remover_do_diretorio(self._dir_cargo, funcionario.cargo, funcionario)
        self.__remover_do_diretorio(self._dir_departamento, funcionario.departamento, funcionario)
        self.__remover_do_diretorio(self._dir_salario, self.obter_range_salario(funcionario.salario), funcionario)
        return True

    def obter_range_salario(self, salario: float):
        if salario <= 5000:
            return '0-5000'
        if salario <= 10000:
            return '5001-10000'
        return '10000+'

    def __adicionar_no_diretorio(self, diretorio: dict[str, set[Funcionario]], valor: str, obj: Funcionario):
        if not diretorio.get(valor.lower()):
            diretorio[valor.lower()] = set()
        diretorio[valor.lower()].add(obj)

    def __remover_do_diretorio(self, diretorio: dict[str, set[Funcionario]], valor: str, obj: Funcionario):
        if not diretorio.get(valor.lower()):
            return
        diretorio[valor.lower()].remove(obj)
