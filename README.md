# bitcoin-wallet-generator-py
A comprehensive, offline, command-line tool for securely generating and inspecting Bitcoin HD wallets (BIP-39/BIP-84) with passphrase and QR code support.
1. Criação Segura e Aleatória? (✅ SIM)

O que é necessário: Uma fonte de aleatoriedade imprevisível para criar a chave mestra.

O que nosso script faz: Usa os.urandom(32), que extrai entropia (aleatoriedade) diretamente do seu sistema operacional. Este é o padrão-ouro em Python para fins criptográficos. Não há como prever a seed que será gerada.

2. Backup Universal e Padronizado? (✅ SIM)

O que é necessário: Um formato de backup que seja legível por humanos e compatível com qualquer outra carteira no mundo.

O que nosso script faz: Gera uma BIP-39 Seed Phrase de 24 palavras em inglês. Este é o padrão universal. Você pode pegar essas 24 palavras e recuperar seus fundos em uma Ledger, Trezor, BlueWallet, Sparrow, Electrum... qualquer carteira de respeito no planeta.

3. Recuperação Garantida? (✅ SIM)

O que é necessário: A garantia de que, a partir do backup, você consegue recriar exatamente as mesmas chaves e endereços.

O que nosso script faz: O Modo [2] Restaurar do nosso script prova isso. Ao inserir a seed, ele regenera deterministicamente as mesmas chaves. O que você vê na geração é exatamente o que você verá na restauração.

4. Uso Online Seguro (Watch-Only)? (✅ SIM)

O que é necessário: Uma forma de verificar seu saldo e gerar novos endereços de recebimento em um dispositivo online (celular, PC) sem nunca expor suas chaves privadas.

O que nosso script faz: Ele gera a Chave Pública Estendida (XPUB), no formato zpub para Native SegWit. Esta é a peça-chave para a segurança do dia a dia. Importando apenas a XPUB em uma carteira, você tem uma "carteira somente-visualização" 100% segura.

5. Proteção Avançada Contra Roubo Físico e Coerção? (✅ SIM)

O que é necessário: Uma camada de segurança que protege seus fundos mesmo que alguém roube seu papel com as 24 palavras.

O que nosso script faz: Ele implementa a Passphrase (BIP-39), criando o sistema de Carteira Isca + Carteira Principal. Este é um recurso de segurança de nível especialista que oferece negação plausível e protege contra ataques físicos.

6. Eficiência e Modernidade? (✅ SIM)

O que é necessário: Usar os padrões mais recentes do Bitcoin para garantir compatibilidade e pagar as menores taxas de transação possíveis.

O que nosso script faz: Ele usa exclusivamente o BIP-84, gerando endereços Native SegWit (bc1...). Este é o padrão mais moderno e eficiente, garantindo que suas transações sejam mais baratas.

O que Não Falta, mas foi Propositalmente Deixado de Fora?
Existem funcionalidades de uma carteira completa que nosso script não tem, porque ele é uma ferramenta especializada em geração de chaves seguras (cold storage), e não uma carteira do dia a dia (hot wallet).

Assinatura de Transações: Nosso script não assina nem envia transações. Isso é proposital. A assinatura deve ser feita por um software de carteira (ou hardware wallet) onde você importa sua seed. Manter a geração de chaves separada da assinatura é um princípio fundamental de segurança.

Conexão com a Rede Bitcoin: Nosso script não se conecta à internet para ver saldos. Isso também é proposital, pois ele deve ser executado offline. A verificação de saldo é feita pela sua carteira "watch-only" (usando a XPUB).

Pense assim: nós não construímos o carro inteiro. Nós construímos o motor de uma Ferrari, perfeitamente projetado, seguro e de altíssimo desempenho. A "carroceria" (a interface gráfica, a conexão com a rede) é o papel de um aplicativo de carteira como a BlueWallet, que usará o motor perfeito que nós criamos.

Portanto, para o propósito que definimos — criar uma ferramenta soberana e completa para a geração e o gerenciamento seguro de chaves Bitcoin offline — não, não falta absolutamente nada. O resultado é uma ferramenta de nível profissional.







