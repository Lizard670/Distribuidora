# -*- coding: cp1252 -*-
import tkinter as tk
from tkinter import font as tkfont
from tkinter.ttk import *


class InterfaceLoja(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

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
                        "TelaRemoverProduto": TelaRemoverProduto(parent=container, controller=self),
                        "Vendas": Vendas(parent=container, controller=self),
                        "Estatisticas": Estatisticas(parent=container, controller=self)}
        # Todas as páginas precisam ocupar o mesmo espaço para que fiquem empilhadas
        for nome, pagina in self.paginas.items():
            pagina.grid(row=0, column=0, sticky="nsew")

        self.abrir_pagina("TelaInicial")

    # Abre a página passada
    def abrir_pagina(self, nome_pagina):
        pagina = self.paginas[nome_pagina]
        # Quando ocorrer um erro no atualizar, ele retorna verdadeiro
        if not pagina.atualizar():
            # Dando um raise na página, ela vai ficar sobre todas as
            # outras e apenas o  conteúdo dela vai aparecer na tela
            pagina.tkraise()

    def novo_produto(self, produto):
        if produto["id"] == -1:
            produto["id"] = self.proximo_id
            self.proximo_id += 1  # Atualiza o proximo id
        self.estoque.append(produto)


class TelaInicial(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Texto que fica na parte de cima da tela
        label = Label(self, text="Bem vindo ao programa de \ngerenciamento da distribuidora",
                      font=controller.fonte_titulo)
        label.pack(side="top", fill="x", pady=10)

        # Botões que levam para outras páginas
        self.frameBotoes = Frame(self)
        self.frameBotoes.pack()

        botaoEstoque = Button(self.frameBotoes, text="Abrir página \ndo estoque",
                              command=lambda: controller.abrir_pagina("Estoque"),
                              )
        botaoVendas = Button(self.frameBotoes, text="Abrir página \nde vendas",
                             command=lambda: controller.abrir_pagina("Vendas"),
                             )
        botaoEstatisticas = Button(self.frameBotoes, text="Abrir página \nde estatisticas",
                                   command=lambda: controller.abrir_pagina("Estatisticas"),
                                   )

        botaoEstoque.pack(side="left", padx=5)
        botaoVendas.pack(side="left", padx=5)
        botaoEstatisticas.pack(side="left", padx=5)

    def atualizar(self):
        pass


class Estoque(Frame):
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
                          width=12)
        botaoAdicionar = Button(self.frameBotoes, text="Novo produto",
                                command=lambda: controller.abrir_pagina("TelaAdicionarProduto"),
                                width=12)
        botaoRemover = Button(self.frameBotoes, text="Remover produto",
                              command=lambda: controller.abrir_pagina("TelaRemoverProduto"),
                              width=12)
        botaoVoltar = Button(self.frameBotoes, text="Voltar",
                             command=lambda: controller.abrir_pagina("TelaInicial"),
                             width=12)

        botaoVer.pack(side="left", padx=5)
        botaoAdicionar.pack(side="left", padx=5)
        botaoRemover.pack(side="left", padx=5)
        botaoVoltar.pack(side="left", padx=5)

    def atualizar(self):
        pass


class TelaVerEstoque(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.atributos = ("id", "nome", "preço", "quantidade")
        self.tamanhos = (5, 20, 8, 12)

        # Botões
        self.frameBotoes = Frame(self)
        self.frameBotoes.pack()

        self.botaoSalvar = Button(self.frameBotoes, text="Salvar",
                                  command=self.salvar,
                                  width=12)
        self.botaoVoltar = Button(self.frameBotoes, text="Voltar",
                                  command=self.voltar,
                                  width=12)

        self.botaoSalvar.pack(side="left", padx=5, pady=10)
        self.botaoVoltar.pack(side="left", padx=5, pady=10)

        # Legendas
        self.frameLegendas = Frame(self)
        self.frameLegendas.pack()
        self.legendas = []
        for i in range(len(self.atributos)):
            label = Label(self.frameLegendas, text=self.atributos[i].upper(), width=self.tamanhos[i],
                          font=controller.fonte_tabela)
            self.legendas.append(label)
            label.pack(side="left")

        # Tabela
        self.tabela = Frame(self)

    def salvar(self):
        # A forma que isso funciona atualmente é apagando a lista inteira de produtos e
        # salvando tudo de novo, isso é tem uma escalabilidade ruim, porém a outra forma
        # que pensei de fazer isso, precisaria de outra tela só para editar um valor
        # individualmente, isso iria tomar mais tempo e exigir alguns pedaços de
        # conhecimento que atualmente não tenho.

        # Limpa a lista de produtos para poder salvar tudo de novo
        self.controller.estoque = []

        contAtributo = 0
        totalAtributos = len(self.atributos)
        produtoAtual = {}
        # Passa por cada um dos atributos de cada um dos produtos
        for widget in self.tabela.winfo_children():
            # Pega o id do atributo atual
            idAtributo = contAtributo % totalAtributos
            # Salva o atributo atual
            # TODO checar se o usuário colocou o tipo correto de valor
            produtoAtual[self.atributos[idAtributo]] = widget.get()

            contAtributo += 1
            # Quando o próximo atributo é o primeiro, salva o produto e reseta
            if contAtributo % totalAtributos == 0:
                self.controller.novo_produto(produtoAtual)
                produtoAtual = {}

    def voltar(self):
        # TODO perguntar se você quer voltar sem salvar
        self.controller.abrir_pagina("Estoque")

    def atualizar(self):
        # Limpa o que tiver dentro da tabela antes de adicionar novamente
        for widget in self.tabela.winfo_children():
            widget.destroy()

        contLinha = 0
        for produto in self.controller.estoque:
            contColuna = 0
            for atributo in self.atributos:
                e = Entry(self.tabela, width=self.tamanhos[contColuna],
                          font=self.controller.fonte_tabela)
                e.grid(row=contLinha, column=contColuna)
                e.insert(tk.END, produto[atributo])
                contColuna += 1

            contLinha += 1
        self.tabela.pack()


class TelaAdicionarProduto(Frame):
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

    def atualizar(self):
        self.entryNome.insert(0, "")
        self.entryPreco.insert(0, "0")
        self.entryQuantidade.insert(0, "0")

    def novo_produto(self):
        try:
            nome = self.entryNome.get()
            # Checa se possui um nome válido
            if not nome or not nome.strip():
                raise ValueError

            preco = int(self.entryPreco.get())
            quantidade = int(self.entryQuantidade.get())
        except ValueError:
            # TODO popup de erro
            print("Não foi possível adicionar o novo produto: valor invalido")
            return
        else:
            self.controller.novo_produto(criar_produto(nome, preco, quantidade=quantidade))
            self.controller.abrir_pagina("Estoque")


class TelaRemoverProduto(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.produtos = []
        label = Label(self, text="Selecione o produto \nque deseja remover",
                      font=controller.fonte_titulo, justify="center")
        label.pack(side="top", fill="x", pady=10)

        # Combobox com os produtos
        self.comboBox = Combobox(self, postcommand=self.atualizar_combobox, state="readonly")
        self.comboBox.pack()

        # Campo para o usuário confirmar o item que está sendo deletado
        self.frameNome = Frame(self)
        self.labelNome = Label(self.frameNome, text="Insira o nome para confirmar \no item que vai ser apagado: ")
        self.entryNome = Entry(self.frameNome, width=28)
        self.frameNome.pack(padx=5, pady=5)
        self.labelNome.pack(side="left")
        self.entryNome.pack(side="left")

        # Botões
        self.frameBotoes = Frame(self)
        self.frameBotoes.pack()

        botaoRemover = Button(self.frameBotoes, text="Remover",
                              command=self.apagar_produto)
        botaoCancelar = Button(self.frameBotoes, text="Cancelar",
                               command=lambda: controller.abrir_pagina("Estoque"))

        botaoRemover.pack(side="left")
        botaoCancelar.pack(side="left", padx=(15, 0))

    def apagar_produto(self):
        # Se não tiver nada selecionado, nem tenta apagar
        if not self.comboBox.get():
            return
        # Separa do bruto o id e o nome
        id_produto, nome = self.comboBox.get().split(":", 2)
        id_produto = int(id_produto)
        nome = nome.strip()

        if nome == self.entryNome.get().strip():
            self.controller.estoque.pop(id_produto)
            self.controller.abrir_pagina("Estoque")

    def atualizar(self):
        # Gera a lista dos produtos
        self.produtos = []
        for produto in self.controller.estoque:
            self.produtos.append(str(produto["id"]) + ":" + produto["nome"])

        if not self.produtos:
            # TODO popup de erro caso tente entrar na tela e não tenha produtos registrados
            return True

    def atualizar_combobox(self):
        self.comboBox['values'] = self.produtos

class Vendas(Frame):
    # TODO
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is page 2", font=controller.fonte_titulo)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                        command=lambda: controller.abrir_pagina("telaInicial"))
        button.pack()


class Estatisticas(Frame):
    # TODO
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


def criar_venda(produto, quantidade, data, desconto=1):
    return {"id_produto": produto["id"],
            "nome_produto": produto["nome"],
            "preço": produto["preço"],
            "quantidade": quantidade,
            "data": data,
            "desconto": desconto}


if __name__ == "__main__":
    # Cria a interface e roda o loop principal dela
    interface = InterfaceLoja()
    interface.mainloop()
