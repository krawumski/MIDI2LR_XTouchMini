from PyQt5.Qt import (
    QApplication, QImage, QImageWriter, Qt, QFont, QFontDatabase, QPainter, QPainterPath, QPoint, QTextLayout, QTextOption,
    QTextCharFormat, QColor, QRect, QRectF, QPen, QBrush, QTransform, QPolygon
)

###############################################################################
#
# Global definitions - Cheat image paramters
#
kImgW = 800
kImgH = 220
kColorBg = QColor(50, 50, 50)
kColorMd = QColor(90, 90, 90)
kColorFg = QColor(200, 200, 200)
kColorSl = QColor(200, 100, 0)
#
###############################################################################


###############################################################################
#
# Functions to write knob & button settings.
#
###############################################################################

def write_header (outFile):
    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", file=outFile)
    print("\n<!-- Generated MIDI2LR Profile for Behringer X-Touch Mini -->\n", file=outFile)
    print("<settings>", file=outFile)

def write_footer (outFile):
    print("</settings>", file=outFile)

# Write a single knob control definition. Two lines are written:
#  - A controller setting for the knob turning action
#  - A note setting for the knob push action to reset the parameter
#
def write_knob_setting (controllerNumber, noteNumber, commandString, outFile):
    print("    <setting channel=\"11\" controller=\""+str(controllerNumber)+"\" command_string=\""+commandString+"\"/>", file=outFile)
    print("    <setting channel=\"11\" note=\""+str(noteNumber)+"\" command_string=\"Reset"+commandString+"\"/>", file=outFile)

# Write a knob definition for layer A.
# controllerIndex   The controller postion (1-8)
#
def write_knob_a (controllerIndex, commandString, label, p, outFile, color=None):
    write_knob_setting(controllerIndex, controllerIndex-1, commandString, outFile)
    draw_cheat_knob(p, controllerIndex, label, color)


# Write a knob definition for layer B.
# controllerIndex   The controller postion (1-8)
#
def write_knob_b (controllerIndex, commandString, outFile):
    write_knob_setting(controllerIndex+10, controllerIndex+23, commandString, outFile)

# Write a knob definition for both layers A and B.
# controllerIndex   The controller postion (1-8)
#
def write_knob_ab (controllerIndex, commandString, outFile):
    write_knob_a(controllerIndex, commandString, outFile)
    write_knob_b(controllerIndex, commandString, outFile)

###############################################################################

# Write a single button control definition.
# noteNumber    The midi note number to assign the command to.
#
def write_button_setting (noteNumber, commandString, outFile):
    print("    <setting channel=\"11\" note=\""+str(noteNumber)+"\" command_string=\""+commandString+"\"/>", file=outFile)

# Write a single button definition for the upper button row in the A layer.
# buttonIndex   The button position (1-8)
#
def write_button_upper_a(buttonIndex, commandString, label, p, outFile):
    write_button_setting(buttonIndex+7, commandString, outFile)
    draw_cheat_button(p, 1, buttonIndex, label)

# Write a single button definition for the upper button row in the B layer.
# buttonIndex   The button position (1-8)
#
def write_button_upper_b(buttonIndex, commandString, outFile):
    write_button_setting(buttonIndex+31, commandString, outFile)

# Write a setting definition that assigns the same command to the same button
# in the upper button row for both A and B layers.
# buttonIndex   The button position (1-8)
#
def write_button_upper_ab(buttonIndex, commandString, label, p, outFile):
    write_button_upper_a(buttonIndex, commandString, label, p, outFile)
    write_button_upper_b(buttonIndex, commandString, outFile)
    # print("", file=outFile)

# Write a single button definition for the upper lower row in the A layer.
# buttonIndex   The button position (1-8)
#
def write_button_lower_a(buttonIndex, commandString, label, p, outFile):
    write_button_setting(buttonIndex+15, commandString, outFile)
    draw_cheat_button(p, 2, buttonIndex, label)

# Write a single button definition for the lower button row in the B layer.
# buttonIndex   The button position (1-8)
#
def write_button_lower_b(buttonIndex, commandString, outFile):
    write_button_setting(buttonIndex+39, commandString, outFile)

# Write a setting definition that assigns the same command to the same button
# in the lower button row for both A and B layers.
# buttonIndex   The button position (1-8)
#
def write_button_lower_ab (buttonIndex, commandString, label, p, outFile):
    write_button_lower_a(buttonIndex, commandString, label, p, outFile)
    write_button_lower_b(buttonIndex, commandString, outFile)
    # print("", file=outFile)

###############################################################################

# Write a single button setup definition.
# noteNumber    The midi note number to assign the command to.
# value         The note value (0 - dark, 1 - lit)
#
def write_button_setup (noteNumber, value, outFile):
    print("    <setup channel=\"11\" note=\""+str(noteNumber)+"\" value=\""+str(value)+"\"/>", file=outFile)

# Write a single button setup for the upper button row in the A layer.
# buttonIndex   The button position (1-8)
#
def write_button_setup_upper_a(buttonIndex, value, outFile):
    write_button_setup(buttonIndex+7, value, outFile)

# Write a single button definition for the upper button row in the B layer.
# buttonIndex   The button position (1-8)
#
def write_button_setup_upper_b(buttonIndex, value, outFile):
    write_button_setup(buttonIndex+31, value, outFile)

# Write a setup definition that assigns the same command to the same button
# in the upper button row for both A and B layers.
# buttonIndex   The button position (1-8)
#
def write_button_setup_upper_ab(buttonIndex, value, outFile):
    write_button_setup_upper_a(buttonIndex, value, outFile)
    write_button_setup_upper_b(buttonIndex, value, outFile)
    # print("", file=outFile)

# Write a single button setup for the upper lower row in the A layer.
# buttonIndex   The button position (1-8)
#
def write_button_setup_lower_a(buttonIndex, value, outFile):
    write_button_setup(buttonIndex+15, value, outFile)

# Write a single button setup for the lower button row in the B layer.
# buttonIndex   The button position (1-8)
#
def write_button_setup_lower_b(buttonIndex, value, outFile):
    write_button_setup(buttonIndex+39, value, outFile)

# Write a setup definition that assigns the same command to the same button
# in the lower button row for both A and B layers.
# buttonIndex   The button position (1-8)
#
def write_button_setup_lower_ab (buttonIndex, value, outFile):
    write_button_setup_lower_a(buttonIndex, value, outFile)
    write_button_setup_lower_b(buttonIndex, value, outFile)
    # print("", file=outFile)


###############################################################################
#
# Cheat image.
#
###############################################################################

def init_cheat_image ():
    return QImage(kImgW, kImgH, QImage.Format_ARGB32)

def init_cheat_painting (img):
    p = QPainter(img)
    p.setRenderHint(QPainter.Antialiasing)

    rect = QRect(0, 0, img.width(), img.height())

    p.fillRect(rect, kColorBg)

    return p

def draw_cheat_knob (p, col, txt, color=None):
    bxWidth  = kImgW/8
    bxHeight = kImgH*0.4

    # Channel number
    r = bxWidth*0.09
    c = QPoint(bxWidth*(col-1)+r*1.5, r*1.5)
    p.setPen(QPen(kColorMd, 0))
    p.setBrush(kColorMd)
    p.drawEllipse(c, r, r)

    p.setFont(QFont("Source Sans Pro", 10, QFont.DemiBold))
    p.setPen(kColorBg)
    p.drawText(QRect(c.x()-r, c.y()-r, r*2, r*2), Qt.AlignHCenter, str(col))

    # Knob
    if (txt != ""):
        p.setPen(QPen(kColorMd, 3))
    else:
        p.setPen(QPen(kColorMd, 1))
    p.setBrush(Qt.NoBrush)

    c = QPoint(bxWidth*col-bxWidth/2, bxHeight*0.35)
    r = bxHeight * 0.12
    p.drawEllipse(c, r, r)
    p.setPen(QPen(kColorMd, 1))
    p.drawEllipse(c, r*1.9, r*1.9)

    if (color != None):
        p.setPen(QPen(kColorMd, 0))
        p.setBrush(color)
        p.drawEllipse(c, r, r)
        p.setBrush(Qt.NoBrush)

    p.setFont(QFont("Source Sans Pro", 11, QFont.DemiBold))
    p.setPen(kColorFg)
    p.drawText(QRect(bxWidth*(col-1), bxHeight*0.6, bxWidth, bxHeight*0.3), Qt.AlignHCenter, txt.upper())


def draw_cheat_button (p, row, col, txt, isSelected=0):

    bxOff    = kImgH*0.4
    bxWidth  = kImgW/8
    bxHeight = (kImgH-bxOff)/2
    btWidth  = bxWidth*0.35
    btHeight = bxHeight*0.4
    btX = bxWidth*col-bxWidth/2-btWidth/2
    btY = bxOff+bxHeight*row-bxHeight/2-btHeight/2-bxHeight*0.15

    path = QPainterPath()
    path.addRoundedRect(QRectF(btX, btY, btWidth, btHeight), 5, 5)

    if (txt != ""):
        p.setPen(QPen(kColorMd, 3))
    else:
        p.setPen(QPen(kColorMd, 1))
    p.setBrush(Qt.NoBrush)
    p.drawPath(path)

    p.setFont(QFont("Source Sans Pro", 11, QFont.DemiBold))
    p.setPen(kColorFg)
    p.drawText(QRect(bxWidth*(col-1), btY+btHeight*1.2, bxWidth, bxHeight*0.3), Qt.AlignHCenter, txt.upper())

    if (isSelected):
        p.setPen(QPen(kColorMd, 3))
        p.setBrush(QBrush(kColorSl))
        p.drawPath(path)

    #p.drawRect(bxWidth*(col-1), bxOff+bxHeight*(row-1), bxWidth, bxHeight)

def draw_cheat_knob_group (p, colA, colB, txt):
    rArc  = 12
    posY  = kImgH*0.34
    posXA = kImgW/8*(colA-1)+4
    posXB = kImgW/8*(colB)-4
    len   = posXB-posXA

    p.setPen(QPen(kColorMd, 2))
    p.drawLine(posXA+rArc-4, posY, posXB-rArc+4, posY)
    p.drawArc(posXA, posY-rArc, rArc, rArc, 180*16, 90*16)
    p.drawArc(posXB-rArc, posY-rArc, rArc, rArc, 270*16, 90*16)

    p.drawText(QRect(posXA, posY+1, len, 16), Qt.AlignHCenter, txt.upper())


def write_cheat_image (p, img, fileName):
    p.end()

    writer = QImageWriter(fileName)
    writer.write(img)


###############################################################################
#
# Global assignment blocks (navigation).
#
###############################################################################

def write_global_nav_setup (activeItem, outFile):
    print ("\n    <!-- Global Navigation Setup -->\n", file=outFile)
    
    for index in range (1, 8):
        value = 0
        if (index == activeItem):
            value = 1

        write_button_setup_lower_ab(index, value, outFile)

def write_submenu_setup (activeItem, outFile):
    print ("\n    <!-- Submenu Navigation Setup -->\n", file=outFile)
    
    for index in range (1, 6):
        value = 0
        if (index == activeItem):
            value = 1

        write_button_setup_upper_ab(index, value, outFile)

# Submenu in upper key row for Basic mode
#
def write_nav_basic (sel, p, outFile):
    print ("\n    <!-- Basic Profile Sub-Navigation -->\n", file=outFile)
    write_button_upper_ab(1, "RevealPanelLens", "Lens", p, outFile)
    write_button_upper_ab(2, "ActionSeries4", "Transform", p, outFile)
    write_button_upper_ab(3, "CropOverlay", "Crop", p, outFile)
    draw_cheat_button(p, 1, 4, "")
    draw_cheat_button(p, 1, 5, "")
    draw_cheat_button(p, 1, 6, "")
    draw_cheat_button(p, 1, sel, "", 1)

def write_nav_colors_1 (sel, p, outFile):
    print ("\n    <!-- Colors 1 Profile Sub-Navigation -->\n", file=outFile)
    write_button_upper_ab(1, "ActionSeries2", "Tone", p, outFile)
    write_button_upper_ab(2, "ActionSeries3", "Presence", p, outFile)
    write_button_upper_ab(3, "GraduatedFilter", "Gradient", p, outFile)
    write_button_upper_ab(4, "AdjustmentBrush", "Brush", p, outFile)
    write_button_upper_ab(5, "RevealPanelTone", "Tone Curve", p, outFile)
    draw_cheat_button(p, 1, 6, "")
    draw_cheat_button(p, 1, sel, "", 1)

def write_nav_colors_2 (sel, p, outFile):
    print ("\n    <!-- Colors 2 Profile Sub-Navigation -->\n", file=outFile)
    write_button_upper_ab(1, "ActionSeries5", "Hue", p, outFile)
    write_button_upper_ab(2, "ActionSeries6", "Saturation", p, outFile)
    write_button_upper_ab(3, "ActionSeries7", "Luminance", p, outFile)
    draw_cheat_button(p, 1, 4, "")
    draw_cheat_button(p, 1, 5, "")
    draw_cheat_button(p, 1, 6, "")
    draw_cheat_button(p, 1, sel, "", 1)

def write_nav_enhance (sel, p, outFile):
    print ("\n    <!-- Enhance Profile Sub-Navigation -->\n", file=outFile)
    write_button_upper_ab(1, "RevealPanelEffects", "Effects", p, outFile)
    write_button_upper_ab(2, "RevealPanelDetail", "Detail", p, outFile)
    draw_cheat_button(p, 1, 3, "")
    draw_cheat_button(p, 1, 4, "")
    draw_cheat_button(p, 1, 5, "")
    draw_cheat_button(p, 1, 6, "")
    draw_cheat_button(p, 1, sel, "", 1)

def write_nav_grading (sel, p, outFile):
    print ("\n    <!-- Grading Profile Sub-Navigation -->\n", file=outFile)
    write_button_upper_ab(1, "ActionSeries9", "Midtones", p, outFile)
    write_button_upper_ab(2, "ActionSeries10", "Highlights", p, outFile)
    write_button_upper_ab(3, "ActionSeries11", "Shadows", p, outFile)
    write_button_upper_ab(4, "ActionSeries12", "Global", p, outFile)
    draw_cheat_button(p, 1, 5, "")
    draw_cheat_button(p, 1, 6, "")
    draw_cheat_button(p, 1, sel, "", 1)


def write_global_nav_keys (sel, p, outFile):
    print ("\n    <!-- Global Navigation -->\n", file=outFile)

    write_button_upper_ab(7, "Key3", "Before/After", p, outFile)
    write_button_upper_ab(8, "Key1", "Clipping", p, outFile)
    write_button_lower_ab(1, "ActionSeries1", "Library", p, outFile)
    write_button_lower_ab(2, "RevealPanelLens", "Basic", p, outFile)
    write_button_lower_ab(3, "ActionSeries2", "Colours 1", p, outFile)
    write_button_lower_ab(4, "ActionSeries5", "Colours 2", p, outFile)
    write_button_lower_ab(5, "ActionSeries8", "Grayscale", p, outFile)
    write_button_lower_ab(6, "RevealPanelEffects", "Enhance", p, outFile)
    write_button_lower_ab(7, "ActionSeries9", "Grading", p, outFile)
    write_button_lower_ab(8, "ToggleZoomOffOn", "Zoom", p, outFile)
    draw_cheat_button(p, 2, sel, "", 1)



###############################################################################
#
# Functions to write profile files.
#
###############################################################################

# Library

def write_profile_library ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Library.xml", "w") as outFile:
        write_header(outFile)

        write_global_nav_setup(1, outFile)
        write_submenu_setup(0, outFile)

        for k in range(1,9):
            draw_cheat_knob(p, k, "")

        write_button_upper_a(1, "Pick", "Flag", p, outFile)
        write_button_upper_a(2, "Reject", "Reject", p, outFile)
        write_button_upper_a(3, "RemoveFlag", "Clear", p, outFile)
        write_button_upper_a(4, "AddOrRemoveFromTargetColl", "Target", p, outFile)
        draw_cheat_button(p, 1, 5, "")
        draw_cheat_button(p, 1, 6, "")
        
        write_global_nav_keys(1, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Library.png")


# Basic Profiles



def write_profile_lens ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Lens.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(1, outFile)
        write_global_nav_setup(2, outFile)

        write_knob_a(1, "LensManualDistortionAmount", "Distortion", p, outFile)
        write_knob_a(2, "DefringePurpleAmount", "Amount", p, outFile, QColor(90, 0, 180))
        write_knob_a(3, "DefringePurpleHueLo", "Hue Lo", p, outFile, QColor(90, 0, 180))
        write_knob_a(4, "DefringePurpleHueHi", "Hue Hi", p, outFile, QColor(90, 0, 180))
        draw_cheat_knob_group(p, 2, 4, "Purple")
        write_knob_a(5, "DefringeGreenAmount", "Amount", p, outFile, QColor(0, 150, 0))
        write_knob_a(6, "DefringeGreenHueLo", "Hue Lo", p, outFile, QColor(0, 150, 0))
        write_knob_a(7, "DefringeGreenHueHi", "Hue Hi", p, outFile, QColor(0, 150, 0))
        draw_cheat_knob_group(p, 5, 7, "Green")
        draw_cheat_knob(p, 8, "")

        write_button_upper_a(6, "EnableLensCorrections", "On/Off", p, outFile)

        write_nav_basic(1, p, outFile)
        write_global_nav_keys(2, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Lens.png")


def write_profile_transform ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Transform.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(2, outFile)
        write_global_nav_setup(2, outFile)

        write_knob_a(1, "PerspectiveVertical", "Vertical", p, outFile)
        write_knob_a(2, "PerspectiveHorizontal", "Horizontal", p, outFile)
        write_knob_a(3, "PerspectiveRotate", "Rotate", p, outFile)
        write_knob_a(4, "PerspectiveScale", "Scale", p, outFile)
        write_knob_a(5, "PerspectiveX", "Offset X", p, outFile)
        write_knob_a(6, "PerspectiveY", "Offset Y", p, outFile)
        draw_cheat_knob(p, 7, "")
        draw_cheat_knob(p, 8, "")

        write_button_upper_a(5, "CropConstrainToWarp", "Crop", p, outFile)
        write_button_upper_a(6, "EnableTransform", "On/Off", p, outFile)

        write_nav_basic(2, p, outFile)
        write_global_nav_keys(2, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Transform.png")

def write_profile_crop ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Crop.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(3, outFile)
        write_global_nav_setup(2, outFile)

        write_knob_a(1, "CropTop", "Top", p, outFile)
        write_knob_a(2, "CropLeft", "Left", p, outFile)
        write_knob_a(3, "CropRight", "Right", p, outFile)
        write_knob_a(4, "CropBottom", "Bottom", p, outFile)
        write_knob_a(5, "straightenAngle", "Angle", p, outFile)
        draw_cheat_knob(p, 6, "")
        draw_cheat_knob(p, 7, "")
        draw_cheat_knob(p, 8, "")

        # Keyboard shortcut definition 2: l - lights out
        write_button_upper_a(6, "Key2", "Lights Out", p, outFile)

        write_nav_basic(3, p, outFile)
        write_global_nav_keys(2, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Crop.png")

# Colors 1 Profiles

def write_profile_tone ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Tone.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(1, outFile)
        write_global_nav_setup(3, outFile)

        write_knob_a(1, "Whites", "Whites", p, outFile, QColor(200, 200, 200))
        write_knob_a(2, "Highlights", "Highlights", p, outFile, QColor(160, 160, 160))
        write_knob_a(3, "Shadows", "Shadows", p, outFile, QColor(80, 80, 80))
        write_knob_a(4, "Blacks", "Blacks", p, outFile, QColor(30, 30, 30))
        draw_cheat_knob_group(p, 1, 4, "")
        write_knob_a(5, "Temperature", "Temp", p, outFile)
        write_knob_a(6, "Tint", "Tint", p, outFile)
        draw_cheat_knob_group(p, 5, 6, "WB")
        write_knob_a(7, "Exposure", "Exposure", p, outFile)
        write_knob_a(8, "Contrast", "Contrast", p, outFile)

        print("", file=outFile)

        write_nav_colors_1(1, p, outFile)
        write_global_nav_keys(3, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Tone.png")

def write_profile_presence ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Presence.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(2, outFile)
        write_global_nav_setup(3, outFile)

        write_knob_a(1, "Texture", "Texture", p, outFile)
        write_knob_a(2, "Clarity", "Clarity", p, outFile)
        write_knob_a(3, "Dehaze", "Dehaze", p, outFile)
        write_knob_a(4, "Vibrance", "Vibrance", p, outFile)
        write_knob_a(5, "Saturation", "Saturation", p, outFile)
        draw_cheat_knob(p, 6, "")
        draw_cheat_knob(p, 7, "")
        draw_cheat_knob(p, 8, "")

        write_nav_colors_1(2, p, outFile)
        write_global_nav_keys(3, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Presence.png")

def write_profile_gradient ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Gradient.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(3, outFile)
        write_global_nav_setup(3, outFile)

        write_knob_a(1, "local_Exposure", "Exposure", p, outFile)
        write_knob_a(2, "local_Contrast", "Contrast", p, outFile)
        write_knob_a(3, "local_Highlights", "Highlights", p, outFile)
        write_knob_a(4, "local_Shadows", "Shadows", p, outFile)
        write_knob_a(5, "local_Whites2012", "Whites", p, outFile)
        write_knob_a(6, "local_Blacks2012", "Blacks", p, outFile)
        write_knob_a(7, "local_Clarity", "Clarity", p, outFile)
        write_knob_a(8, "local_Dehaze", "Dehaze", p, outFile)

        write_knob_b(1, "local_Temperature", outFile)
        write_knob_b(2, "local_Tint", outFile)
        # local_Vibrance does not exist
        write_knob_b(4, "local_Saturation", outFile)
        write_knob_b(5, "local_Sharpness", outFile)
        write_knob_b(6, "local_LuminanceNoise", outFile)
        write_knob_b(7, "local_Moire", outFile)
        write_knob_b(8, "local_Defringe", outFile)

        write_button_upper_ab(6, "EnableGradientBasedCorrections", "On/Off", p, outFile)

        write_nav_colors_1(3, p, outFile)
        write_global_nav_keys(3, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Gradient.png")

def write_profile_brush ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Brush.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(4, outFile)
        write_global_nav_setup(3, outFile)

        write_knob_a(1, "local_Exposure", "Exposure", p, outFile)
        write_knob_a(2, "local_Contrast", "Contrast", p, outFile)
        write_knob_a(3, "local_Highlights", "Highlights", p, outFile)
        write_knob_a(4, "local_Shadows", "Shadows", p, outFile)
        write_knob_a(5, "local_Whites2012", "Whites", p, outFile)
        write_knob_a(6, "local_Blacks2012", "Blacks", p, outFile)
        write_knob_a(7, "local_Clarity", "Clarity", p, outFile)
        write_knob_a(8, "local_Dehaze", "Dehaze", p, outFile)

        write_knob_b(1, "local_Temperature", outFile)
        write_knob_b(2, "local_Tint", outFile)
        # local_Vibrance does not exist
        write_knob_b(4, "local_Saturation", outFile)
        write_knob_b(5, "local_Sharpness", outFile)
        write_knob_b(6, "local_LuminanceNoise", outFile)
        write_knob_b(7, "ChangeFeatherSize", outFile)
        write_knob_b(8, "ChangeBrushSize", outFile)

        write_button_upper_ab(6, "EnablePaintBasedCorrections", "On/Off", p, outFile)

        write_nav_colors_1(4, p, outFile)
        write_global_nav_keys(3, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Brush.png")

def write_profile_tone_curve ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("ToneCurve.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(5, outFile)
        write_global_nav_setup(3, outFile)

        write_knob_a(1, "ParametricHighlights", "Highlights", p, outFile, QColor(200, 200, 200))
        write_knob_a(2, "ParametricLights", "Lights", p, outFile, QColor(160, 160, 160))
        write_knob_a(3, "ParametricDarks", "Darks", p, outFile, QColor(80, 80, 80))
        write_knob_a(4, "ParametricShadows", "Shadows", p, outFile, QColor(30, 30, 30))
        draw_cheat_knob_group(p, 1, 4, "")
        write_knob_a(5, "ParametricHighlightSplit", "Split High", p, outFile, QColor(160, 160, 160))
        write_knob_a(6, "ParametricMidtoneSplit", "Split Mid", p, outFile, QColor(80, 80, 80))
        write_knob_a(7, "ParametricShadowSplit", "Split Low", p, outFile, QColor(30, 30, 30))
        draw_cheat_knob_group(p, 5, 7, "")
        draw_cheat_knob(p, 8, "")

        write_button_upper_ab(6, "EnableToneCurve", "On/Off", p, outFile)

        write_nav_colors_1(5, p, outFile)
        write_global_nav_keys(3, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./ToneCurve.png")

# Colors 2 Profiles

def write_profile_colors_hue ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Colors-Hue.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(1, outFile)
        write_global_nav_setup(4, outFile)

        write_knob_a(1, "HueAdjustmentRed", "Red", p, outFile, QColor(200,0,0))
        write_knob_a(2, "HueAdjustmentOrange", "Orange", p, outFile, QColor(200,100,0))
        write_knob_a(3, "HueAdjustmentYellow", "Yellow", p, outFile, QColor(220,200,32))
        write_knob_a(4, "HueAdjustmentGreen", "Green", p, outFile, QColor(0, 200, 0))
        write_knob_a(5, "HueAdjustmentAqua", "Aqua", p, outFile, QColor(0, 200, 200))
        write_knob_a(6, "HueAdjustmentBlue", "Blue", p, outFile, QColor(0, 0, 200))
        write_knob_a(7, "HueAdjustmentPurple", "Purple", p, outFile, QColor(120, 0, 240))
        write_knob_a(8, "HueAdjustmentMagenta", "Magenta", p, outFile, QColor(190, 0, 210))

        write_button_upper_ab(6, "EnableColorAdjustments", "On/Off", p, outFile)

        write_nav_colors_2(1, p, outFile)
        write_global_nav_keys(4, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Colors-Hue.png")

def write_profile_colors_saturation ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Colors-Saturation.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(2, outFile)
        write_global_nav_setup(4, outFile)

        write_knob_a(1, "SaturationAdjustmentRed", "Red", p, outFile, QColor(200,0,0))
        write_knob_a(2, "SaturationAdjustmentOrange", "Orange", p, outFile, QColor(200,100,0))
        write_knob_a(3, "SaturationAdjustmentYellow", "Yellow", p, outFile, QColor(220,200,32))
        write_knob_a(4, "SaturationAdjustmentGreen", "Green", p, outFile, QColor(0, 200, 0))
        write_knob_a(5, "SaturationAdjustmentAqua", "Aqua", p, outFile, QColor(0, 200, 200))
        write_knob_a(6, "SaturationAdjustmentBlue", "Blue", p, outFile, QColor(0, 0, 200))
        write_knob_a(7, "SaturationAdjustmentPurple", "Purple", p, outFile, QColor(120, 0, 240))
        write_knob_a(8, "SaturationAdjustmentMagenta", "Magenta", p, outFile, QColor(190, 0, 210))

        write_button_upper_ab(6, "EnableColorAdjustments", "On/Off", p, outFile)

        write_nav_colors_2(2, p, outFile)
        write_global_nav_keys(4, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Colors-Saturation.png")

def write_profile_colors_luminance ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Colors-Luminance.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(3, outFile)
        write_global_nav_setup(4, outFile)

        write_knob_a(1, "LuminanceAdjustmentRed", "Red", p, outFile, QColor(200,0,0))
        write_knob_a(2, "LuminanceAdjustmentOrange", "Orange", p, outFile, QColor(200,100,0))
        write_knob_a(3, "LuminanceAdjustmentYellow", "Yellow", p, outFile, QColor(220,200,32))
        write_knob_a(4, "LuminanceAdjustmentGreen", "Green", p, outFile, QColor(0, 200, 0))
        write_knob_a(5, "LuminanceAdjustmentAqua", "Aqua", p, outFile, QColor(0, 200, 200))
        write_knob_a(6, "LuminanceAdjustmentBlue", "Blue", p, outFile, QColor(0, 0, 200))
        write_knob_a(7, "LuminanceAdjustmentPurple", "Purple", p, outFile, QColor(120, 0, 240))
        write_knob_a(8, "LuminanceAdjustmentMagenta", "Magenta", p, outFile, QColor(190, 0, 210))

        write_button_upper_ab(6, "EnableColorAdjustments", "On/Off", p, outFile)

        write_nav_colors_2(3, p, outFile)
        write_global_nav_keys(4, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Colors-Luminance.png")

def write_profile_colors_gray ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Grayscale.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(0, outFile)
        write_global_nav_setup(5, outFile)

        write_knob_a(1, "GrayMixerRed", "Red", p, outFile, QColor(200,0,0))
        write_knob_a(2, "GrayMixerOrange", "Orange", p, outFile, QColor(200,100,0))
        write_knob_a(3, "GrayMixerYellow", "Yellow", p, outFile, QColor(220,200,32))
        write_knob_a(4, "GrayMixerGreen", "Green", p, outFile, QColor(0, 200, 0))
        write_knob_a(5, "GrayMixerAqua", "Aqua", p, outFile, QColor(0, 200, 200))
        write_knob_a(6, "GrayMixerBlue", "Blue", p, outFile, QColor(0, 0, 200))
        write_knob_a(7, "GrayMixerPurple", "Purple", p, outFile, QColor(120, 0, 240))
        write_knob_a(8, "GrayMixerMagenta", "Magenta", p, outFile, QColor(190, 0, 210))

        for k in range(1, 7):
            draw_cheat_button(p, 1, k, "")

        write_button_upper_ab(6, "EnableGrayscaleMix", "On/Off", p, outFile)

        write_global_nav_keys(5, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Grayscale.png")

# Effects Profile

def write_profile_effects ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Effects.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(1, outFile)
        write_global_nav_setup(6, outFile)

        colVig = QColor(120, 120, 120)
        colGrn = QColor(80, 80, 80)

        write_knob_a(1, "PostCropVignetteAmount", "Amount", p, outFile, colVig)
        write_knob_a(2, "PostCropVignetteMidpoint", "Midpoint", p, outFile, colVig)
        write_knob_a(3, "PostCropVignetteRoundness", "Roundness", p, outFile, colVig)
        write_knob_a(4, "PostCropVignetteFeather", "Feather", p, outFile, colVig)
        draw_cheat_knob_group(p, 1, 4, "Vignette")
        write_knob_a(5, "GrainAmount", "Amount", p, outFile, colGrn)
        write_knob_a(6, "GrainSize", "Size", p, outFile, colGrn)
        write_knob_a(7, "GrainFrequency", "Frequency", p, outFile, colGrn)
        draw_cheat_knob_group(p, 5, 7, "Grain")
        draw_cheat_knob(p, 8, "")

        write_button_upper_ab(6, "EnableEffects", "On/Off", p, outFile)

        write_nav_enhance(1, p, outFile)
        write_global_nav_keys(6, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Effects.png")

def write_profile_detail ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Detail.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(2, outFile)
        write_global_nav_setup(6, outFile)

        colShp = QColor(120, 120, 120)
        colLum = QColor(80, 80, 80)

        write_knob_a(1, "Sharpness", "Sharpness", p, outFile, colShp)
        write_knob_a(2, "SharpenRadius", "Radius", p, outFile, colShp)
        write_knob_a(3, "SharpenDetail", "Detail", p, outFile, colShp)
        write_knob_a(4, "SharpenEdgeMasking", "Edge", p, outFile, colShp)
        draw_cheat_knob_group(p, 1, 4, "Sharpen")
        write_knob_a(5, "LuminanceSmoothing", "Smoothing", p, outFile, colLum)
        write_knob_a(6, "LuminanceNoiseReductionDetail", "Noise Det", p, outFile, colLum)
        write_knob_a(7, "LuminanceNoiseReductionContrast", "Noise Cont", p, outFile, colLum)
        draw_cheat_knob_group(p, 5, 7, "Luminance")
        draw_cheat_knob(p, 8, "")

        write_button_upper_ab(6, "EnableDetail", "On/Off", p, outFile)

        write_nav_enhance(2, p, outFile)
        write_global_nav_keys(6, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Detail.png")


def write_profile_grading_mid ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Grading-Mid.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(1, outFile)
        write_global_nav_setup(7, outFile)

        write_knob_a(1, "ColorGradeMidtoneHue", "Hue", p, outFile, QColor(60, 60, 60))
        write_knob_a(2, "ColorGradeMidtoneSat", "Saturation", p, outFile, QColor(60, 60, 60))
        write_knob_a(3, "ColorGradeMidtoneLum", "Luminance", p, outFile, QColor(60, 60, 60))
        draw_cheat_knob_group(p, 1, 3, "")
        write_knob_a(4, "ColorGradeBlending", "Blending", p, outFile)
        write_knob_a(5, "SplitToningBalance", "Balance", p, outFile)
        draw_cheat_knob_group(p, 4, 5, "Global")
        for k in range(6,9):
            draw_cheat_knob(p, k, "")

        write_button_upper_ab(6, "EnableColorGrading", "On/Off", p, outFile)

        write_nav_grading(1, p, outFile)
        write_global_nav_keys(7, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Grading-Mid.png")


def write_profile_grading_high ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Grading-High.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(2, outFile)
        write_global_nav_setup(7, outFile)

        write_knob_a(1, "SplitToningHighlightHue", "Hue", p, outFile, QColor(60, 60, 60))
        write_knob_a(2, "SplitToningHighlightSaturation", "Saturation", p, outFile, QColor(60, 60, 60))
        write_knob_a(3, "ColorGradeHighlightLum", "Luminance", p, outFile, QColor(60, 60, 60))
        draw_cheat_knob_group(p, 1, 3, "")
        write_knob_a(4, "ColorGradeBlending", "Blending", p, outFile)
        write_knob_a(5, "SplitToningBalance", "Balance", p, outFile)
        draw_cheat_knob_group(p, 4, 5, "Global")
        for k in range(6,9):
            draw_cheat_knob(p, k, "")

        write_button_upper_ab(6, "EnableColorGrading", "On/Off", p, outFile)

        write_nav_grading(2, p, outFile)
        write_global_nav_keys(7, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Grading-High.png")


def write_profile_grading_shadow ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Grading-Shadow.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(3, outFile)
        write_global_nav_setup(7, outFile)

        write_knob_a(1, "SplitToningShadowHue", "Hue", p, outFile, QColor(60, 60, 60))
        write_knob_a(2, "SplitToningShadowSaturation", "Saturation", p, outFile, QColor(60, 60, 60))
        write_knob_a(3, "ColorGradeShadowLum", "Luminance", p, outFile, QColor(60, 60, 60))
        draw_cheat_knob_group(p, 1, 3, "")
        write_knob_a(4, "ColorGradeBlending", "Blending", p, outFile)
        write_knob_a(5, "SplitToningBalance", "Balance", p, outFile)
        draw_cheat_knob_group(p, 4, 5, "Global")
        for k in range(6,9):
            draw_cheat_knob(p, k, "")

        write_button_upper_ab(6, "EnableColorGrading", "On/Off", p, outFile)

        write_nav_grading(3, p, outFile)
        write_global_nav_keys(7, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Grading-Shadow.png")

def write_profile_grading_global ():

    img = init_cheat_image()
    p   = init_cheat_painting(img)

    with open("Grading-Global.xml", "w") as outFile:
        write_header(outFile)

        write_submenu_setup(4, outFile)
        write_global_nav_setup(7, outFile)

        write_knob_a(1, "ColorGradeGlobalHue", "Hue", p, outFile, QColor(60, 60, 60))
        write_knob_a(2, "ColorGradeGlobalSat", "Saturation", p, outFile, QColor(60, 60, 60))
        write_knob_a(3, "ColorGradeGlobalLum", "Luminance", p, outFile, QColor(60, 60, 60))
        draw_cheat_knob_group(p, 1, 3, "")
        write_knob_a(4, "ColorGradeBlending", "Blending", p, outFile)
        write_knob_a(5, "SplitToningBalance", "Balance", p, outFile)
        draw_cheat_knob_group(p, 4, 5, "Global")
        for k in range(6,9):
            draw_cheat_knob(p, k, "")

        write_button_upper_ab(6, "EnableColorGrading", "On/Off", p, outFile)

        write_nav_grading(4, p, outFile)
        write_global_nav_keys(7, p, outFile)

        write_footer(outFile)
        write_cheat_image(p, img, "./Grading-Global.png")




###############################################################################
#
# Main
#
###############################################################################

app = QApplication(["-platform offscreen"])
QFontDatabase.addApplicationFont("./SourceSansPro-SemiBold.ttf")

write_profile_library()
write_profile_crop()
write_profile_transform()
write_profile_lens()

write_profile_tone()
write_profile_presence()
write_profile_gradient()
write_profile_brush()
write_profile_tone_curve()

write_profile_colors_hue()
write_profile_colors_saturation()
write_profile_colors_luminance()

write_profile_colors_gray()

write_profile_effects()
write_profile_detail()

write_profile_grading_mid()
write_profile_grading_high()
write_profile_grading_shadow()
write_profile_grading_global()
