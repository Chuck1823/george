# FamCloud GPU Rig — Shopping List

## Target: ~$1,120 per unit
$100/month × 12 months = $1,200 → hardware pays back in ~11 months.

## Parts List

### GPU: RTX 4060 Ti 16GB (~$450)
16GB VRAM — runs 7B models at full precision, 13B quantized
- Amazon: https://www.amazon.com/s?k=RTX+4060+Ti+16GB
- Newegg: https://www.newegg.com/p/pl?d=RTX+4060+Ti+16GB

### Motherboard: Mini-ITX B650 (~$200)
WiFi + Bluetooth included. Compatible with AMD Ryzen 5000/7000.
- Amazon: https://www.amazon.com/s?k=mini-itx+b650+motherboard

### CPU: AMD Ryzen 5 5600X (~$150)
6 cores, efficient, more than enough for inference + routing.
- Amazon: https://www.amazon.com/s?k=AMD+Ryzen+5+5600X

### RAM: 32GB DDR5 (~$80)
2x16GB kit, DDR5-4800 or higher.
- Amazon: https://www.amazon.com/s?k=32GB+DDR5+RAM

### Storage: 500GB NVMe SSD (~$40)
OS + models + workspace. Upgradable later.
- Amazon: https://www.amazon.com/s?k=500GB+NVMe+SSD

### Case: Mini-ITX Small Enclosed (~$100)
Small enough for a desk, looks like a product not a PC.
- NR200: https://www.amazon.com/Cooler-Master-NR200-Mini-ITX-Case/dp/B08CXT2ZKZ
- Fractal Ridge: https://www.amazon.com/s?k=fractal+ridge+mini+itx

### PSU: SFX 750W (~$100)
750W is plenty for 4060 Ti (165W) + Ryzen 5 (65W).
- Amazon: https://www.amazon.com/s?k=SFX+750W+power+supply

---

## Total: ~$1,120

## Assembly: 30-45 min
1. Mount CPU (lever, drop, close)
2. Click in RAM
3. Mount motherboard in case (4 screws)
4. Slot in GPU, screw, power cable
5. Connect PSU cables (3-4, keyed)
6. Close case, boot
7. Install Ubuntu from USB (15 min)

## Post-Install: FamCloud Bootstrap
Run the one-liner (script in experiment/scripts/bootstrap-gpu-rig.sh):
```
curl -sL <famcloud-url>/bootstrap-gpu-rig.sh | bash
```

Installs: NVIDIA drivers, Ollama/vLLM, OpenClaw, model weights, nightly update cron, SSH for remote support.
