# XL-Log — Sistema de Gerenciamento de Tarefas

## Objetivo
O XL-Log foi desenvolvido como parte do Portfólio Átomo de **Engenharia de Software**.  
O projeto simula o desenvolvimento de um sistema ágil para gerenciamento de tarefas,  
aplicando conceitos práticos de **planejamento, versionamento, controle de qualidade e gestão de mudanças**.

---

## Tecnologias Utilizadas
- Python 3.11  
- Flask 3.x  
- SQLAlchemy  
- SQLite  
- Bootstrap 5  
- Git + GitHub Actions + Pytest

---

## Funcionalidades
- CRUD completo de tarefas  
- Interface web simples  
- Banco de dados local (SQLite)  
- Estrutura modular (models, templates, main)  
- Testes automatizados (Pytest)  
- Integração contínua com **GitHub Actions**

---

## Metodologia Ágil
O projeto segue o modelo **Kanban** utilizando o GitHub Projects.  
Quadro configurado com as colunas:

- 🟡 A Fazer  
- 🔵 Em Progresso  
- 🟢 Concluído  

As tarefas foram organizadas conforme o ciclo de desenvolvimento.

---

##  Mudança de Escopo (Simulada)
Durante o desenvolvimento, decidiu-se **adicionar o campo de “prioridade”** às tarefas,  
atendendo à solicitação de usuários que desejavam destacar atividades críticas.  
Essa alteração foi registrada no README e refletida no quadro Kanban e no código.

---

## Controle de Qualidade
Os testes automatizados foram implementados com **Pytest** e executados automaticamente  
via **GitHub Actions** em cada push ou pull request, garantindo estabilidade e confiabilidade.

Workflow principal:  
`.github/workflows/tests.yml`

---

### Execução Local

pip install -r requirements.txt
python main.py

A aplicação será executada em:
-> http://127.0.0.1:5000/

## Modelagem UML

Os diagramas foram elaborados no draw.io e estão em:
/docs/uml/

Incluem:

- Diagrama de Casos de Uso

- Diagrama de Classes

## Autor

Rafael H. Gozzo
Repositório: XL-Log Portfólio

## Referências

* Pressman, R. S. — Engenharia de Software: Uma Abordagem Profissional.
* Documentação Oficial do GitHub Actions
* Artigo Atlassian — Como Usar o Kanban no GitHub para Melhorar a Produtividade.


alo alo testando
tenho que fazer mais 6 commits :( pq Deus?