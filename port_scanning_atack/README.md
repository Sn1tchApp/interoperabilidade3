# Como executar em conteiner
1. docker build -t port_attack_simul .
2. docker run --rm -it --network host port_attack_simul

- Verificar se a chave da imagem python sendo executada no docker é igual a definida no dockerfile
