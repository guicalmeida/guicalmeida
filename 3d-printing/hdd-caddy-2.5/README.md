# Caddy de HD: 3.5" → 2.5"

`hdd_caddy_2.5.stl` é o `hdd_caddy_3.5_original.stl` adaptado para HD/SSD de 2.5",
gastando menos filamento e mantendo o encaixe no suporte original.

## O que mudou

| | Original 3.5" | 2.5" |
|---|---|---|
| Volume | 37,4 cm³ | 28,1 cm³ (−25%) |
| Envelope externo | 112 × 159,3 × 19,4 mm | idêntico |

- **Ficou igual** (é o que encaixa no suporte): paredes laterais com os trilhos e
  recortes, batentes traseiros, barra traseira superior, a frente toda (alça/trava,
  furo do pino) e o recorte do piso para o conector do backplane.
- **Saiu:** o piso em grade hexagonal.
- **Entrou:** quatro travessas de 5 × 2 mm, duas diagonais, ilhas para os parafusos
  inferiores e duas abas para parafusos laterais.

## Posição do disco

O 2.5" fica **encostado na parede esquerda** (olhando a traseira/conector, de pé),
**no batente traseiro** e **apoiado no plano do piso** (z = 2 mm), igual ao 3.5".
É assim que adaptadores para hot-swap alinham o conector SATA do 2.5" com a posição
do conector de um 3.5". Isso serve tanto para backplane quanto para cabo.

## Fixação (parafusos M3)

- 4 parafusos por baixo, nos furos inferiores do disco (como no original, a
  cabeça fica por baixo do piso).
- 2 parafusos laterais nas abas do lado direito. Use para discos sem furos inferiores.
- Os furos são **oblongos**: a SFF-8201 põe os furos a 14,0 e 90,6 mm de uma
  extremidade, e os oblongos servem para os dois sentidos. **Empurre o disco contra
  o batente traseiro antes de apertar.**

Serve para discos de 7, 9,5 e 12,5 mm (para 15 mm também, verificado sem colisão).

## Impressão

Mesma orientação do original (piso na mesa), sem suporte.

## Regerar

```
pip install trimesh manifold3d numpy networkx
python3 build.py hdd_caddy_3.5_original.stl hdd_caddy_2.5.stl
```

As cotas (posição do disco, largura das travessas, altura das abas) são
parâmetros no começo do `build.py`.
