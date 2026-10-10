"""Converte o caddy 3.5" em caddy 2.5" mantendo a interface com o suporte."""
import sys, numpy as np, trimesh, manifold3d as mf

src, out = sys.argv[1], sys.argv[2]
orig = trimesh.load(src)

def to_mf(m):
    return mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices, np.float32),
                               tri_verts=np.asarray(m.faces, np.uint32)))
def to_tm(M):
    g = M.to_mesh()
    return trimesh.Trimesh(g.vert_properties[:, :3], g.tri_verts, process=True)
def box(x0, x1, y0, y1, z0, z1):
    return mf.Manifold.cube([x1-x0, y1-y0, z1-z0]).translate([x0, y0, z0])
def ycyl_slot_x(x0, x1, ya, yb, z, d):
    """Furo oblongo atravessando em X, estendido em Y de ya a yb, centro em z."""
    r = d/2
    c = mf.Manifold.cylinder(x1-x0, r, r, 48).rotate([0, 90, 0]).translate([x0, 0, z])
    return mf.Manifold.batch_hull([c.translate([0, ya, 0]), c.translate([0, yb, 0])])
def zslot(x, ya, yb, d, z0=-1, z1=3):
    r = d/2
    c = mf.Manifold.cylinder(z1-z0, r, r, 48).translate([x, 0, z0])
    return mf.Manifold.batch_hull([c.translate([0, ya, 0]), c.translate([0, yb, 0])])

# --- Geometria do original (medida do STL) ---
XL, XR = -408.0, -306.0       # faces internas das paredes laterais
Y_STOP = 5.17                 # face dos batentes traseiros (lado do conector)
Y_FRONT = 143.0               # a partir daqui a frente (alca/trava) fica intacta
FLOOR = 2.0                   # espessura do piso / plano de apoio do disco
KEEP_OUT = (-401.0, -355.0, 19.5)  # recorte p/ conector do backplane (x0, x1, y<)

# --- HD 2.5" (SFF-8201): 69.85 x 100.2; furos a 14.00 e 90.60 de uma extremidade,
# inferiores a 4.07 das laterais, laterais a 3.00 do fundo. Encostado na parede
# esquerda, no batente traseiro e no plano do piso -> conector SATA na mesma
# posicao do conector de um 3.5" (exigencia para backplane hot-swap).
W25, L25 = 69.85, 100.2
dx0 = XL; dx1 = XL + W25
hole_x = [dx0 + 4.07, dx1 - 4.07]
# Oblongos cobrem as duas convencoes de referencia (14.0/90.6 a partir do
# conector ou da frente do disco).
slots_y = [(Y_STOP + 9.6, Y_STOP + 14.0), (Y_STOP + 86.2, Y_STOP + 90.6)]
HOLE_D = 3.4

base = to_mf(orig)
# 1) remove a grade hexagonal do piso entre as paredes (frente e batentes ficam)
base = base - box(XL, XR, Y_STOP, Y_FRONT, -1, FLOOR + 0.5)

# 2) quadro (z 0..2 sob o disco), sobrepondo 0.6 mm nas paredes
o = 0.6
T = FLOOR
BW = 5.0                      # largura das travessas
RIB_H = 5.0                   # altura das nervuras no vao direito (fora do disco)
RIB_X0 = dx1 + 0.5            # nervuras so a direita do disco
Y_FSTOP = Y_STOP + 100.45 + 0.15   # batente dianteiro (comprimento max. do 2.5")
parts = []
YA = KEEP_OUT[2] + BW/2 + 0.25                    # logo atras do recorte do conector
YB = (slots_y[1][0] + slots_y[1][1]) / 2          # passa pelos furos dianteiros
YD = Y_FSTOP + BW/2                               # segura o batente dianteiro
cross = (YA, 57.0, YB, YD)
for yc in cross:
    parts.append(box(XL - o, XR + o, yc - BW/2, yc + BW/2, 0, T))
    # nervura vertical no vao direito (rigidez a flexao/torcao)
    parts.append(box(RIB_X0, XR + o, yc - 1.0, yc + 1.0, 0, RIB_H))
    # mao-francesa no plano, nas duas paredes
    for xw, sx in ((XL, 1), (XR, -1)):
        for sy in (1, -1):
            tri = [(0, 0), (6 * sx, 0), (0, 6 * sy)]
            g = mf.CrossSection([tri if sx * sy > 0 else tri[::-1]])
            parts.append(mf.Manifold.extrude(g, T).translate([xw, yc + sy * BW/2, 0]))

# ilhas em volta dos furos inferiores, ligadas a parede / travessas
for ya, yb in slots_y:
    y0, y1 = ya - 4.2, yb + 4.2
    rear = ya < KEEP_OUT[2]
    if rear:
        y0, y1 = Y_STOP - 1.99, max(y1, YA)
    parts.append(box(XL - o, (KEEP_OUT[0] + 1.0) if rear else hole_x[0] + 5.0, y0, y1, 0, T))
    parts.append(box(hole_x[1] - 5.0, hole_x[1] + 5.0, y0, y1, 0, T))
# batente traseiro do lado direito do disco (o original so encosta no esquerdo)
parts.append(box(hole_x[1] - 5.0, dx1 - 0.5, Y_STOP - 1.99, Y_STOP, 0, FLOOR + 5.0))
# batentes dianteiros: travam o disco quando o conector empurra no encaixe
for xa, xb in ((XL - o, XL + 12.0), (dx1 - 16.0, dx1 + 2.0)):
    parts.append(box(xa, xb, Y_FSTOP, Y_FSTOP + 3.0, 0, FLOOR + 4.0))
# diagonais nervuradas no vao direito (contra paralelogramo)
def bar(p0, p1, w, h):
    p0, p1 = np.array(p0), np.array(p1)
    v = p1 - p0; L = np.linalg.norm(v); a = np.degrees(np.arctan2(v[1], v[0]))
    return box(0, L, -w/2, w/2, 0, h).rotate([0, 0, a]).translate([p0[0], p0[1], 0])
for p0, p1 in (((RIB_X0 + 1, YA + 2), (XR, 57.0 - 2)),
               ((RIB_X0 + 1, YB - 2), (XR, 57.0 + 2))):
    parts.append(bar(p0, p1, 4.0, T))

frame = mf.Manifold.batch_boolean(parts, mf.OpType.Add)
# furos inferiores: oblongos escareados (parafuso M3 cabeca chata fica embutido,
# nada sobra por baixo para raspar no cage)
def csk_slot(x, ya, yb):
    d0, d1 = 6.4, HOLE_D
    cone = mf.Manifold.cylinder((d0 - d1) / 2, d0 / 2, d1 / 2, 48).translate([x, 0, -0.01])
    thru = mf.Manifold.cylinder(T + 2, d1 / 2, d1 / 2, 48).translate([x, 0, -1])
    one = cone + thru
    return mf.Manifold.batch_hull([one.translate([0, ya, 0]), one.translate([0, yb, 0])])
cut = [csk_slot(hx, ya, yb) for ya, yb in slots_y for hx in hole_x]
frame = frame - mf.Manifold.batch_boolean(cut, mf.OpType.Add)
# nada do quadro pode invadir o recorte do conector nem sair do envelope
frame = frame - box(KEEP_OUT[0], KEEP_OUT[1], 0, KEEP_OUT[2], -1, 30)

res = base + frame
m = to_tm(res)
m.export(out)
print('faces', len(m.faces), 'watertight', m.is_watertight,
      'vol cm3 %.2f (orig %.2f)' % (m.volume/1000, orig.volume/1000),
      'bounds', np.round(m.bounds, 2).tolist())
# checagem: disco 2.5" (9.5 mm) nao colide com o modelo
drive = box(dx0 + .02, dx1 - .02, Y_STOP + .02, Y_STOP + L25 - .02, FLOOR + .02, FLOOR + 9.5)
print('interferencia disco (mm3): %.3f' % (res ^ drive).volume())
drive15 = box(dx0 + .02, dx1 - .02, Y_STOP + .02, Y_STOP + 100.45 - .02, FLOOR + .02, FLOOR + 15)
print('interferencia disco 15mm (mm3): %.3f' % (res ^ drive15).volume())
# checagem: envelope externo identico fora do miolo do piso
ob = orig.bounds; print('bounds iguais:', np.allclose(m.bounds, ob, atol=1e-3))
