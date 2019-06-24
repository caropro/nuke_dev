import nuke
# by huoxiaodong 
# weibo.com/huoxiaodong
# 
toolbar = nuke.toolbar("Nodes")
m = toolbar.addMenu("HXD", "H.png")

#H_filter
m.addCommand("H_filter/H_EdgeSVMotionBlur", "nuke.createNode(\"H_EdgeSVMotionBlur\")", icon="H_EdgeSVMotionBlur")
m.addCommand("H_filter/H_EdgeVGMotionBlur", "nuke.createNode(\"H_EdgeVGMotionBlur\")", icon="H_EdgeVGMotionBlur")


