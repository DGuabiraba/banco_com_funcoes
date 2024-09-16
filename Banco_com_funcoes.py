#TODO
#implementar menu de criaçãode usuario antes das operações bancarias para uma melhor organização do programa 
#pq o programa faz operações saque, deposito e extrato sem salvar na conta do usuario 
#@footer DGuabiraba

import textwrap
import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def moeda_local(valor):
    return locale.currency(valor, grouping=True, symbol=True)

def data_e_hora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def menu():
    menu = """
   ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [7]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, extrato):
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        saldo += valor
        extrato.append(f"{data_e_hora()} - Depósito: {moeda_local(valor)}")
        print(f"\n=== Depósito de {moeda_local(valor)} realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato

def sacar(saldo, extrato, limite, numero_saques, limite_saques):
    valor = float(input("Informe o valor do saque: "))
    if valor > saldo:
        print("\n@@@ Saldo insuficiente. @@@")
    elif valor > limite:
        print("\n@@@ O valor do saque excede o limite. @@@")
    elif numero_saques >= limite_saques:
        print("\n@@@ Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato.append(f"{data_e_hora()} - Saque: {moeda_local(valor)}")
        numero_saques += 1
        print(f"\n=== Saque de {moeda_local(valor)} realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato, numero_saques 

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for linha in extrato:
            print(linha)
        print(f"\nSaldo:\t\t{moeda_local(saldo)}")
        print("==========================================")
        
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)
        
    if usuario:
            print("\n@@@ Já existe usuário com esse CPF! @@@")
    else:
            nome = input("Infome o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
            usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
            print("=== Usuário criado com sucesso! ===")
            
def filtrar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario['cpf'] == cpf), None)
            
def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        contas.append({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario})
        print("\n=== Conta criada com sucesso! ===")
    else:
        print("\n@@@ Usuário não encontrado! @@@")
            
def listar_contas(contas):
        for conta in contas:
            print("=" * 50)
            print(f"Agência: {conta['agencia']}\nConta: {conta['numero_conta']}\nTitular: {conta['usuario']['nome']}")
            print("=" * 50)
    
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        match opcao:
            case "1":
                saldo, extrato = depositar(saldo, extrato)
            case "2":
                saldo, extrato, numero_saques = sacar(saldo, extrato, limite, numero_saques, LIMITE_SAQUES)
            case "3":
                exibir_extrato(saldo, extrato)
            case "4":
                numero_conta = len(contas) + 1
                criar_conta(AGENCIA, numero_conta, usuarios, contas)
            case "5":
                listar_contas(contas)
            case "6":
                criar_usuario(usuarios)
            case "7":
                print("Saindo...")
                break
            case _:
                print("Operação inválida, por favor selecione novamente a operação desejada.")

main()

