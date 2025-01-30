# -*- coding: cp1252 -*-
from tkinter import *
from tkinter import font as tkfont


class InterfaceLoja(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Muda o título da janela
        self.title("Distribuidora")

        # Cria os objetos fonte que podem ser reutilizados
        self.fonte_titulo = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.fonte_botao = tkfont.Font(family='Helvetica', size=11)
        self.fonte_tabela = tkfont.Font(family='Helvetica', size=12, weight="bold")

        # Listas do estoque e das vendas
        self.estoque = []
        self.vendas = []
        # Proximo id que vai ser entregado quando criar um novo produto
        self.proximo_id = 0
        self.novo_produto(criar_produto("Teste", 15))

        # Container que guarda os frames das outras páginas
        # Quando precisar abrir uma página use o método abrir_pagina
        container = Frame(self)
        # Configura o container pra preencher a tela toda e ser composto de uma linha e uma coluna
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Inicialização das páginas
        self.paginas = {"TelaInicial": TelaInicial(parent=container, controller=self),
                        "Estoque": Estoque(parent=container, controller=self),
                        "TelaVerEstoque": TelaVerEstoque(parent=container, controller=self),
                        "TelaAdicionarProduto": TelaAdicionarProduto(parent=container, controller=self),
                        "Vendas": Vendas(parent=container, controller=self),
                        "Estatisticas": Estatisticas(parent=container, controller=self)}
        # Todas as páginas precisam ocupar o mesmo espaço para que fiquem empilhadas
        for nome, pagina in self.paginas.items():
            pagina.grid(row=0, column=0, sticky="nsew")

        self.abrir_pagina("TelaInicial")

    # Abre a página passada
    def abrir_pagina(self, page_name):
        pagina = self.paginas[page_name]
        # Dando um raise na página, ela vai ficar sobre todas as outras e apenas o conteúdo dela vai aparecer na tela
        pagina.tkraise()

    def novo_produto(self, produto):
        produto["id"] = self.proximo_id
        self.estoque.append(produto)
        self.proximo_id += 1  # Atualiza o proximo id


class TelaInicial(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, pady=5)
        self.controller = controller

        # Texto que fica na parte de cima da tela
        label = Label(self, text="Bem vindo ao programa de \ngerenciamento da distribuidora",
                      font=controller.fonte_titulo, pady=10, padx=10)
        label.pack(side="top", fill="x", pady=10)

        # Botões que levam para outras páginas
        self.frameBotoes = Frame(self)
        self.frameBotoes.pack()

        botaoEstoque = Button(self.frameBotoes, text="Abrir página \ndo estoque",
                              command=lambda: controller.abrir_pagina("Estoque"),
                              font=controller.fonte_botao)
        botaoVendas = Button(self.frameBotoes, text="Abrir página \nde vendas",
                             command=lambda: controller.abrir_pagina("Vendas"),
                             font=controller.fonte_botao)
        botaoEstatisticas = Button(self.frameBotoes, text="Abrir página \nde estatisticas",
                                   command=lambda: controller.abrir_pagina("Estatisticas"),
                                   font=controller.fonte_botao)

        botaoEstoque.pack(side="left", padx=5)
        botaoVendas.pack(side="left", padx=5)
        botaoEstatisticas.pack(side="left", padx=5)


class Estoque(Frame):
    # todo
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Texto do topo da tela
        label = Label(self, text="Estoque", font=controller.fonte_titulo)
        label.pack(side="top", fill="x", pady=30)

        # Botões
        self.frameBotoes = Frame(self)
        self.frameBotoes.pack()

        botaoVer = Button(self.frameBotoes, text="Ver e editar",
                          command=lambda: controller.abrir_pagina("TelaVerEstoque"),
                          width=12, height=2, font=controller.fonte_botao)
        botaoAdicionar = Button(self.frameBotoes, text="Novo produto",
                                command=lambda: controller.abrir_pagina("TelaAdicionarProduto"),
                                width=12, height=2, font=controller.fonte_botao)
        botaoVoltar = Button(self.frameBotoes, text="Voltar",
                             command=lambda: controller.abrir_pagina("TelaInicial"),
                             width=12, height=2, font=controller.fonte_botao)

        botaoVer.pack(side="left", padx=5)
        botaoAdicionar.pack(side="left", padx=5)
        botaoVoltar.pack(side="left", padx=5)


class TelaVerEstoque(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, padx=10, pady=10)
        self.controller = controller
        self.atributos = ("id", "nome", "preço", "quantidade")
        self.tamanhos = (5, 20, 8, 11)

        # Botões
        self.frameBotoes = Frame(self)
        self.frameBotoes.pack()

        self.botaoSalvar = Button(self.frameBotoes, text="Salvar",
                                  command=self.salvar,
                                  width=12, height=2, font=controller.fonte_botao)
        # TODO perguntar se você quer voltar sem salvar
        self.botaoVoltar = Button(self.frameBotoes, text="Voltar",
                                  command=lambda: controller.abrir_pagina("Estoque"),
                                  width=12, height=2, font=controller.fonte_botao)

        self.botaoSalvar.pack(side="left", padx=5, pady=10)
        self.botaoVoltar.pack(side="left", padx=5, pady=10)

        # Legendas
        self.frameLegendas = Frame(self)
        self.frameLegendas.pack()
        self.legendas = []
        for i in range(len(self.atributos)):
            label = Label(self.frameLegendas, text=self.atributos[i].upper(), width=self.tamanhos[i] - 1,
                          font=controller.fonte_tabela)
            self.legendas.append(label)
            label.pack(side="left")

        # Tabela
        contLinha = 0
        self.tabela = Frame(self)
        for produto in controller.estoque:
            contColuna = 0
            for atributo in self.atributos:
                self.e = Entry(self.tabela, width=self.tamanhos[contColuna],
                               font=controller.fonte_tabela)
                self.e.grid(row=contLinha, column=contColuna)
                self.e.insert(END, produto[atributo])
                contColuna += 1

            contLinha += 1
        self.tabela.pack()

    def salvar(self):
        pass


class TelaAdicionarProduto(Frame):
    # todo
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is page 2", font=controller.fonte_titulo)
        label.pack(side="top", fill="x", pady=10)

        # Campos para o usuário preencher
        self.frameNome = Frame(self)
        self.labelNome = Label(self.frameNome, text="Nome: ")
        self.entryNome = Entry(self.frameNome, width=28)
        self.frameNome.pack(padx=5, pady=5)
        self.labelNome.pack(side="left")
        self.entryNome.pack(side="left")

        self.framePrecoEQuantidade = Frame(self)
        self.labelPreco = Label(self.framePrecoEQuantidade, text="Preço: ")
        self.entryPreco = Entry(self.framePrecoEQuantidade, width=8)
        self.labelQuantidade = Label(self.framePrecoEQuantidade, text="Quantidade: ")
        self.entryQuantidade = Entry(self.framePrecoEQuantidade, width=4)
        self.entryQuantidade.insert(0, "0")
        self.framePrecoEQuantidade.pack(padx=5, pady=5)
        self.labelPreco.pack(side="left")
        self.entryPreco.pack(side="left")
        self.labelQuantidade.pack(side="left", padx=(10, 0))
        self.entryQuantidade.pack(side="left")

        # Botões
        self.frameBotoes = Frame(self)
        self.frameBotoes.pack()

        botaoAdicionar = Button(self.frameBotoes, text="Adicionar",
                                command=self.novo_produto)
        botaoCancelar = Button(self.frameBotoes, text="Cancelar",
                               command=lambda: controller.abrir_pagina("Estoque"))

        botaoAdicionar.pack(side="left")
        botaoCancelar.pack(side="left", padx=(15, 0))

    def novo_produto(self):
        try:
            nome = self.entryNome.get()
            # Checa se possui um nome válido
            if not nome or not nome.strip():
                raise ValueError

            preco = int(self.entryPreco.get())
            quantidade = int(self.entryPreco.get())
        except ValueError:
            # todo popup de erro
            print("Não foi possível adicionar o novo produto: valor invalido")
            return
        else:
            self.controller.novo_produto(criar_produto(nome, preco, quantidade=quantidade))
            self.controller.abrir_pagina("Estoque")


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


def criar_produto(nome, preco, id_produto=-1, quantidade=0):
    return {"nome": nome, "preço": preco, "id": id_produto, "quantidade": quantidade}


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
