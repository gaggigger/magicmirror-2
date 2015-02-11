#!/usr/bin/env python

import Image
import mysql.connector
import sqlconnection
import cStringIO
import newfaces as nf

# def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None, resample=Image.BICUBIC):
  # if (scale is None) and (center is None):
    # return image.rotate(angle=angle, resample=resample)
  # nx,ny = x,y = center
  # sx=sy=1.0
  # if new_center:
    # (nx,ny) = new_center
  # if scale:
    # (sx,sy) = (scale, scale)
  # cosine = math.cos(angle)
  # sine = math.sin(angle)
  # a = cosine/sx
  # b = sine/sx
  # c = x-nx*a-ny*b
  # d = -sine/sy
  # e = cosine/sy
  # f = y-nx*d-ny*e
  # return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=resample)

# def CropFace(image, eye_left=(0,0), eye_right=(0,0), offset_pct=(0.23,0.23), dest_sz = (70,70)):
  # # calculate offsets in original image
  # offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
  # offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
  # # get the direction
  # eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
  # # calc rotation angle in radians
  # rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
  # # distance between them
  # dist = Distance(eye_left, eye_right)
  # # calculate the reference eye-width
  # reference = dest_sz[0] - 2.0*offset_h
  # # scale factor
  # scale = float(dist)/float(reference)
  # # rotate original around the left eye
  # image = ScaleRotateTranslate(image, center=eye_left, angle=rotation)
  # # crop the rotated image
  # crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
  # crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
  # image = image.crop((int(crop_xy[0]), int(crop_xy[1]), int(crop_xy[0]+crop_size[0]), int(crop_xy[1]+crop_size[1])))
  # # resize it
  # image = image.resize(dest_sz, Image.ANTIALIAS)
  # return image
  
cnx = sqlconnection.connecttodb()

cursor = cnx.cursor(dictionary=True)
id = 2
query = ("SELECT id, lefteye_x, lefteye_y, righteye_x, righteye_y, imgdata, imgtype FROM images WHERE id = (%s)")
cursor.execute(query, (id,))
for row in cursor:
	file_like = cStringIO.StringIO(row["imgdata"])
	image = Image.open(file_like)
	image = nf.CropFace( image, eye_left=(row["lefteye_x"],row["lefteye_y"]), eye_right=(row["righteye_x"],row["righteye_y"]))
	image.show()
cursor.close()
cnx.close()

