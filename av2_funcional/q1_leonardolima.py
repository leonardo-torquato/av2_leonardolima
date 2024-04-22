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
