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