#!/usr/bin/env python3
"""Download candidate images, verify they are real images, report results."""
import subprocess, os, sys

DEST = os.path.expanduser("~/workspace/solar-bahria-website/assets/images")
os.makedirs(DEST, exist_ok=True)

CANDIDATES = [
    # (url, filename)
    ("https://www.aaryonenergy.com/assets/hero-rooftop-solar-CIqKA7qp.jpg", "luxury-home-rooftop-solar-panels.jpg"),
    ("https://solarnidomy.cz/templates/yootheme/cache/f2/solarni-domy-solarni-domy-f2c4e5d6.jpeg", "modern-villa-solar-panels-pool.jpg"),
    ("https://suriahomesolar.com.my/wp-content/uploads/2026/08/solar-rooftop.jpg", "modern-house-flat-roof-solar.jpg"),
    ("https://www.sunlightandpower.com/sites/default/files/2023-02/residential_solar_castro_valley_hero1.jpg", "residential-rooftop-solar-panels.jpg"),
    ("https://exactsolar.com/wp-content/uploads/2024/09/mg-thumbnail.png", "aerial-home-solar-panels.png"),
    ("https://hccenergiasolar.com.br/wp-content/uploads/2022/08/jurazero-energia-solar-1-1024x683.jpeg", "solar-panel-installation-worker.jpg"),
    ("https://climatearchive.wpenginepowered.com/wp-content/uploads/2024/09/solar-mr-1600x800.png", "solar-installer-rooftop-work.png"),
    ("https://www.suness.com/data/upload/ueditor/20240408/6613bf8c69063.jpg", "solar-battery-storage-inverters.jpg"),
    ("https://rprorwxhikrmln5q-static.micyjz.com/cloud/lrBpjKkqloSRqljrolkjiq/home-energy-storage-system-lithium-battery-inverters.jpg", "hybrid-inverter-battery-system.jpg"),
    ("https://www.gmsolarkit.com/storage/uploads/images/202505/01/1746078743_qHE24lI4Kl.jpg", "solar-inverter-battery-wall.jpg"),
    ("https://www.ny-engineers.com/hs-fs/hubfs/commercial%20solar%20roof-1.jpg?width=1875&name=commercial%20solar%20roof-1.jpg", "commercial-rooftop-solar-panels.jpg"),
    ("https://cssb.com.my/assets/Solar_PV.webp", "commercial-solar-pv-roof.webp"),
    ("https://update-eu.cz/src/uploads/iStock-506200050-1641x1080.jpg", "solar-panel-cells-closeup.jpg"),
    ("https://res.cloudinary.com/stills-website/image/private/t_2xl,f_auto/v1/files/images/p-99e76509-ab33-4ce4-91be-f1cbbf7445fe.jpg", "solar-panels-blue-sky.jpg"),
    ("https://oc-static.poweredbyproctors.co.uk/public/images/26/01/23/EET_Solar-panel-field_low-angle-view_img_3-2.jpg?VersionId=h8nMM6ZLl3OsYKbSAejtWNw3lHFaeLjV", "solar-panel-field-low-angle.jpg"),
    ("https://ar.hugergy.com/js/htmledit/kindeditor/attached/20220901/20220901104339_37943.jpg", "solar-panel-roof-mounting.jpg"),
    ("https://ro.powerack.com/storage/uploads/images/202303/02/1677746216_b4snMewmey.jpg", "solar-panel-mounting-structure.jpg"),
    ("https://images.unsplash.com/photo-1509391366360-2e959784a276?auto=format&fit=crop&w=1600&q=80", "solar-panels-field-sunset.jpg"),
    ("https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?auto=format&fit=crop&w=1600&q=80", "solar-panels-sunset-field.jpg"),
    ("https://images.unsplash.com/photo-1613665813446-82a78c468a1d?auto=format&fit=crop&w=1600&q=80", "rooftop-solar-panels-house.jpg"),
    ("https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?auto=format&fit=crop&w=1600&q=80", "solar-panels-roof-sunset.jpg"),
    ("https://images.unsplash.com/photo-1509390144018-eeaf65052242?auto=format&fit=crop&w=1600&q=80", "solar-array-field.jpg"),
]

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def magic_ok(path):
    with open(path, "rb") as f:
        head = f.read(12)
    if head[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    return None

ok, fail = [], []
for url, name in CANDIDATES:
    dest = os.path.join(DEST, name)
    r = subprocess.run(["curl", "-fsSL", "--connect-timeout", "10", "--max-time", "60",
                        "-A", UA, "-H", "Accept: image/*;q=0.8", "-H", "Referer: https://www.google.com/",
                        "-o", dest, url], capture_output=True, text=True)
    if r.returncode != 0:
        fail.append((name, f"curl rc={r.returncode}"))
        continue
    kind = magic_ok(dest)
    size = os.path.getsize(dest)
    if kind is None or size < 5000:
        fail.append((name, f"bad magic/size {size}"))
        try: os.remove(dest)
        except OSError: pass
        continue
    ok.append((name, kind, size))
    print(f"OK   {name:45s} {kind:5s} {size:>8,} bytes")

print()
for name, why in fail:
    print(f"FAIL {name:45s} {why}")
print(f"\n{len(ok)} ok, {len(fail)} failed")
