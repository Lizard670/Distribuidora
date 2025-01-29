# -*- coding: cp1252 -*-
from tkinter import *
from tkinter import font as tkfont


class InterfaceLoja(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Muda o título da janela
        self.title("Distribuidora")

        # Cria um objeto fonte que pode ser reutilizado para todos os titulos
        self.fonte_titulo = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # Container que guarda os frames das outras páginas
        # Quando precisar abrir uma página use o método abrir_pagina
        container = Frame(self)
        # Configura o container pra preencher a tela toda e ser composto de uma linha e uma coluna
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Inicialização das páginas, todas precisam ocupar o mesmo espaço para que fiquem empilhadas
        self.paginas = {}
        self.paginas["telaInicial"] = TelaInicial(parent=container, controller=self)
        self.paginas["telaInicial"].grid(row=0, column=0, sticky="nsew")

        self.paginas["estoque"] = Estoque(parent=container, controller=self)
        self.paginas["estoque"].grid(row=0, column=0, sticky="nsew")

        self.paginas["vendas"] = Vendas(parent=container, controller=self)
        self.paginas["vendas"].grid(row=0, column=0, sticky="nsew")

        self.paginas["estatisticas"] = Estatisticas(parent=container, controller=self)
        self.paginas["estatisticas"].grid(row=0, column=0, sticky="nsew")

        self.abrir_pagina("telaInicial")

    # Abre a página passada
    def abrir_pagina(self, page_name):
        pagina = self.paginas[page_name]
        # Dando um raise na página, ela vai ficar sobre todas as outras e apenas o conteúdo dela vai aparecer na tela
        pagina.tkraise()


class TelaInicial(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Bem vindo ao programa de \ngerenciamento da distribuidora",
                      font=controller.fonte_titulo, pady=10, padx=10)
        label.pack(side="top", fill="x", pady=10)

        self.frameBotoes = Frame(self)
        self.frameBotoes.pack()

        botaoEstoque = Button(self.frameBotoes, text="Abrir página \ndo estoque",
                         command=lambda: controller.abrir_pagina("estoque"))
        botaoVendas = Button(self.frameBotoes, text="Abrir página \nde vendas",
                         command=lambda: controller.abrir_pagina("vendas"))
        botaoEstatisticas = Button(self.frameBotoes, text="Abrir página \nde estatisticas",
                         command=lambda: controller.abrir_pagina("estatisticas"))

        botaoEstoque.pack(side="left", padx=5)
        botaoVendas.pack(side="left", padx=5)
        botaoEstatisticas.pack(side="left", padx=5)


class Estoque(Frame):
    # todo
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is page 1", font=controller.fonte_titulo)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                        command=lambda: controller.abrir_pagina("telaInicial"))
        button.pack()


class Vendas(Frame):
    # todo
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is page 2", font=controller.fonte_titulo)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                        command=lambda: controller.abrir_pagina("telaInicial"))
        button.pack()


class Estatisticas(Frame):
    # todo
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is page 3", font=controller.fonte_titulo)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                        command=lambda: controller.abrir_pagina("telaInicial"))
        button.pack()




class Estabelecimento:
    def __init__(self):
        self.estoque = []
        self.vendas = []
        # Proximo id que vai ser entregado quando criar um novo produto
        self.proximo_id = 0

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
                pass
                # todo


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


if __name__ == "__main__":
    # Cria a interface e roda o loop principal dela
    interface = InterfaceLoja()
    interface.mainloop()