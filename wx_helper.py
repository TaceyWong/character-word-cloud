
from PIL import Image
import wx

def wx_scale_bitmap(bitmap, width, height):
    w,h = bitmap.Size
    if w==h:
        width=width
        height=height
    elif w>h:
        width=width
        height=int(width*h/w)
    else:
        height=height
        width=int(height*w/h)
    return bitmap.ConvertToImage().Scale(width, height, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()

def PIL2wx (image):
    """PIL图片转换为wxpython bitmap"""
    width, height = image.size
    return wx.BitmapFromBuffer(width, height, image.tobytes())

def wx2PIL (bitmap):
    """wxpython bitmap转换为PIL图片"""
    size = tuple(bitmap.GetSize())
    try:
        buf = size[0]*size[1]*3*"\x00"
        bitmap.CopyToBuffer(buf)
    except:
        del buf
        buf = bitmap.ConvertToImage().GetData()
    return Image.frombuffer("RGB", size, buf, "raw", "RGB", 0, 1)


# Suggested usage is to put the code in a separate file called
# helpers.py and use it as this:


# i = Image.open("someimage.jpg").convert("RGB")
# wxb = PIL2wx(i)
# Now draw wxb to screen and let user draw something over it using wxDC() and so on...
# Then pick a wx.Bitmap() from wx.DC() and do something like:
# wx2PIL(thedc.GetAsBitmap()).save("some new image.jpg")