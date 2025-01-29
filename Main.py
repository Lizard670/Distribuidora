menus["vendas"] = '''
1) Ver vendas
2) Adicionar venda
3) Editar venda
4) Remover venda
0) Voltar
    Opção: '''
menus["venda"] = '''
O que deseja editar?
1) Produto
2) Quantidade
3) Data
4) Desconto
0) Cancelar
    Opção: '''


def main():
    # Pede para carregar informações já salvas
    # TODO
    # Caso não abra, cria novo estabelecimento
    distribuidora = Estabelecimento()

    # Loop principal do programa, continua rodando até que o usuário selecione para sair
    while (True):
        # O menu retorna True quando for para encerrar o programa
        if menu_principal(distribuidora):
            break


def menu_principal(estabelecimento):
    # Pega a opção que o usuário selecionou
    opcao = int(input('''
1) Gerenciar estoque
2) Gerenciar vendas
3) Ver estatísticas
0) Encerrar programa
    Opção: '''))

    # Encerrar programa
    if opcao == 0:
        # Pergunta se o usuário quer salvar antes de sair
        # TODO
        return True
    # Gerenciar estoque
    elif opcao == 1:
        gerenciar_estoque(estabelecimento)
    # Gerenciar vendas
    elif opcao == 2:
        gerenciar_estoque(estabelecimento)
    # Ver estatísticas
    elif opcao == 3:
        exibir_estatisticas(estabelecimento)


def gerenciar_estoque(estabelecimento):
    texto_menu = '''
1) Ver produtos
2) Adicionar produto
3) Editar produto
4) Ativar/Desativar produto
5) Remover produto
0) Voltar
    Opção: '''
    opcao = int(input(texto_menu))
    while opcao != 0:
        if opcao == 1:
            estabelecimento.exibir_estoque()
        elif opcao == 2:
            estabelecimento.novo_produto()
        elif opcao == 3:
            estabelecimento.exibir_estoque()
            id = int(input("Selecione um produto para editar"))
            estabelecimento.editar_produto(id)

        elif opcao == 4:
            pass
        elif opcao == 5:
            pass

        opcao = int(input(texto_menu))


def gerenciar_estoque(estabelecimento):
    # TODO
    pass


def exibir_estatisticas(estabelecimento):
    # TODO
    pass


class Estabelecimento:
    def __init__(self):
        self.estoque = []
        self.vendas = []
        # Proximo id que vai ser entregado quando criar um novo produto
        self.proximo_id = 0

    def exibir_estoque(self):
    # TODO
        pass

    def exibir_vendas(self):
    # TODO
        pass

    def novo_produto(self, nome=None, preco=None, quantidade=None):
        if nome is None:
            nome = input("Insira o nome do produto: ")

        if preco is None:
            preco = float(input("Insira o valor: "))

        if quantidade is None:
            quantidade = int(input("Insira a quantidade inicial: "))

        self.estoque.append(Produto(nome, preco, self.proximo_id, quantidade))
        self.proximo_id += 1  # Atualiza o proximo id


    def editar_produto(self, id_produto):
        for produto in self.estoque:
            # Checa se o id é igual ao id do produto que deseja editar
            if id_produto == produto.id_numerico:
                opcao = int(input('''
        O que deseja editar?
        1) Nome
        2) preço
        3) Quantidade
        0) Cancelar
            Opção: '''))


class Produto:
    def __init__(self, nome, preco, id_numerico, quantidade=0):
        self.id_numerico = id_numerico
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

        self.ativo = True


class Venda:
    def __init__(self, produto, quantidade, data, desconto=1):
        self.id_produto = produto.id_numerico
        self.nome_produto = produto.nome
        self.preco = produto.preco
        self.quantidade = quantidade

        self.data = data

        self.desconto = desconto

    def calcular(self):
        return self.preco * self.quantidade * self.desconto


if __name__ == '__main__':
    main()
