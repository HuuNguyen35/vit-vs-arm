"""Environment smoke test: checks imports, the GPU, and a small CUDA computation.

Run from the repo root:  python scripts/cuda_smoke_test.py
Exit code 0 = everything works, 1 = something failed.
"""
import importlib
import sys


def check_import(name):
    """Try to import a module by name; print its version or the error."""
    try:
        module = importlib.import_module(name)
    except Exception as err:
        print(f"[FAIL] {name}: {err}")
        return None
    print(f"[ OK ] {name} {getattr(module, '__version__', '')}")
    return module


def main():
    ok = True

    for name in ["numpy", "cv2", "yaml", "pyrealsense2", "vitvs_arm"]:
        if check_import(name) is None:
            ok = False

    torch = check_import("torch")
    if torch is None:
        return 1

    if not torch.cuda.is_available():
        print("[FAIL] torch.cuda.is_available() is False (CPU-only build or driver problem)")
        return 1
    print(f"[ OK ] CUDA {torch.version.cuda} on {torch.cuda.get_device_name(0)}")

    # Do real work on the GPU, not just a check that it exists.
    a = torch.randn(1024, 1024, device="cuda")
    b = torch.randn(1024, 1024, device="cuda")
    c = a @ b
    torch.cuda.synchronize()  # wait for the GPU to actually finish
    print(f"[ OK ] GPU matmul ran, result is on {c.device}")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())