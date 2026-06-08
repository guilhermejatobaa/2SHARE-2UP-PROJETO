# Gerenciador de Despesas Coletivas (Tema 10)

## Informações Acadêmicas
* **Instituição:** Unima
* **Curso:** Ciência da Computação
* **Matéria:** Projeto de Programação
* **Professor:** Amaury Nogueira
* **Aluno:** Guilherme Jatobá

---

## Sobre o Projeto
Este projeto consiste em uma solução de software robusta para a gestão e o rateio de despesas em grupos (estilo *Splitwise*). A aplicação permite cadastrar membros, registrar gastos com divisões personalizadas e executa um algoritmo inteligente de **Clearing (Liquidação)** para minimizar a quantidade de transferências financeiras necessárias para zerar as pendências de todos os participantes.

---

## Arquitetura e Decisões de Design (DDD)

O projeto foi totalmente desenvolvido seguindo os princípios de **DDD (Domain-Driven Design)** e **Arquitetura Limpa**, garantindo alta testabilidade, baixo acoplamento e separação estrita de responsabilidades.

```text
src/
├── domain/            # Regras de Negócio Puras (Sem dependências externas)
│   ├── money.py       # Value Object (Moeda e Centavos)
│   ├── member.py      # Entidade de Domínio
│   ├── expense.py     # Entidade de Domínio
│   ├── group.py       # Aggregate Root & Value Object Settlement
│   └── exceptions.py  # Erros de Negócio Customizados
├── application/       # Orquestração e Casos de Uso
│   └── group_service.py