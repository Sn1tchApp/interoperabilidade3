
# Instalação do Docker

## Instalação do Docker e Docker Compose
```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common
sudo curl -sSL https://get.docker.com/ | sh
sudo systemctl enable docker
sudo systemctl start docker
sudo curl -SL https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-linux-$(uname -m) -o /usr/libexec/docker/cli-plugins/docker-compose
sudo chmod +x /usr/libexec/docker/cli-plugins/docker-compose
```

# Instalação do Wazuh Single Node

## Referência:
[Wazuh Container Documentation](https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html)

### Clona o repositório Wazuh na tag v4.9.0
```bash
git clone --branch tags/v4.9.0 --single-branch https://github.com/wazuh/wazuh-docker.git
```

### Entra na pasta do repositório
```bash
cd wazuh-docker/single-node
```

### Instala os certificados Wazuh
```bash
docker compose -f generate-indexer-certs.yml run --rm generator
```

### Sobe o Wazuh
```bash
docker compose up -d
```

# Instalação do Suricata

## Referência:
[Suricata Quickstart Guide](https://docs.suricata.io/en/suricata-6.0.9/quickstart.html#running-suricata)

### Instalação do Suricata no host AWS
```bash
sudo add-apt-repository ppa:oisf/suricata-stable
sudo apt-get install suricata
sudo systemctl start suricata
sudo systemctl enable suricata
```

### Configuração do Suricata

Edite o arquivo `/etc/suricata/suricata.yaml` para habilitar a inspeção de tráfego nas redes e nas interfaces de rede.

Minhas redes eram:
- 10.0.0.0 (rede Docker)
- 172.31.0.0 (rede do host da AWS)

```yaml
address-groups:
  HOME_NET: "[10.0.0.0/16,172.31.0.0/16]"
```

### Configuração das interfaces
No mesmo arquivo, na seção `af-packet`, adicione as interfaces que deseja inspecionar:

```yaml
af-packet:
  - interface: docker0
  - interface: ens5
```

### Criação de regras Suricata

Adicione as seguintes regras no arquivo `/var/lib/suricata/rules/sqli.rules`:

```yaml
alert http any any -> any any (msg:"SQLI - CLAUSULA SELECT IDENTIFICADA"; content:"SELECT"; http_client_body; nocase; classtype:alert; sid:1000007; rev:1;)
alert http any any -> any any (msg:"SQLI - CLAUSULA UNION IDENTIFICADA"; content:"UNION"; http_client_body; nocase; classtype:alert; sid:1000008; rev:1;)
alert http any any -> any any (msg:"SQLI - CLAUSULA OR IDENTIFICADA"; content:"OR"; http_client_body; nocase; classtype:alert; sid:1000009; rev:1;)
alert http any any -> any any (msg:"SQLI - CLAUSULA UPDATE IDENTIFICADA"; content:"UPDATE"; http_client_body; nocase; classtype:alert; sid:1000010; rev:1;)
```

### Teste se as regras estão funcionando
```bash
suricata -T -c /etc/suricata/suricata.yaml
```

### Monitore as regras sendo detectadas
```bash
tail -f /var/log/suricata/fast.log
```

# Instalação do Wazuh Agent para enviar logs do Suricata para Wazuh

## Referência:
[Integrate Network IDS Suricata](https://documentation.wazuh.com/current/proof-of-concept-guide/integrate-network-ids-suricata.html)

### Instalação do Agente

Instale o agente Wazuh através do console de gerenciamento. Siga o passo a passo no seguinte link:
[Deploy do Agente Wazuh](https://IP_DO_SEU_SERVIDOR_WAZUH/app/endpoints-summary#/agents-preview/deploy)

### Configuração do log do Suricata para o Wazuh

Adicione a seguinte configuração ao arquivo `/var/ossec/etc/ossec.conf` do agente Wazuh no final do arquivo. Isso permite que o agente leia o arquivo de logs do Suricata:

```xml
<ossec_config>
  <localfile>
    <log_format>json</log_format>
    <location>/var/log/suricata/eve.json</location>
  </localfile>
</ossec_config>
```

### Reinicie o agente
```bash
sudo systemctl restart wazuh-agent.service
```

