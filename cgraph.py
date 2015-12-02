import moviepy.video.tools.drawing as dw
import numpy as np
import cv2
import argparse

from moviepy.editor import *

# params
t_begin = 10.5
t_end   = 10.8
max_height = 240
in_movie_name = "movie.mp4"
out_gif_name = "cinemagraph.gif"
mask_name = "mask.png"
gif_fuzz=3
gif_fps=15

def create_cinemagraph(mask_helper=False):
    og_clip = VideoFileClip(in_movie_name, audio=False).subclip((t_begin),(t_end))

    if og_clip.size[0] > max_height:
        og_clip = og_clip.resize(height=max_height)
        
    if mask_helper:
        og_clip.save_frame("mask_helper1.png", 0.0)
        og_clip.save_frame("mask_helper2.png", (t_end - t_begin) / 2.0)
        og_clip.save_frame("mask_helper3.png", t_end - t_begin)
        mask = np.zeros((og_clip.size[1], og_clip.size[0]))
    else:
        mask = cv2.imread(mask_name, cv2.IMREAD_GRAYSCALE)
        mask = cv2.resize(mask, og_clip.size)
        mask = cv2.normalize(mask.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)

    cv2.imwrite("mask_resized.png", mask * 255.0)

    snapshot = (og_clip.to_ImageClip()
                .set_duration(og_clip.duration)
                .set_mask(ImageClip(mask, ismask=True)))

    composition = CompositeVideoClip([og_clip,snapshot]).speedx(0.2)

    composition.write_gif(out_gif_name, fps=gif_fps, fuzz=gif_fuzz)   
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    parser.add_argument('-m', dest='mask_helper', action='store_true')
    args = parser.parse_args()
    print "args:"
    print args
    create_cinemagraph(args.mask_helper)
