"""Environment smoke test: imports, CUDA availability, and a tiny GPU computation.

Usage:  python scripts/cuda_smoke_test.py
Exits non-zero if a required import fails or CUDA is not usable.
"""
import importlib
import sys


def check_import(name):
    try:
        mod = importlib.import_module(name)
    except Exception as exc:  # noqa: BLE001 - report any import failure
        print(f"[FAIL] import {name}: {exc}")
        return None
    print(f"[ OK ] {name} {getattr(mod, '__version__', '')}")
    return mod


def main():
    ok = True
    for name in ("numpy", "cv2", "yaml", "pyrealsense2", "vitvs_arm"):
        ok &= check_import(name) is not None

    torch = check_import("torch")
    if torch is None:
        return 1

    if not torch.cuda.is_available():
        print("[FAIL] torch.cuda.is_available() is False "
              "(CPU-only torch build, or driver problem)")
        return 1
    print(f"[ OK ] CUDA {torch.version.cuda}, device: {torch.cuda.get_device_name(0)}")

    a = torch.randn(1024, 1024, device="cuda")
    b = torch.randn(1024, 1024, device="cuda")
    c = a @ b
    torch.cuda.synchronize()
    print(f"[ OK ] GPU matmul, result on {c.device}, mean={c.mean().item():.4f}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
