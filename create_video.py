from pathlib import Path
import imageio_ffmpeg
import numpy as np
from PIL import Image
import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", default="./game.mp4", help="Name of the output video file")
args = parser.parse_args()
video_path = Path(args.o)
if video_path.suffix != ".mp4":
    raise ValueError(f"Video must be in mp4 format. Given: {video_path}")

# video_path = "./game-177-recreate.mp4"
s_width = 640
s_height = 480
fps = 15


frame = np.empty((s_width, s_height, 3), dtype=np.uint8)
# disable warning (due to frame size not being a multiple of 16)
writer = imageio_ffmpeg.write_frames(video_path, (s_width, s_height), ffmpeg_log_level="error",
                                     fps=fps, quality=9)
writer.send(None)  # Seed the generator

print(f"Creating video...")
dir_imgs = Path("./render")
files_imgs = list(dir_imgs.glob("*.png"))
files_imgs.sort(key=lambda x: int(x.stem))
for f_ in tqdm.tqdm(files_imgs, ncols=80):
    frame = Image.open(f_)
    frame = frame.resize((s_width, s_height))
    frame_np = np.ascontiguousarray(np.asarray(frame)[:, :, :3])
    writer.send(frame_np)

writer.close()
print(f"saved video to {video_path}")
