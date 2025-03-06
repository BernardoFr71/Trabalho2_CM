# Flet Solitaire

Este projeto é uma implementação do clássico jogo de paciência (Solitário) utilizando a biblioteca **Flet** em Python. O jogo inclui funcionalidades como desfazer jogadas, salvar e carregar o estado do jogo, escolher o design das cartas, um modo cronometrado e um sistema de pontuação.

## Funcionalidades

### 1. **Desfazer Jogadas (Undo)**
   - Permite ao jogador desfazer a última jogada, útil para corrigir erros ou experimentar diferentes estratégias.
   - O histórico de jogadas é armazenado, permitindo desfazer múltiplas jogadas.

### 2. **Salvar e Carregar o Estado do Jogo**
   - O jogador pode salvar o progresso do jogo e carregá-lo posteriormente, permitindo continuar de onde parou.
   - O estado do jogo é salvo em um arquivo JSON (`saved_game.json`).

### 3. **Escolher o Design das Cartas**
   - O jogador pode escolher entre diferentes designs para as costas das cartas, personalizando a aparência do jogo.
   - As opções de design são: `card_back0.png`, `card_back1.png`, `card_back2.png` e `card_back3.png`.

### 4. **Modo de Jogo Cronometrado**
   - Adiciona um temporizador ao jogo, onde o jogador tem 5 minutos para completar o jogo.
   - O tempo restante é exibido na barra de aplicativos.
   - Quando o tempo acaba, o jogo é encerrado automaticamente.

### 5. **Sistema de Pontuação**
   - O jogador ganha pontos ao mover cartas para as fundações.
   - A pontuação é calculada com base no número de cartas movidas para as fundações e no tempo restante ao final do jogo.

### 6. **Regras do Jogo**
   - O jogo segue as regras clássicas do Solitário (Klondike).
   - O objetivo é mover todas as cartas para as fundações, organizadas por naipe e em ordem crescente (de Ás a Rei).

## Como Executar o Projeto

### Pré-requisitos
- Python 3.7 ou superior.
- Biblioteca Flet instalada.

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/flet-solitaire.git
   cd flet-solitaire