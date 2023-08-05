import click
import os
from moviepy.editor import VideoFileClip


class Movie:
    def __init__(self, file_name, path_to_save, start_time, step):
        self.file_name = file_name
        self.path_to_save = path_to_save
        self.start_time = start_time
        self.step = step

    def extract_frames(self):
        clip = VideoFileClip(self.file_name)
        duration = clip.duration * 1000

        if self.start_time > duration:
            print('Error: Start time is greater than the video duration.')
            return

        # if self.step  is 0, only one frame must be taken
        if self.step == 0:
            time = self.start_time / 1000  # time in s
            imgpath = os.path.join(self.path_to_save, '{}.png'.format(time))
            clip.save_frame(imgpath, time)
            return

        # else must take a frame every self.step milliseconds
        times = [(t + self.start_time) / 1000 for t in range(0, int(duration), self.step)]
        for t in times:
            imgpath = os.path.join(self.path_to_save, '{}.png'.format(t))
            clip.save_frame(imgpath, t)


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(exists=True, dir_okay=True),
              help="Path to directory where images will be saved",
              default='.')
@click.option('--start-time', '-t',
              help="Time of first frame to capture, in milliseconds. Default to start of video",
              default=0)
@click.option('--step', '-s',
              help="Capture a frame every <step> milliseconds. If 0, captures only the frame stated in --start-time",
              default=0)
def pyctorize(filename, output, start_time, step):
    movie = Movie(filename, output, start_time, step)
    click.echo("Generating images...")
    movie.extract_frames()


if __name__ == '__main__':
    pyctorize()
