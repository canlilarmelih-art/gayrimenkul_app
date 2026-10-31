#!/usr/bin/env python3
"""OSM XML parçalarını (api/0.6/map) tek bir sade JSON'a çevirir.
Kullanım: python3 build_data.py <osm_klasoru> <cikti.json>
Koordinatlar metre cinsinden (x=doğu, y=kuzey), merkeze göre.
"""
import sys, glob, json, math
import xml.etree.ElementTree as ET

src, out = sys.argv[1], sys.argv[2]
nodes, ways = {}, {}
for f in glob.glob(f"{src}/*.osm"):
    try:
        root = ET.parse(f).getroot()
    except ET.ParseError:
        continue
    for n in root.iter("node"):
        nodes[n.get("id")] = (float(n.get("lon")), float(n.get("lat")))
    for w in root.iter("way"):
        wid = w.get("id")
        if wid in ways:
            continue
        ways[wid] = ([nd.get("ref") for nd in w.iter("nd")],
                     {t.get("k"): t.get("v") for t in w.iter("tag")})

lons = [p[0] for p in nodes.values()]; lats = [p[1] for p in nodes.values()]
lon0 = (min(lons) + max(lons)) / 2; lat0 = (min(lats) + max(lats)) / 2
kx = 111320 * math.cos(math.radians(lat0)); ky = 110574

def pts(refs):
    return [[round((nodes[r][0]-lon0)*kx, 1), round((nodes[r][1]-lat0)*ky, 1)]
            for r in refs if r in nodes]

def height(t):
    for k in ("height", "building:height"):
        if k in t:
            try: return float(t[k].split()[0].replace(",", "."))
            except ValueError: pass
    for k in ("building:levels", "levels"):
        if k in t:
            try: return float(t[k]) * 3.0 + 1.5
            except ValueError: pass
    b = t.get("building")
    return {"house": 6, "detached": 6, "garage": 3, "shed": 3, "roof": 3,
            "commercial": 14, "retail": 12, "office": 20, "hotel": 22,
            "apartments": 15, "mosque": 12}.get(b, 11)

res = {"origin": [lon0, lat0], "buildings": [], "roads": [], "water": [], "parks": []}
ROAD_W = {"motorway": 14, "trunk": 14, "primary": 12, "secondary": 10, "tertiary": 8,
          "residential": 6, "unclassified": 6, "pedestrian": 5}
for refs, t in ways.values():
    p = pts(refs)
    if len(p) < 2: continue
    closed = refs[0] == refs[-1] and len(p) >= 4
    if "building" in t and closed:
        res["buildings"].append({"p": p[:-1], "h": round(height(t), 1),
                                 "n": t.get("name", ""), "k": t.get("building")})
    elif t.get("highway") in ROAD_W:
        res["roads"].append({"p": p, "w": ROAD_W[t["highway"]], "k": t["highway"]})
    elif t.get("natural") == "water" and closed:
        res["water"].append({"p": p[:-1]})
    elif (t.get("leisure") in ("park", "garden") or t.get("landuse") in ("grass", "forest")) and closed:
        res["parks"].append({"p": p[:-1]})

xs = [q[0] for b in res["buildings"] for q in b["p"]]; ys = [q[1] for b in res["buildings"] for q in b["p"]]
res["bounds"] = [min(xs), min(ys), max(xs), max(ys)] if xs else [0, 0, 0, 0]
json.dump(res, open(out, "w"), separators=(",", ":"), ensure_ascii=False)
print({k: len(v) for k, v in res.items() if isinstance(v, list)}, "bounds", res["bounds"])
