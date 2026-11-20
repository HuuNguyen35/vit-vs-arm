# vit-vs-arm

Image-based visual servoing (IBVS) with DINOv2 features on a low-cost 5-DOF hobby-servo arm, reproducing the core result of ViT-VS (Scherl et al., IROS 2025): servoing with pretrained ViT features converges more reliably than classical (ORB) IBVS under lighting changes and partial occlusion.

**Team:** Tin (vision pipeline), Alex (embedded and robot side)

## How it works

1. The gripper camera streams images to the laptop (RTX 4060).
2. The goal image is encoded once with DINOv2. Each step, the current image is encoded and patches are matched to the goal by mutual nearest neighbors.
3. A rotation compensation step aligns the views before servoing.
4. Matched points feed the IBVS control law, which outputs a camera velocity.
5. The velocity is mapped to joint commands via the arm's Jacobian and sent to the servos through a PCA9685 driver on a Raspberry Pi 5.

## Repository layout

```
vit-vs-arm/
├── src/vitvs_arm/        # All library code
│   ├── vision/           # (Tin) calibration, DINOv2 + ORB matching,
│   │                     #       rotation compensation, IBVS control law
│   ├── robot/            # (Alex) kinematics, Jacobian, servo driver,
│   │                     #        depth sensor
│   ├── comms/            # Pi <-> laptop link (shared)
│   └── common/           # Shared types, config loading, logging (shared)
├── configs/              # YAML settings: camera intrinsics, servo limits, gains
├── scripts/              # Runnable entry points (calibrate, run servoing, experiments)
├── tests/                # Unit tests (e.g. IBVS math on synthetic points)
├── experiments/          # Experiment configs and result summaries
├── notebooks/            # Exploration only; nothing the pipeline depends on
├── docs/                 # Interface spec, wiring notes, report drafts
├── data/                 # Goal images, calibration photos (NOT tracked by git)
└── third_party/          # Code from other authors (ViT-VS), kept separate
```

### Conventions

- **Library code goes in `src/`, things you run go in `scripts/`.** Scripts stay short and call into the library.
- **No hard-coded numbers.** Gains, servo limits, and camera intrinsics live in `configs/`.
- **Don't import from `third_party/` directly.** Wrap it in our own module (e.g. `vision/dino_matcher.py`) so the rest of the code doesn't depend on it.
- **Stay in your own folder where possible.** Vision work goes in `vision/`, robot work in `robot/`. Shared folders (`comms/`, `common/`) get discussed first.
- **Never commit** large images, videos, or model weights. Share those through Google Drive.

## Interfaces between our halves

See `docs/interfaces.md` (to be written) for the agreed formats:
- Vision -> Robot: 6D camera velocity (units and frame specified)
- Robot -> Vision: depth value(s) and joint state
- Pi <-> Laptop: image frames and joint commands

## Getting started

```bash
git clone git@github.com:HuuNguyen35/vit-vs-arm.git
cd vit-vs-arm
python3 -m venv .venv
source .venv/bin/activate
```

Dependency files (laptop and Pi) will be added as the code takes shape.

## Git workflow

- `main` should always work. Don't commit unfinished work directly to it.
- Make a branch per task, named by area: `git checkout -b vision/dino-matcher`
- Push the branch and open a Pull Request; the other person reviews and merges.
- Run `git pull` at the start of every work session.
- Commit messages are short and imperative: "Add mutual nearest neighbor matching".

## Reference

- Scherl et al., ViT-VS (IROS 2025): https://arxiv.org/abs/2503.04545
- Authors' code: https://github.com/AlessandroScherl/ViT-VS
