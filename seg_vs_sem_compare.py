from ultralytics import YOLO
import argparse
import os

# ----------------------------
# Model loader helper
# ----------------------------
def load_model(model_type, size):
    """
    model_type: 'seg' or 'sem'
    size: n, s, m, l, x
    """
    return YOLO(f"yolo26{size}-{model_type}.pt")


# ----------------------------
# Run inference
# ----------------------------
def run(model, video_path, tag):
    print(f"[INFO] Running: {tag}")
    model(video_path, save=True)
    print(f"[DONE] {tag}")


# ----------------------------
# Main logic
# ----------------------------
def main(args):
    video_path = args.video

    # ----------------------------
    # Instance / Seg comparison
    # ----------------------------
    if args.compare == "both":
        for size in args.sizes:
            run(load_model("seg", size), video_path, f"INSTANCE-{size}")
            run(load_model("sem", size), video_path, f"SEMANTIC-{size}")

    # ----------------------------
    # Only instance (seg)
    # ----------------------------
    elif args.compare == "seg":
        for size in args.sizes:
            run(load_model("seg", size), video_path, f"INSTANCE-{size}")

    # ----------------------------
    # Only semantic (sem)
    # ----------------------------
    elif args.compare == "sem":
        for size in args.sizes:
            run(load_model("sem", size), video_path, f"SEMANTIC-{size}")

    else:
        print("Invalid compare mode. Use: both | seg | sem")


# ----------------------------
# CLI
# ----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True, help="path to input video")
    parser.add_argument("--compare", type=str, default="both",
                        help="both | seg | sem")

    parser.add_argument("--sizes", nargs="+", default=["n", "m", "x"],
                        help="model sizes n s m l x")

    args = parser.parse_args()
    main(args)