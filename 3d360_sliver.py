import os
from sys import argv
from PIL import Image
import rawpy
import imageio
from shutil import copyfile

def sliver(pixCount, raw, destPath):
	rawpyPars = rawpy.Params(output_bps=16)
	rgb = raw.postprocess(params=rawpyPars)
	w = rgb.shape[1]
	rgbSliver = rgb[:,w / 2 - pixCount / 2:w / 2 + pixCount / 2,:]
	imageio.imsave(destPath, rgbSliver)

def main(pixCount, srcDir, destDir):
	srcNames = os.listdir(srcDir)
	nr = 0
	for srcName in srcNames:
		nr += 1
		countLog = str(nr) + '/' + str(len(srcNames)) + ' >'
		srcPath = os.path.join(srcDir, srcName)
		destName = srcName.split('.')[0] + '_slice' + str(pixCount) + '.tif'
		destPath = os.path.join(destDir, destName)
		if os.path.isfile(destPath):
			#print(countLog, destName, 'already processed')
			continue
		try:
			# srcExt = srcName.split('.')[-1]
			# print('ext', ']'+srcExt+'[', srcExt in ['png', 'jpg', 'tif'])
			# if srcExt in ['png', 'jpg', 'tif']:
			# 	print('x', srcPath)
			# 	try:
			# 		img = Image.open(srcPath)
			# 	except:
			# 		raw = None
			# 	print('y')
			# 	return #<<
			# elif srcExt in ['nef', 'cr2', 'dng']:
			# 	try:
			# 		raw = rawpy.imread(srcPath)
			# 	except:
			# 		raw = None
			# else:
			# 	print(countLog, srcName, 'file format not supported')
			# 	continue
			# return #<<
			raw = rawpy.imread(srcPath)
		except:
			raw = None
		if raw:
			print(countLog, srcName)
			sliver(pixCount, raw, destPath)
		else:
			corruptDir = os.path.join(srcDir, '../corrupt')
			if not os.path.isdir(corruptDir):
				os.makedirs(corruptDir)
			corruptPath = os.path.join(corruptDir, srcName)
			if not os.path.exists(corruptPath):
				copyfile(srcPath, corruptPath)
				print(countLog, srcName, 'rawpy import faild, copied to "corrupt" dir')
			else:
				convertedName = srcName.split('.')[0] + '.dng'
				convertedPath = os.path.join(corruptDir, convertedName)
				if not os.path.exists(convertedPath):
					print(countLog, srcName, 'is corrupt, convert to .dng, leave in "corrupt" dir')
				else:
					try:
						raw = rawpy.imread(convertedPath)
					except:
						raw = None
					if raw:
						print(countLog, convertedName)
						sliver(pixCount, rawConverted, destPath)
					else:
						print(countLog, convertedName, 'found converted .dng, rawpy import faild, you`re screwed')
	print('finished!')

if __name__ == "__main__":
	if len(argv) != 4:
		print('3 arguments excepted:')
		print('[pixCount] [srcDir] [destDir]')
	else:
		pixCount = argv[1]
		if not pixCount.isdigit():
			print('first argument, pixCount, needs to be an integer')
		else:
			pixCount = int(pixCount)
			if pixCount < 2 or pixCount % 2:
				print('first argument, pixCount, needs to be an even number and above 1')
			else:
				srcDir = argv[2]
				if not os.path.isdir(srcDir):
					print('second argument, srcDir, needs to be a valid dir')
				else:
					destDir = argv[3]
					if not os.path.isdir(destDir):
						os.makedirs(destDir)
					main(pixCount, srcDir, destDir)