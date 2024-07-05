from lista_invertida import ListaInvertida, Criterio
from funcionario import Funcionario


class Interface:
    def __init__(self):
        self.__criterios = {
            1: Criterio.CARGO,
            2: Criterio.DEPARTAMENTO,
            3: Criterio.SALARIO,
        }
        self.__indexacao = ListaInvertida()

    def init_interface(self):
        while True:
            print('================================')
            print('1 - Obter todos os registros')
            print('2 - Buscar por CPF')
            print('3 - Buscar por critério único')
            print('4 - Buscar por critério composto')
            print('5 - Inserir registro')
            print('6 - Inserir em lote')
            print('7 - Remover registro')
            print('8 - Sair')
            print('================================')

            opcoes = {
                1: self.__obter_registros,
                2: self.__buscar_por_cpf,
                3: self.__buscar_criterio_unico,
                4: self.__buscar_criterio_composto,
                5: self.__inserir_registro,
                6: self.__inserir_registro_lote,
                7: self.__remover_registro,
                8: exit
            }

            try:
                opcao = int(input('Escolha uma ação: '))
                if opcao < 1 or opcao > 8:
                    raise ValueError
                opcoes[opcao]()
            except ValueError:
                print('Digite uma opção válida')

    def __formatar_funcionario(self, funcionario: Funcionario):
        return f'Nome: {funcionario.nome} - CPF: {funcionario.cpf} - Cargo: {funcionario.cargo} - Departamento: {funcionario.departamento} - Salário: R${funcionario.salario}'

    def __obter_registros(self):
        print('\n'.join([
            self.__formatar_funcionario(funcionario)
            for funcionario in self.__indexacao.registros
        ]))

    def __buscar_por_cpf(self):
        cpf = input('Informe o CPF: ')
        funcionario = self.__indexacao.buscar(cpf)
        if funcionario:
            print(self.__formatar_funcionario(funcionario))
            return
        print('Funcionário não encontrado!')

    def __obter_criterio(self):
        try:
            print('1 - Cargo')
            print('2 - Departamento')
            print('3 - Salário')
            opcao = int(input('Informe o critério: '))
            if opcao < 1 or opcao > 3:
                raise ValueError
            valor = input('Informe o valor: ')
            return self.__criterios[opcao], valor
        except ValueError:
            print('Digite uma opção válida')

    def __buscar_criterio_unico(self):
        criterio, valor = self.__obter_criterio()
        valor = self.__indexacao.obter_range_salario(float(valor)) if criterio == Criterio.SALARIO else valor
        funcionarios = self.__indexacao.busca_criterio_simples(criterio, valor)
        if not funcionarios:
            print('Nenhum registro encontrado!')
            return
        print('\n'.join([
            self.__formatar_funcionario(funcionario)
            for funcionario in funcionarios
        ]))

    def __buscar_criterio_composto(self):
        print('--- Primeiro critério --- ')
        prim_criterio, prim_valor = self.__obter_criterio()
        print('--- Segundo critério ---')
        seg_criterio, seg_valor = self.__obter_criterio()
        prim_valor = self.__indexacao.obter_range_salario(float(prim_valor)) if prim_criterio == Criterio.SALARIO else prim_valor
        seg_valor = self.__indexacao.obter_range_salario(float(seg_valor)) if seg_criterio == Criterio.SALARIO else seg_valor
        funcionarios = self.__indexacao.busca_criterio_combinada(prim_criterio, prim_valor, seg_criterio, seg_valor)
        if not funcionarios:
            print('Nenhum registro encontrado!')
            return
        print('\n'.join([
            self.__formatar_funcionario(funcionario)
            for funcionario in funcionarios
        ]))

    def __inserir_registro(self):
        cpf = input('Informe o CPF: ')
        nome = input('Informe o nome: ')
        cargo = input('Informe o cargo: ')
        departamento = input('Informe o departamento: ')
        salario = float(input('Informe o salário: '))
        self.__indexacao.inserir(Funcionario(cpf, nome, cargo, departamento, salario))
        print('Funcionário inserido com sucesso!')

    def __inserir_registro_lote(self):
        nome_csv = input('Informe o nome do CSV: ')
        arquiv_csv = open(nome_csv)
        for registro in arquiv_csv.read().split('\n'):
            cpf, nome, cargo, departamento, salario = registro.split(',')
            self.__indexacao.inserir(Funcionario(cpf, nome, cargo, departamento, float(salario)))
        arquiv_csv.close()
        print('Funcionários inseridos com sucesso!')

    def __remover_registro(self):
        cpf = input('Informe o CPF: ')
        removido = self.__indexacao.remover(cpf)
        print('Funcionário removido com sucesso!') if removido else print('Funcionário não encontrado!')
