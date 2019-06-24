#coding=utf-8
import nuke
# import renderFinished
import beforerender

nuke.addBeforeRender(beforerender.mkds)
# nuke.addAfterRender(renderFinished.notify_user)

