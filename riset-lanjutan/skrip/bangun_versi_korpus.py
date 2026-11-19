"""Bangun versi baru korpus paralel dengan menerapkan penilaian penutur asli.

Setiap berkas penilaian memakai format `data/anotasi_penutur/penilaian_korpus_kami.csv`:
pair_id, lembar, keputusan, teks_bbc_baru, teks_id_baru (kosong bila tidak diubah), catatan.
Bila satu pasangan dinilai di beberapa lembar, lembar yang lebih belakang di --urutan yang berlaku.

Pemakaian (dari akar repo):
  python riset-lanjutan/skrip/bangun_versi_korpus.py --dasar data/btb_parallel_sentence.csv \
      --penilaian riset-lanjutan/data/anotasi_penutur/penilaian_korpus_kami.csv \
      --urutan C1,C6 --versi 1.1 --keluaran data/btb_parallel_sentence_v1.1.csv
Untuk versi berikutnya, --dasar adalah versi sebelumnya dan --penilaian berkas penilaian yang baru.
"""
import argparse
from pathlib import Path
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--dasar", required=True)
ap.add_argument("--penilaian", nargs="+", required=True)
ap.add_argument("--urutan", required=True, help="urutan prioritas lembar, yang terakhir paling kuat, mis. C1,C6")
ap.add_argument("--versi", required=True)
ap.add_argument("--keluaran", required=True)
ap.add_argument("--putusan_am", default="riset-lanjutan/data/anotasi_penutur/putusan_am_korpus_kami.csv")
a = ap.parse_args()

d = pd.read_csv(a.dasar, keep_default_na=False)
for kol, isi in [("pemeriksaan_penutur", ""), ("keputusan_penutur", ""), ("dikoreksi_pada_versi", ""), ("catatan_varietas", "")]:
    if kol not in d:
        d[kol] = isi
urut = {l: i for i, l in enumerate(a.urutan.split(","))}
p = pd.concat([pd.read_csv(f, keep_default_na=False) for f in a.penilaian], ignore_index=True)
tak_dikenal = set(p.lembar) - set(urut)
assert not tak_dikenal, f"lembar tidak ada di --urutan: {tak_dikenal}"
tak_ada = set(p.pair_id) - set(d.pair_id)
assert not tak_ada, f"pair_id tidak ada di korpus dasar: {sorted(tak_ada)[:5]}"
p["prioritas"] = p.lembar.map(urut)
d = d.set_index("pair_id")

n_ubah = {"toba": 0, "indonesia": 0}
for pid, g in p.sort_values("prioritas").groupby("pair_id", sort=False):
    akhir = g.iloc[-1]                                   # penilaian terkuat
    lama = d.at[pid, "pemeriksaan_penutur"]
    d.at[pid, "pemeriksaan_penutur"] = "+".join(dict.fromkeys([x for x in lama.split("+") if x] + list(g.lembar)))
    d.at[pid, "keputusan_penutur"] = akhir.keputusan
    # teks baru diambil dari penilaian terkuat; bila penilaian terkuat tidak memberi teks, pakai yang lebih lemah
    # hanya bila penilaian terkuat tidak menyatakan teksnya benar
    for kol, sisi in [("teks_bbc_baru", "toba_final"), ("teks_id_baru", "indo_final")]:
        baru = str(akhir[kol]).strip()
        if not baru and akhir.keputusan not in ("benar", "accept"):
            baru = next((str(x).strip() for x in g[kol][::-1] if str(x).strip()), "")
        if baru and baru != d.at[pid, sisi]:
            d.at[pid, sisi] = baru
            versi = [x for x in d.at[pid, "dikoreksi_pada_versi"].split("+") if x]
            d.at[pid, "dikoreksi_pada_versi"] = "+".join(dict.fromkeys(versi + [a.versi]))
            n_ubah["toba" if sisi == "toba_final" else "indonesia"] += 1

if Path(a.putusan_am).exists():
    for r in pd.read_csv(a.putusan_am).itertuples():
        if r.pair_id in d.index and r.putusan_penutur == "ada_unsur_AM" and not d.at[r.pair_id, "dikoreksi_pada_versi"]:
            d.at[r.pair_id, "catatan_varietas"] = f"ada unsur Angkola-Mandailing ({r.penanda}), menurut penutur asli"

d = d.reset_index()
assert d.pair_id.is_unique and (d.toba_final.str.strip() != "").all() and (d.indo_final.str.strip() != "").all()
d.to_csv(a.keluaran, index=False)
print(f"versi {a.versi}: {len(d)} pasangan | teks Toba diubah {n_ubah['toba']}, teks Indonesia diubah {n_ubah['indonesia']}")
print("pasangan diperiksa penutur:", int((d.pemeriksaan_penutur != "").sum()),
      "| dikoreksi pada versi ini:", int(d.dikoreksi_pada_versi.str.split("+").map(lambda x: a.versi in x).sum()),
      "| bercatatan varietas:", int((d.catatan_varietas != "").sum()))
