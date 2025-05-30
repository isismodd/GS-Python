from datetime import datetime

# variaveis
REGIOES = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
ongs_parceiras = []
resgates = []
doacoes = []


def mostrar_ajuda():
    print("\nCOMANDOS HoppeMapper DISPONÍVEIS:")
    print("  ong       - Gerenciar ONGs parceiras")
    print("  doar      - Fazer uma doação (você escolherá a região)")
    print("  relatorio - Ver doações por região/ONG")
    print("  resgate   - registra um chamado de resgate")
    print("  sair      - Encerrar o app")

def input_numero(mensagem):
    #Pede um número pro usuário e valida
    while True:
        entrada = input(mensagem).strip()
        if entrada.isdigit():
            return int(entrada)
        print("Erro: Digite apenas números!")
        

def input_decimal(mensagem):
    #Pede um valor decimal e valida 
    while True:
        entrada = input(mensagem).strip()
        valido = True
        ponto_ja_visto = False
        
        for caractere in entrada:
            # Verifica se é um dígito ou ponto decimal
            if not (caractere in '0123456789' or 
                   (caractere == '.' and not ponto_ja_visto)):
                valido = False
                break
            if caractere == '.':
                ponto_ja_visto = True
                
        if valido and entrada:  # Não pode ser string vazia
            return float(entrada)
        print("Erro: Digite um valor numérico válido (ex: 50 ou 100.50)!")
        
        
# --- GERENCIAMENTO DE ONGs ---
def gerenciar_ongs():
    print("\n📋 GERENCIAR ONGs PARCEIRAS")
    print("Subcomandos: 'cadastrar', 'listar', 'vincular', 'voltar'")
    
    while True:
        subcomando = input("\n(ongs) > ").strip().lower()
        
        if subcomando == "voltar":
            break
        
        elif subcomando == "cadastrar":
            nome = input("Nome da ONG: ").strip()
            if not nome:
                print("Erro: Nome não pode ser vazio!")
                continue
            
            ong = {
                "id": len(ongs_parceiras) + 1,
                "nome": nome,
                "regioes": [],
                "data_cadastro": datetime.now().strftime("%d/%m/%Y")
            }
            ongs_parceiras.append(ong)
            print(f"✅ ONG '{nome}' cadastrada (ID: {ong['id']})!")
        
        elif subcomando == "listar":
            if not ongs_parceiras:
                print("Nenhuma ONG cadastrada.")
                continue
            
            for ong in ongs_parceiras:
                regioes = ", ".join(ong["regioes"]) if ong["regioes"] else "Nenhuma"
                print(f"\nID {ong['id']}: {ong['nome']}")
                print(f"  Regiões atendidas: {regioes}")
        
        elif subcomando == "vincular":
            if not ongs_parceiras:
                print("Cadastre uma ONG primeiro!")
                continue
            
            print("\nONGs disponíveis:")
            for ong in ongs_parceiras:
                print(f"ID {ong['id']}: {ong['nome']}")
            
            id_ong = input_numero("\nID da ONG para vincular região: ")
            ong = next((o for o in ongs_parceiras if o["id"] == id_ong), None)
            if not ong:
                print("ID inválido!")
                continue
            
            print("\nRegiões disponíveis:")
            for i, regiao in enumerate(REGIOES, 1):
                print(f"{i}. {regiao}")
            
            regiao_num = input_numero("\nNúmero da região: ") - 1
            if 0 <= regiao_num < len(REGIOES):
                regiao = REGIOES[regiao_num]
                if regiao not in ong["regioes"]:
                    ong["regioes"].append(regiao)
                    print(f"✅ Região '{regiao}' vinculada a {ong['nome']}!")
                else:
                    print("Esta ONG já atua nessa região.")
            else:
                print("Número inválido!")
        
        else:
            print("Subcomando inválido. Tente novamente.")

# --- GERENCIAR CHAMADOS DE RESGATE ---
def chamados_resgate():
    print("\n📋 chamados de resgate")
    print("Subcomandos: 'cadastrar', 'listar chamados', 'voltar'")
    
    while True:
        subcomando = input("\n(resgate) > ").strip().lower()
        
        if subcomando == "voltar":
            break
        
        elif subcomando == "cadastrar":
            tipo = input("Tipo de resgate(Pessoa, animal doméstico ou animal exótico): ").strip()
            if not tipo:
                print("Erro: Tipo não pode ser vazio!")
                continue
            
            resgate = {
                "id": len(resgates) + 1,
                "tipo": tipo,
                "regioes": [],
                "data_cadastro": datetime.now().strftime("%d/%m/%Y")
            }
            resgates.append(resgate)
            print(f"✅ Chamado de resgate '{tipo}' aberto (ID: {resgate['id']})!")
        
        elif subcomando == "listar":
            if not resgates:
                print("Nenhum chamado aberto.")
                continue
            
            for resgate in resgates:
                regioes = ", ".join(resgate["regioes"]) if resgate["regioes"] else "Nenhuma"
                print(f"\nID {resgate['id']}: {resgate['tipo']}")
                print(f"  Regiões vinculadas: {regioes}")
        

# --- DOAÇÕES POR REGIÃO ---
def registrar_doacao():
    if not ongs_parceiras:
        print("\nErro: Nenhuma ONG cadastrada. Use o comando 'ong' primeiro.")
        return
    
    print("\n📍 DOAÇÃO POR REGIÃO")
    print("Escolha uma região para listar ONGs disponíveis:")
    
    for i, regiao in enumerate(REGIOES, 1):
        print(f"{i}. {regiao}")
    
    regiao_num = input_numero("\nNúmero da região: ") - 1
    if not (0 <= regiao_num < len(REGIOES)):
        print("Número inválido!")
        return
    
    regiao = REGIOES[regiao_num]
    ongs_na_regiao = [o for o in ongs_parceiras if regiao in o["regioes"]]
    
    if not ongs_na_regiao:
        print(f"Nenhuma ONG atende a região {regiao} ainda.")
        return
    
    print(f"\nONGs em {regiao}:")
    for ong in ongs_na_regiao:
        print(f"ID {ong['id']}: {ong['nome']}")
    
    id_ong = input_numero("\nID da ONG que receberá a doação: ")
    ong = next((o for o in ongs_na_regiao if o["id"] == id_ong), None)
    if not ong:
        print("ID inválido!")
        return
    
    valor = input_decimal("Valor da doação (R$): ")
    doacao = {
        "ong_id": id_ong,
        "ong_nome": ong["nome"],
        "regiao": regiao,
        "valor": valor,
        "data": datetime.now().strftime("%d/%m/%Y")
    }
    doacoes.append(doacao)
    print(f"\n✅ Doação de R$ {valor:.2f} registrada para {ong['nome']} ({regiao})!")

# --- RELATÓRIOS ---
def mostrar_relatorio():
    if not doacoes:
        print("\nNenhuma doação registrada ainda.")
        return
    
    print("\n📊 RELATÓRIO DE DOAÇÕES")
    print("\nPor região:")
    for regiao in REGIOES:
        total = sum(d["valor"] for d in doacoes if d["regiao"] == regiao)
        print(f"  {regiao}: R$ {total:.2f}")
    
    print("\nPor ONG:")
    for ong in ongs_parceiras:
        total = sum(d["valor"] for d in doacoes if d["ong_id"] == ong["id"])
        if total > 0:
            print(f"  {ong['nome']}: R$ {total:.2f}")

# --- LOOP PRINCIPAL ---
print("\n🌈 HOPEMAPPER - CONECTANDO DOADORES A COMUNIDADES 🌎")
print("Digite 'ajuda' para ver comandos.\n")

rodando = True
while rodando:
    comando = input("> ").strip().lower()
    
    if comando == "sair":
        print("\nObrigado por usar o HopeMapper! Juntos fazemos a diferença! 🌍\n")
        rodando = False  # Substitui o sys.exit()
    elif comando == "ong":
        gerenciar_ongs()
    elif comando == "doar":
        registrar_doacao()
    elif comando == "relatorio":
        mostrar_relatorio()
    elif comando == "ajuda":
        mostrar_ajuda()
    else:
        print(f"\nComando inválido: '{comando}'. Digite 'ajuda' para ver opções.")
