# Caddy de HD: 3.5" → 2.5"

`hdd_caddy_2.5.stl` é o `hdd_caddy_3.5_original.stl` adaptado para HD/SSD de 2.5".
Gasta menos filamento e mantém o encaixe no suporte original.

## O que mudou

| | Original 3.5" | 2.5" |
|---|---|---|
| Volume | 37,4 cm³ | 29,5 cm³ (−21%) |
| Envelope externo | 112 × 159,3 × 19,4 mm | idêntico |

- **Ficou igual** (é o que encaixa no suporte e o que leva o esforço de tirar e
  colocar): paredes laterais com trilhos e recortes, batentes traseiros, barra
  traseira superior, a frente toda (alça/trava, furo do pino) e o recorte do piso
  para o conector do backplane.
- **Saiu:** o piso em grade hexagonal.
- **Entrou:**
  - 4 travessas de 5 × 2 mm com mão-francesa nas paredes;
  - nervuras de 5 mm de altura no vão ao lado do disco;
  - 2 diagonais;
  - batentes dianteiros e um batente traseiro extra que prendem o disco no
    sentido do encaixe, sem depender do aperto dos parafusos.

## Posição do disco

O 2.5" fica **encostado na parede esquerda** (olhando a traseira/conector, de pé),
**entre os batentes traseiro e dianteiro** e **apoiado no plano do piso**
(z = 2 mm), igual ao 3.5". É assim que adaptadores para hot-swap alinham o conector
SATA do 2.5" com a posição do conector de um 3.5".

## Fixação: 4 parafusos pela face de baixo do disco

- **M3 cabeça chata (escareada)**, DIN 965 / ISO 7046, de **4 a 5 mm**. A cabeça
  fica embutida no piso, então nada sobra por baixo para raspar no cage. Não use
  parafuso mais longo: a rosca do disco é rasa.
- Os furos são **oblongos**: a SFF-8201 põe os furos a 14,0 e 90,6 mm de uma
  extremidade, e os oblongos servem para os dois sentidos. Quem posiciona o disco
  são os batentes; o parafuso só prende.

Serve para discos de 7 a 15 mm de altura.

## Impressão

Mesma orientação do original (piso na mesa), sem suporte. PETG ou PLA, 3 perímetros.

## Regerar

```
pip install trimesh manifold3d numpy networkx
python3 build.py hdd_caddy_3.5_original.stl hdd_caddy_2.5.stl
```

As cotas (posição do disco, travessas, nervuras, batentes) são parâmetros no
`build.py`.
