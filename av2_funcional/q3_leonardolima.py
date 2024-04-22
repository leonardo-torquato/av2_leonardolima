import mysql.connector

# conexão com o MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='senha'
)

crs = mydb.cursor()
exec_sql_cmd = lambda cmd, crs: crs.execute(cmd)

#banco de dados
criar_banco = lambda nome_banco, crs: exec_sql_cmd(f"CREATE DATABASE IF NOT EXISTS {nome_banco};", crs)
excluir_banco = lambda nome_banco, crs: exec_sql_cmd(f"DROP DATABASE {nome_banco};", crs)
utilizar_banco = lambda nome_banco, crs: exec_sql_cmd(f"USE {nome_banco};", crs)

#tabelas
criar_tabela = lambda nome_tabela, atributos, crs: exec_sql_cmd(f"CREATE TABLE IF NOT EXISTS {nome_tabela} ({atributos});", crs)
excluir_tabela = lambda nome_tabela, crs: exec_sql_cmd(f"DROP TABLE {nome_tabela};", crs)

#dados
formatar_dados = lambda valores : ', '.join(f"'{val}'" if isinstance(val, str) else str(val) for val in valores)
inserir_dados_tabela = lambda nome_tabela, atributos, valores, crs: exec_sql_cmd(f"INSERT INTO {nome_tabela} ({atributos}) VALUES ({formatar_dados(valores)});", crs)
excluir_dados_tabela = lambda nome_tabela, condicao, crs: exec_sql_cmd(f"DELETE FROM {nome_tabela} WHERE {condicao};", crs)
selecionar_dados_condicao = lambda atributos, nome_tabela, condicao, crs: exec_sql_cmd(f"SELECT {atributos} FROM {nome_tabela} WHERE {condicao};", crs)

# Execução de operações
criar_banco('av2_leonardolima', crs)
utilizar_banco("av2_leonardolima", crs)

# tabelas pedidas na questão
criar_tabela("USERS", 'id INT, name VARCHAR(255), country VARCHAR(255), id_console INT', crs)
criar_tabela("VIDEOGAMES", 'id_console INT, name VARCHAR(255), id_company INT, release_date VARCHAR(255)', crs)
criar_tabela("GAMES", "id_game INT, title VARCHAR(255), genre VARCHAR(255), release_date VARCHAR(255), id_console VARCHAR(255)", crs)
criar_tabela("COMPANY", "id_company INT, name VARCHAR(255), country VARCHAR(75)", crs)

inserir_dados_tabela("USERS", 'id, name, country, id_console', (1, 'João Silva', 'Brasil', 5), crs)
inserir_dados_tabela("USERS", 'id, name, country, id_console', (2, 'leonardo lima', 'Brasil', 6), crs)
inserir_dados_tabela("USERS", 'id, name, country, id_console', (3, 'joana alemida', 'Brasil', 7), crs)
inserir_dados_tabela("COMPANY", 'id_company, name, country', (2, 'Amazon', 'eua'), crs)
inserir_dados_tabela("GAMES", 'id_game, title, genre, release_date, id_console', (24827, 'fallout 2', 'RPG', "10-10-1999", "PC"), crs)


mydb.commit()