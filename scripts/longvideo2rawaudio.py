import moviepy.editor as mp
from pydub import AudioSegment
import argparse
import os
import time

long_video_dir = "./long_video/"
long_audio_dir = "./long_audio/"
raw_audio_dir = "./raw_audio/"
filelist = list(os.walk(long_video_dir))[0][2]

def extract_audio(videos_file_path,audio_file_path):
    print('\n当前转换视频文件：{}'.format(videos_file_path))
    print('******************************* 视频提取音频开始 *******************************')
    t1 = time.time()
    video = mp.VideoFileClip(videos_file_path)
    video.audio.write_audiofile(audio_file_path)
    t2 = time.time()
    print('音频保存地址：{}'.format(audio_file_path))
    print('视频提取音频耗时：{}s'.format(t2-t1))
    return video

def cut_audio(input_path, output_dir, file_name, interval):
    print('******************************* 音频切割开始 *******************************')
    # 打开音频文件
    audio = AudioSegment.from_file(input_path, format='wav')

    # 计算总体时长
    duration = audio.duration_seconds
    print('源文件时长：{}s'.format(duration))
    
    # 开始切割并分开保存
    cnt = duration//interval + 1
    for i in range(int(cnt)):
        begin_time = i * interval * 1000
        end_time = (i+1) * interval * 1000
        frames = audio[begin_time:end_time]
        output_path = output_dir + file_name + '{0:03d}'.format(i) + '.wav'
        print(output_path)
        frames.export(output_path,format='wav')

def main():
    for i in range(len(filelist)):
#     for i in range(1):
        if filelist[i].endswith(".mp4"):
            print('\n当前进度 {}/{}'.format(i+1,len(filelist)))
            
            # 1 长视频分离出长音频
            long_video_path = long_video_dir + filelist[i]
            long_audio_path = long_audio_dir + filelist[i].replace('mp4','wav')
            extract_audio(long_video_path,long_audio_path)
            
            # 2 长音频切割成中等音频
            cut_audio(long_audio_path,raw_audio_dir,filelist[i].replace('.mp4',''),interval)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", default="600")
    args = parser.parse_args()
    interval = int(args.interval)
    main()
