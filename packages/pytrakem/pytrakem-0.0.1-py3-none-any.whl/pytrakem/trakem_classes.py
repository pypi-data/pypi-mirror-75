from jnius import autoclass

ElasticLayerAlignment = autoclass('mpicbg.trakem2.align.ElasticLayerAlignment')
AffineAlignment = autoclass('mpicbg.trakem2.align.RegularizedAffineLayerAlignment') 

Project = autoclass('ini.trakem2.Project')
Layer = autoclass('ini.trakem2.display.Layer')
ArrayList = autoclass('java.util.ArrayList')
Set = autoclass('java.util.HashSet')

Patch = autoclass('ini.trakem2.display.Patch')
Filter = autoclass('ini.trakem2.utils.Filter')
TemplateThing = autoclass('ini.trakem2.tree.TemplateThing')
FSLoader = autoclass('ini.trakem2.persistence.FSLoader')
Dataset = autoclass('net.imagej.Dataset')
AlignmentUtils = autoclass('mpicbg.trakem2.align.AlignmentUtils')
ImagePlus = autoclass('ij.ImagePlus')

ControlWindow = autoclass('ini.trakem2.ControlWindow')
ControlWindow.setGUIEnabled(False)

Display = autoclass('ini.trakem2.display.Display')
AffineTransformOp = autoclass('java.awt.image.AffineTransformOp')
BufferedImage = autoclass('java.awt.image.BufferedImage')
CoordinateTransformXML = autoclass('ini.trakem2.io.CoordinateTransformXML')

Point = autoclass('mpicbg.models.Point')
PointMatch = autoclass('mpicbg.models.PointMatch')