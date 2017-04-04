#!/usr/bin/env python

import sys
import os
import subprocess
import cv2

CRF_VALUE = '18'

# h.264 profile
PROFILE = 'high'

# encoding speed:compression ratio
PRESET = 'veryslow'

FFMPEG_PATH = '/usr/local/bin/ffmpeg'


def encode(file, mvs_path):
    name = '../../' + file
    quality = [[3840, 1920], [1920, 960]]
    counter = 0
    f = open('output.txt', 'w')
    for q in quality:
        subprocess.call(['mkdir', '%d_%d' % (q[0],q[1])])
        os.chdir('%d_%d' % (q[0], q[1]))
        for i in xrange(0, 80):
            try:
                if i < 60:
                    time = '00:%d:%d' % (0, i)
                else:
                    time = '00:%d:%d' % (int(i / 60), i % 60)

		f.write('time: %s\n' % time)

                command = [FFMPEG_PATH, '-ss', time, '-i', name, '-t', '1',
                           '-c:v', 'libx264', '-x264opts', 'keyint=30:min-keyint=30:no-scenecut',
                           '-profile:v', PROFILE, '-crf', CRF_VALUE, '-vf', 'scale=%d:%d' % (q[0], q[1]), ]
                output = ['%d_sec.mp4' % i]
                command += output
                subprocess.call(command)

		mvs = '/home/chao/360tiling/videos/extract_mvs %d_sec.mp4 >> %d_sec_mvs.txt' % (i, i)
		process = subprocess.Popen(mvs, shell=True, stdout=subprocess.PIPE)
		process.wait()
		f.write('extract %d_sec_mvs : %d\n' % (i, process.returncode))

            finally:
                counter += 1
                f.write('encode %d process success!!\n' % counter)
                print "encode %d process success!!\n" % counter

        os.chdir('..')
    f.close()


if __name__ == "__main__":

    cwd = os.getcwd()
    mvs_path = 'cwd' + 'extract_mvs'
    for file in os.listdir(cwd):
	if file.split('.')[-1] == 'mp4':
	    subprocess.call(['mkdir', '%s' % file.split('.')[0]])
            os.chdir('%s' % file.split('.')[0])
            encode(file, mvs_path)
            os.chdir('..')
