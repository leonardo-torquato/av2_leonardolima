import q3_leonardolima

def gerar_select(atributos, tabelas):
    return (lambda atribs, tabelas: f"SELECT {', '.join(atribs)} FROM {tabelas}")(atributos, tabelas)

def gerar_inner_join(tabela1, tabela2, condicao):
    return (lambda t1, t2, cond: f"INNER JOIN {t2} ON {cond}")(tabela1, tabela2, condicao)

# Condição para o INNER JOIN
condicao_join = "GAMES.id_game = VIDEOGAMES.id_game AND VIDEOGAMES.id_company = COMPANY.id_company"

# Atributos para o SELECT
atributos_select = ["GAMES.title", "COMPANY.name"]

# Tabelas envolvidas na consulta
tabelas = "GAMES INNER JOIN VIDEOGAMES ON GAMES.id_game = VIDEOGAMES.id_game INNER JOIN COMPANY ON VIDEOGAMES.id_company = COMPANY.id_company"

# Gerando a consulta SQL
consulta_sql = gerar_select(atributos_select, tabelas)

# Executando a consulta
exec_sql_cmd = lambda cmd, crs: crs.execute(cmd)
exec_sql_cmd(consulta_sql, q3_leonardolima.crs)

# Imprimindo os resultados
for row in q3_leonardolima.crs:
    print(row)
