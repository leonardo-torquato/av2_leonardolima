import threading
import random

# Dicionário de usuários
users = {}

# Dicionário de contas correntes
current_accounts = {}

# Função para criar usuário e conta corrente
create_user_and_account = lambda user_name, account_number, initial_balance, credit_limit: (
    users.update({len(users) + 1: {"name": user_name, "account_number": account_number}}),
    current_accounts.update({account_number: {"balance": initial_balance, "credit_limit": credit_limit}})
)

# Função para sacar dinheiro (CASH)
withdraw_cash = lambda value, account_number, user_name: (
    (current_accounts[account_number]["balance"] >= value and (
        receive_cash(value, account_number), 
        print_payment_receipt(value, account_number, user_name), 
        complete_transaction())) 
    or cancel_transaction("Fundos Insuficientes para saque")
)

# função para transferencia de fundos (FUND TRANSFER)
fund_transfer = lambda value, from_account, to_account: ( 
    provide_bank_deposit_details(value, from_account, to_account),

    (current_accounts[from_account]["balance"] >= value and ( 
        confirm_payment_approval_from_bank(value, from_account, to_account), 
        complete_transaction(),)) 
    
    or cancel_transaction("fundos insuficientes para transferencia")
)

#funcao para compra no credito (CREDIT)
credit_purchase = lambda value, account_number, user_name: (
    request_credit_account_details(value, account_number, user_name),
    
    (current_accounts[account_number]["credit_limit"] >= value and (
        request_payment_from_bank(value, account_number, user_name),
        complete_transaction()
    )) 
    
    or cancel_transaction("limite de credito insuficiente")
)

# Função para receber dinheiro (RECEIVE CASH)
receive_cash = lambda value, account_number: (
    current_accounts.update({account_number: {"balance": current_accounts[account_number]["balance"] - value, "credit_limit" :  current_accounts[account_number]["credit_limit"]}}),
    print("Saque efetuado!")
)

# Função para imprimir recibo de pagamento (PRINT PAYMENT RECEIPT)
print_payment_receipt = lambda value, account_number, user_name : (
    print(return_payment_receipt(value, account_number, user_name))
)

# Função para retornar recibo de pagamento (RETURN PAYMENT RECEIPT)
return_payment_receipt = lambda value, account_number, user_name: (
    f"O usuário {user_name} sacou R${value} da conta N°{account_number}."
)

# Função para fornecer detalhes do depósito bancário (PROVIDE BANK DEPOSIT DETAILS)
provide_bank_deposit_details = lambda value, from_account, to_account: (
    print(f"transferencia solicitada de R${value} da conta n°{from_account} para a conta n° {to_account}.")
)

# Função para confirmar a aprovação do pagamento pelo banco (CONFIRM PAYMENT APPROVAL FROM BANK)
confirm_payment_approval_from_bank = lambda value, from_account, to_account: (
        current_accounts.update({from_account: {"balance": current_accounts[from_account]["balance"], "credit_limit" :  current_accounts[from_account]["credit_limit"] - value}}),
        current_accounts.update({to_account: {"balance": current_accounts[to_account]["balance"], "credit_limit" :  current_accounts[to_account]["credit_limit"] + value}}),
        print(f"R${value} transferidos para a conta n°{to_account}!")
)

# Função para solicitar detalhes da conta de crédito (REQUEST CREDIT ACCOUNT DETAILS)
request_credit_account_details = lambda value, account_number, user_name: (
    print(f"Compra no credito solicitada no valor de R${value} por {user_name} da conta n°{account_number}.")
)

# Função para solicitar pagamento do banco (REQUEST PAYMENT FROM BANK)
request_payment_from_bank = lambda value, account_number, user_name: (
    current_accounts.update({account_number: {"balance": current_accounts[account_number]["balance"], "credit_limit" :  current_accounts[account_number]["credit_limit"] - value}}),
    print(f"Success: {user_name} made a credit purchase of {value} from account {account_number}.")
)

# Função para completar a transação (COMPLETE TRANSACTION)
complete_transaction = lambda : (print("Transação Completa! "), close_transaction())

# Função para cancelar a transação (CANCEL TRANSACTION)
cancel_transaction = lambda message: (print(f"Transação cancelada: {message}. "), close_transaction())

# Função para fechar transação (CLOSE TRANSACTION)
close_transaction = lambda : print("Operação Finalizada. \n")


# Teste criação de usuários e contas correntes
create_user_and_account("João", "333", 500, 2000)
create_user_and_account("Maria", "444", 1000, 3000)
create_user_and_account("Carlos", "555", 200, 1000)

# teste de saque
withdraw_cash(200, "333", "João")
withdraw_cash(50, "444", "Maria")
withdraw_cash(100, "555", "Carlos")

# teste de transferência de fundos
fund_transfer(300, "333", "444")
fund_transfer(150, "444", "555")
fund_transfer(50, "555", "333")

# teste de compra no crédito
credit_purchase(1000, "333", "João")
credit_purchase(500, "444", "Maria")
credit_purchase(250, "555", "Carlos")


print(users)
print(current_accounts)

# Funções auxiliares para gerar dados de teste
generate_user_data = lambda: (f"User{random.randint(1, 1000)}", f"Account{random.randint(1, 1000)}", random.randint(100, 10000), random.randint(100, 5000))
generate_transaction_data = lambda: (random.choice(['withdraw_cash', 'fund_transfer', 'credit_purchase']), random.randint(1, 1000), random.randint(100, 10000)) if random.choice(['withdraw_cash', 'fund_transfer', 'credit_purchase']) == 'withdraw_cash' else (random.choice(['withdraw_cash', 'fund_transfer', 'credit_purchase']), random.randint(1, 1000), random.randint(1, 1000), random.randint(100, 10000))

# Função para executar operações em um thread
perform_operation = lambda operation, *args: (
    create_user_and_account(*args) if operation == 'create_user_and_account' else
    withdraw_cash(*args) if operation == 'withdraw_cash' else
    fund_transfer(*args) if operation == 'fund_transfer' else
    credit_purchase(*args)
)

# Função para iniciar o teste de stress
start_stress_test = lambda num_threads, num_operations: [
    threading.Thread(target=perform_operation, args=(operation, *args)).start() for _ in range(num_threads) for _ in range(num_operations) for operation, *args in [generate_transaction_data()]
]

# teste de stress
num_threads = 10 # Número de threads para simular operações simultâneas
num_operations = 1000 # Número de operações por thread
start_stress_test(num_threads, num_operations)
