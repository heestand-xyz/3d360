import os
from sys import argv
import tifffile
import numpy as np
import imageio

def main(srcDir):
	srcNames = sorted(os.listdir(srcDir))
	nr = 0
	for srcName in srcNames:
		nr += 1
		srcPath = os.path.join(srcDir, srcName)
		rgb = tifffile.imread(srcPath)
		if nr == 1:
			rgbMerge = rgb
		else:
			rgbMerge = np.concatenate((rgbMerge, rgb), axis=1)
		countLog = str(nr) + '/' + str(len(srcNames)) + ' >'
		print(countLog, srcName, 'merged')
	destPath = os.path.join(srcDir, '..', '3d360_merge.tif')
	imageio.imsave(destPath, rgbMerge)
	print('finished!')

if __name__ == "__main__":
	if len(argv) != 2:
		print('argument excepted:')
		print('[srcDir]')
	else:
		srcDir = argv[1]
		if not os.path.isdir(srcDir):
			print('srcDir, needs to be a valid dir')
		else:
			main(srcDir)