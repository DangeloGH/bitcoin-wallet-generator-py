import os
import getpass
import qrcode
from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip84, Bip84Coins, Bip44Changes

# --- CONFIGURAÇÃO ---
IDIOMA_SEED = "english"
PASTA_QR = "QR_CODES"
NUM_ENDERECOS_PADRAO = 10
NUM_ENDERECOS_ISCA = 1
DIVISORIA_SECAO = "-" * 65

# --- FUNÇÃO PRINCIPAL PARA DERIVAR E MOSTRAR UMA CARTEIRA ---
def derivar_e_mostrar_carteira(frase_seed, passphrase, titulo_carteira, num_enderecos, qr_prefixo):
    """
    Função unificada que deriva e exibe todos os detalhes de uma carteira.
    """
    print(f"\n\n{'#' * 65}")
    print(f"           {titulo_carteira}")
    print(f"{'#' * 65}")

    try:
        if not Mnemonic(IDIOMA_SEED).check(frase_seed):
            raise ValueError("A seed phrase é inválida (palavra incorreta ou checksum falhou).")
        
        semente_binaria = Bip39SeedGenerator(frase_seed).Generate(passphrase)
        
        bip84_mst_ctx = Bip84.FromSeed(semente_binaria, Bip84Coins.BITCOIN)
        bip84_acc_ctx = bip84_mst_ctx.Purpose().Coin().Account(0)
        xpub = bip84_acc_ctx.PublicKey().ToExtended()

        print("\n--- Chave de Visualização (Account xpub) ---")
        print(f"CAMINHO: m/84'/0'/0'")
        print(f"XPUB: {xpub}")
        print(DIVISORIA_SECAO)

        print(f"\n--- Endereços de Recebimento ---")
        print(f"Os QR Codes de cada endereço serão salvos na pasta '{PASTA_QR}'.")
        if not os.path.exists(PASTA_QR):
            os.makedirs(PASTA_QR)
        
        cabecalho = f" {'Índice':<6} | {'Caminho de Derivação':<22} | {'Endereço Bitcoin (bc1...)':<45} | {'Chave Privada (WIF)':<55}"
        divisoria_tabela = "=" * len(cabecalho)
        print("\n" + divisoria_tabela)
        print(cabecalho)
        print(divisoria_tabela)

        bip84_chg_ctx = bip84_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
        for i in range(num_enderecos):
            bip84_addr_ctx = bip84_chg_ctx.AddressIndex(i)
            endereco = bip84_addr_ctx.PublicKey().ToAddress()
            caminho = f"m/84'/0'/0'/0/{i}"
            chave_privada = bip84_addr_ctx.PrivateKey().ToWif()
            
            print(f" #{i:<5} | {caminho:<22} | {endereco:<45} | {chave_privada:<55}")

            qr_img = qrcode.make(endereco)
            nome_arquivo_qr = f"{qr_prefixo}-{i}-{endereco[:12]}... .png"
            caminho_salvar = os.path.join(PASTA_QR, nome_arquivo_qr)
            qr_img.save(caminho_salvar)
        
        print(divisoria_tabela)

    except ValueError as e:
        print(f"\n❌ ERRO: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}")
        return False
    
    return True

# --- FUNÇÕES PARA OS MODOS DO MENU ---
def modo_gerar_nova_carteira():
    """Gera uma nova seed e mostra a(s) carteira(s) de acordo com o uso de passphrase."""
    entropia = os.urandom(32)
    frase_seed = Mnemonic(IDIOMA_SEED).to_mnemonic(entropia)
    
    print("\n\n--- SUA NOVA SEED PHRASE DE 24 PALAVRAS ---")
    print("Anote estas 24 palavras em INGLÊS na ordem exata. Guarde-as de forma segura!")
    print(DIVISORIA_SECAO)
    palavras = frase_seed.split(' ')
    for i in range(0, len(palavras), 4):
        linha = [f'{j+1:02d}-{palavra: <12}' for j, palavra in enumerate(palavras[i:i+4], start=i)]
        print('   '.join(linha))
    print(DIVISORIA_SECAO)
    
    print("\nAgora, crie uma passphrase (senha) para sua carteira principal secreta.")
    print("ATENÇÃO: Se esquecê-la, seus fundos serão PERDIDOS PARA SEMPRE.")
    
    # --- LÓGICA DE CONFIRMAÇÃO DE SENHA ADICIONADA ---
    while True:
        passphrase_secreta = getpass.getpass("Digite a passphrase (deixe em branco para uma carteira padrão): ")
        if passphrase_secreta:
            passphrase_confirm = getpass.getpass("Confirme a passphrase: ")
            if passphrase_secreta == passphrase_confirm:
                print("✅ Passphrase confirmada com sucesso.")
                break
            else:
                print("❌ As passphrases não coincidem. Por favor, tente novamente.\n")
        else:
            # Usuário não quer passphrase, então saímos do loop
            break
            
    if passphrase_secreta:
        print("\nModo de segurança avançado ativado (com passphrase). Gerando duas carteiras...")
        derivar_e_mostrar_carteira(frase_seed, "", "CARTEIRA ISCA (SEM PASSPHRASE)", NUM_ENDERECOS_ISCA, "ISCA")
        derivar_e_mostrar_carteira(frase_seed, passphrase_secreta, "CARTEIRA PRINCIPAL (COM PASSPHRASE)", NUM_ENDERECOS_PADRAO, "PRINCIPAL")
    else:
        print("\nModo padrão ativado (sem passphrase). Gerando carteira única...")
        derivar_e_mostrar_carteira(frase_seed, "", "CARTEIRA PADRÃO (SEM PASSPHRASE)", NUM_ENDERECOS_PADRAO, "PADRAO")

def modo_restaurar_carteira():
    """Pede uma seed existente e mostra a carteira isca e a principal."""
    print("\nCole ou digite suas 12, 15, 18, 21 ou 24 palavras da seed (em inglês), separadas por espaço:")
    frase_seed_input = input("> ").strip().lower()

    if len(frase_seed_input.split()) not in [12, 15, 18, 21, 24]:
        print("\n❌ ERRO: Número de palavras inválido. Encerrando.")
        return

    passphrase_secreta = getpass.getpass("Digite a passphrase da sua carteira principal (deixe em branco se não houver): ")

    sucesso_isca = derivar_e_mostrar_carteira(frase_seed_input, "", "CARTEIRA BASE (SEM PASSPHRASE)", NUM_ENDERECOS_ISCA, "BASE")

    if sucesso_isca and passphrase_secreta:
        derivar_e_mostrar_carteira(frase_seed_input, passphrase_secreta, "CARTEIRA SECRETA (COM PASSPHRASE)", NUM_ENDERECOS_PADRAO, "SECRETA")

# --- LOOP DO MENU PRINCIPAL ---
while True:
    print("\n" + "="*40)
    print("        MENU PRINCIPAL DA CARTEIRA")
    print("="*40)
    print("O que você deseja fazer?")
    print("  [1] Gerar uma NOVA carteira")
    print("  [2] Restaurar / Visualizar uma carteira EXISTENTE")
    print("  [3] Sair")
    
    escolha = input("Escolha uma opção (1, 2 ou 3): ")
    
    if escolha == '1':
        modo_gerar_nova_carteira()
        break
    elif escolha == '2':
        modo_restaurar_carteira()
        break
    elif escolha == '3':
        print("Saindo do programa.")
        break
    else:
        print("❌ Opção inválida. Por favor, tente novamente.")
