# Redes I

___

Projetos de laboratório desenvolvidos na disciplina de Redes durante o 5º semestre da graduação em Ciência da Computação.



## Chat TCP (P2P)

____

Este é um exemplo simples de um chat ponto-a-ponto (peer-to-peer) em Python usando sockets, no qual dois clientes podem se conectar diretamente entre si para enviar e receber mensagens.

### Utilização

Requisitos: Python 3.x, Tkinter (biblioteca da interface implementada).

### Host (host.py)

O host escutará conexões na interface de rede em um endereço IP e porta específicos. Assim que executado, ele aguardará a conexão do cliente.

- listen_ip / listen_port: estabelece o endereço de IP e a porta a serem escutados,
  respectivamente.
- receive_messages: função responsável pela criação de uma thread para lidar com a recepção de mensagens quando o cliente estabelece conexão com o host; possibilitando, dessa forma, o envio e recebimento de mensagens neste ponto.

### Cliente (client.py)

O cliente tentará se conectar ao host usando o endereço IP e a porta do host. Assim que executado, a conexão tentará ser estabelecida.

- remote_ip / remote_port: estabelece o endereço de IP e a porta para conexão com o host,
  respectivamente.
- receive_messages: função responsável pela criação de uma thread para lidar com a recepção
  de mensagens quando o cliente estabelece conexão com o host; possibilita ndo, dessa forma, o
  envio e recebimento de mensagens neste ponto.

### Comunicação

Ambos os clientes podem enviar e receber mensagens digitadas, as quais são enviadas entre os pontos por meio da conexão direta.

### Interface

A implementação da interface não é necessária para o funcionamento desse chat, que pode ser executado no terminal dos diferentes pontos; entretanto, foi implementada uma interface básica com o pacote tkinter.

### Observações

Este é um exemplo básico e não leva em consideração cenários complexos de rede, como NAT traversal, firewalls, segurança, entre outros. A funcionalidade é limitada e pode ser afetada por restrições de rede e, nesse sentido, é importante assegurar-se de que os clientes possam se conectar entre si dentro da mesma rede local (LAN) e que não haja bloqueios de firewall que impeçam a comunicação direta.





## TRANSFERÊNCIA DE STRINGS VIA UDP

____

Esta documentação detalha a aplicação desenvolvida para a transferência de strings entre dois
computadores utilizando o protocolo UDP. A aplicação atende aos requisitos e faz uso das seguintes
funções e módulos nos scripts ‘sender.py’ e ‘receiver.py’.

### Utilização

Requisitos: Python 3.x, fpdf.

### Sender (sender.py)

O Sender é responsável por enviar os dados para o destinatário. Ele implementa as seguintes
funcionalidades:

- send_message(message, checksum, dest): Esta função é responsável por enviar um pacote de
  dados para o destinatário. O processo envolve o envio do pacote e o registro de informações
  relacionadas ao pacote enviado, incluindo seu conteúdo e checksum.
- send(data, dest): Esta função desempenha um papel fundamental na transferência de dados.
  Ela divide a mensagem em pacotes de tamanho especificado, calcula o checksum para cada
  pacote e realiza o envio. Além disso, gera um relatório detalhado da transmissão e encerra o
  socket após a conclusão.
- send_report(data, dest): Responsável por enviar um relatório abrangente ao destinatário. Isso
  envolve o estabelecimento de uma conexão TCP, o envio dos dados doCo relatório e o
  fechamento da conexão.
- __init__: O construtor da classe Sender cria um socket UDP, essencial para a comunicação
  entre remetente e destinatário.

### Receiver (receiver.py)

O Receiver é responsável por receber e validar os pacotes do remetente. Ele Implementa as
seguintes funcionalidades:

- receive_message(): Esta função é encarregada de receber os pacotes de dados enviados pelo
  remetente. Ela desempenha um papel crítico na validação da integridade dos pacotes,
  calculando o checksum e reconstituindo a mensagem original.
- receive_report(: Esta função lida com a recepção e análise do relatório de transmissão
  enviado pelo remetente. Ela estabelece uma conexão TCP, extrai as informações do relatório e
  exibe os resultados.
- __init__: O construtor da classe Receiver inicializa um socket UDP necessário para a recepção
  dos pacotes de dados.

### Comunicação 

A comunicação envolve a transmissão de dados do remetente para o destinatário via UDP,
com verificação de integridade, seguida da geração e envio de um relatório detalhado via TCP. Esse
processo permite a transferência confiável de dados entre os computadores e o registro das estatísticas
da transmissão.



### Observações

Essa aplicação é uma demonstração prática e esclarecedora dos conceitos essenciais da
comunicação em redes de computadores. Ela oferece uma visão abrangente das operações
fundamentais, como o uso dos protocolos UDP e TCP para transferência de dados, a fragmentação da
informação em pacotes, a aplicação de checksums para garantir a integridade dos dados e a avaliação
do desempenho da rede.

Além disso, a aplicação não apenas aborda esses conceitos, mas também os coloca em prática
de maneira coerente e interativa. Ela permite que os usuários observem como os dados são divididos,
transmitidos e verificados, fornecendo uma compreensão prática da dinâmica por trás da comunicação
em redes.1

Assim, esta aplicação vai além do seu papel como ferramenta educacional, pois também se
apresenta como uma base sólida para iniciar investigações em tópicos avançados relacionados à
transferência de dados em redes de computadores.