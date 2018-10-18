#coding=utf-8
import os
import nuke
def main():
    #----------------------------------------------------------------------
    current_path=nuke.root()["name"].getValue()
    filename=current_path.split("/")[-1].split(".")[0]
    step_root=current_path.split("nuke")[0]
    outname=filename+".%04d.tga"
    outpath=os.path.join(step_root,"osc",filename,outname).replace("\\",'/')
    #----------------------------------------------------------------------
    sourcepath=os.path.join(current_path.split("nuke")[0],"render").replace("\\","/")
    version_dir=max([x for x in os.listdir(sourcepath)])
    masterLayer=os.path.join(sourcepath,version_dir,"masterLayer").replace("\\","/")
    if os.path.exists(masterLayer):
        version_path=masterLayer
    else:
        version_path=os.path.join(sourcepath,version_dir).replace("\\","/")
    read_file=nuke.getFileNameList(version_path)[0]
    read_path=os.path.join(version_path,read_file).replace("\\","/")
    #----------------------------------------------------------------------
    dist_dir=current_path.split(filename)[0].replace("lighting","tracking")
    dist_file=max([x for x in os.listdir(dist_dir) if "tracking_dist" in x and "auto" not in x])
    dist_path=os.path.join(dist_dir,dist_file)
    #----------------------------------------------------------------------
    iplate_dir=step_root.split("lighting")[0].replace("3d","elements/iplate")
    src_version_dir=max([x for x in os.listdir(iplate_dir)])
    src_version_path=os.path.join(iplate_dir,src_version_dir).replace("\\","/")
    src_file=nuke.getFileNameList(src_version_path)[0]
    src_path=os.path.join(src_version_path,src_file).replace("\\","/")
    #----------------------------------------------------------------------
    fileread=nuke.createNode("Read")
    fileread['file'].fromUserText(read_path)
    fileread["xpos"].setValue(-64)
    fileread["ypos"].setValue(-1107)
    channels=list(set([x.split(".")[0] for x in fileread.channels()]))
    print fileread
    file=nuke.createNode("Dot")
    file["xpos"].setValue(-30)
    file["ypos"].setValue(-900)
    file.setInput(0,fileread)
    # ----------------------------------------------------------------------
    dda = False
    dia = False
    df = False
    dk = False
    dr = False
    sda = False
    sia = False
    sk = False
    sf = False
    sr = False
    em = False
    sss = False
    trans = False
    mov = False

    # diaj
    diaj = nuke.createNode("Dot")
    diaj["xpos"].setValue(-279)
    diaj["ypos"].setValue(-900)
    diaj.setInput(0, file)
    if "diffuse_direct_amb" in channels:
        dda = True
        # ddaj
        ddaj = nuke.createNode("Dot")
        ddaj["xpos"].setValue(-112)
        ddaj["ypos"].setValue(-900)
        ddaj.setInput(0, file)
        # diffuse_direct_amb
        diffuse_direct_amb = nuke.createNode("Shuffle")
        diffuse_direct_amb['in'].setValue("diffuse_direct_amb")
        diffuse_direct_amb['name'].setValue("diffuse_direct_amb")
        diffuse_direct_amb['xpos'].setValue(-146.0)
        diffuse_direct_amb['ypos'].setValue(-494.0)
        diffuse_direct_amb.setInput(0, ddaj)
    if "diffuse_indirect_amb" in channels:
        dia=True

        # diffuse_indirect_amb
        diffuse_indirect_amb = nuke.createNode("Shuffle")
        diffuse_indirect_amb['in'].setValue("diffuse_indirect_amb")
        diffuse_indirect_amb['name'].setValue("diffuse_indirect_amb")
        diffuse_indirect_amb['xpos'].setValue(-313.0)
        diffuse_indirect_amb['ypos'].setValue(-641.0)
        diffuse_indirect_amb.setInput(0, diaj)
    if dda or dia:
        # block_1
        bdn_1 = nuke.createNode("BackdropNode")
        bdn_1["xpos"].setValue(-350.0)
        bdn_1["ypos"].setValue(-683.0)
        bdn_1["bdheight"].setValue(240)
        bdn_1["bdwidth"].setValue(317)
        bdn_1["label"].setValue("amb_dif")
        bdn_1["note_font_size"].setValue(20)
        bdn_1["tile_color"].setValue(1129690623)
        # m1
        m1 = nuke.createNode("Merge2")
        if dda:
            m1.setInput(1, diffuse_direct_amb)
        if dia:
            m1.setInput(0, diffuse_indirect_amb)
        m1["operation"].setValue("plus")
        m1['xpos'].setValue(-313.0)
        m1['ypos'].setValue(-494.0)

    if "diffuse_fill" in channels:
        df = True
        # dfj
        dfj = nuke.createNode("Dot")
        dfj["xpos"].setValue(213)
        dfj["ypos"].setValue(-900)
        dfj.setInput(0, file)
        # diffuse_fill
        diffuse_fill = nuke.createNode("Shuffle")
        diffuse_fill['in'].setValue("diffuse_fill")
        diffuse_fill['name'].setValue("diffuse_fill")
        diffuse_fill.setInput(0, dfj)
        diffuse_fill['xpos'].setValue(179.0)
        diffuse_fill['ypos'].setValue(-610.0)
        # block_2
        bdn_2 = nuke.createNode("BackdropNode")
        bdn_2["xpos"].setValue(127.0)
        bdn_2["ypos"].setValue(-689)
        bdn_2["bdheight"].setValue(246)
        bdn_2["bdwidth"].setValue(166)
        bdn_2["label"].setValue("fill_dif")
        bdn_2["note_font_size"].setValue(20)
        bdn_2["tile_color"].setValue(14532120623)
    if "diffuse_key" in channels:
        dk = True
        # dkj
        dkj = nuke.createNode("Dot")
        dkj["xpos"].setValue(497)
        dkj["ypos"].setValue(-900)
        dkj.setInput(0, file)
        # diffuse_key
        diffuse_key = nuke.createNode("Shuffle")
        diffuse_key['in'].setValue("diffuse_key")
        diffuse_key['name'].setValue("diffuse_key")
        diffuse_key['xpos'].setValue(463.0)
        diffuse_key['ypos'].setValue(-613.0)
        diffuse_key.setInput(0, dkj)
        key_dot = nuke.createNode("Dot")
        key_dot.setInput(0, diffuse_key)
        key_dot['xpos'].setValue(497.0)
        key_dot['ypos'].setValue(-339.0)
        # block_3
        bdn_3 = nuke.createNode("BackdropNode")
        bdn_3["xpos"].setValue(430.0)
        bdn_3["ypos"].setValue(-689)
        bdn_3["bdheight"].setValue(246)
        bdn_3["bdwidth"].setValue(166)
        bdn_3["label"].setValue("key_dif")
        bdn_3["note_font_size"].setValue(20)
        bdn_3["tile_color"].setValue(1451560623)
    if "diffuse_rim" in channels:
        dr = True
        # drj
        drj = nuke.createNode("Dot")
        drj["xpos"].setValue(740)
        drj["ypos"].setValue(-900)
        drj.setInput(0, file)
        # diffuse_rim
        diffuse_rim = nuke.createNode("Shuffle")
        diffuse_rim['in'].setValue("diffuse_rim")
        diffuse_rim['name'].setValue("diffuse_rim")
        diffuse_rim.setInput(0, drj)
        diffuse_rim['xpos'].setValue(706.0)
        diffuse_rim['ypos'].setValue(-617.0)
        rim_dot = nuke.createNode("Dot")
        rim_dot.setInput(0, diffuse_rim)
        rim_dot['xpos'].setValue(740.0)
        rim_dot['ypos'].setValue(-339.0)
        # block_4
        bdn_4 = nuke.createNode("BackdropNode")
        bdn_4["xpos"].setValue(700.0)
        bdn_4["ypos"].setValue(-689)
        bdn_4["bdheight"].setValue(246)
        bdn_4["bdwidth"].setValue(166)
        bdn_4["label"].setValue("rim_dif")
        bdn_4["note_font_size"].setValue(20)
        bdn_4["tile_color"].setValue(11251560623)
    if df or dk or dr:
        # m2
        m2 = nuke.createNode("Merge2")
        if df:
            m2.setInput(0, diffuse_fill)
        if dk:
            m2.setInput(1, key_dot)
        if dr:
            m2.setInput(3, rim_dot)
        m2["operation"].setValue("plus")
        m2['xpos'].setValue(179.0)
        m2['ypos'].setValue(-343.0)
    if dia or dda or df or dk or dr:
        # diff_m
        diff_m = nuke.createNode("Merge2")
        if dia or dda:
            diff_m.setInput(0, m1)
        else:
            diff_m.setInput(0, file)
        if dk or df or dr:
            diff_m.setInput(1, m2)
        diff_m["operation"].setValue("plus")
        diff_m['xpos'].setValue(-313.0)
        diff_m['ypos'].setValue(-343.0)
    # ----------------------------------------------------------------------
    if "specular_direct_amb" in channels:
        sda = True
        # sdaj
        sdaj = nuke.createNode("Dot")
        sdaj["xpos"].setValue(137)
        sdaj["ypos"].setValue(-900)
        sdaj.setInput(0, file)
        # specular_direct_amb
        specular_direct_amb = nuke.createNode("Shuffle")
        specular_direct_amb['in'].setValue("specular_direct_amb")
        specular_direct_amb['name'].setValue("specular_direct_amb")
        specular_direct_amb.setInput(0, sdaj)
        specular_direct_amb['xpos'].setValue(103.0)
        specular_direct_amb['ypos'].setValue(-85.0)
    if "specular_indirect_amb" in channels:
        sia = True
        # specular_indirect_amb
        specular_indirect_amb = nuke.createNode("Shuffle")
        specular_indirect_amb['in'].setValue("specular_indirect_amb")
        specular_indirect_amb['name'].setValue("specular_indirect_amb")
        specular_indirect_amb.setInput(0, file)
        specular_indirect_amb['xpos'].setValue(-64.0)
        specular_indirect_amb['ypos'].setValue(-178.0)
    if sia or sda:
        # sp_m1
        sp_m1 = nuke.createNode("Merge2")
        if sda:
            sp_m1.setInput(0, specular_direct_amb)
        if sia:
            sp_m1.setInput(1, specular_indirect_amb)
        sp_m1["operation"].setValue("plus")
        sp_m1['xpos'].setValue(-64.0)
        sp_m1['ypos'].setValue(-85.0)
        # block_5
        bdn_5 = nuke.createNode("BackdropNode")
        bdn_5["xpos"].setValue(-106)
        bdn_5["ypos"].setValue(-241)
        bdn_5["bdheight"].setValue(219)
        bdn_5["bdwidth"].setValue(322)
        bdn_5["label"].setValue("amb_spc")
        bdn_5["note_font_size"].setValue(20)
        bdn_5["tile_color"].setValue(1125410623)
    if "specular_key" in channels:
        sk = True
        # skj
        skj = nuke.createNode("Dot")
        skj["xpos"].setValue(396)
        skj["ypos"].setValue(-900)
        skj.setInput(0, file)
        # specular_key
        specular_key = nuke.createNode("Shuffle")
        specular_key['in'].setValue("specular_key")
        specular_key['name'].setValue("specular_key")
        specular_key.setInput(0, skj)
        specular_key['xpos'].setValue(362.0)
        specular_key['ypos'].setValue(-170.0)
        # block_6
        bdn_6 = nuke.createNode("BackdropNode")
        bdn_6["xpos"].setValue(300)
        bdn_6["ypos"].setValue(-250)
        bdn_6["bdheight"].setValue(246)
        bdn_6["bdwidth"].setValue(166)
        bdn_6["label"].setValue("key_spc")
        bdn_6["note_font_size"].setValue(20)
        bdn_6["tile_color"].setValue(11112360623)

    if "specular_fill" in channels:
        sf = True
        # sfj
        sfj = nuke.createNode("Dot")
        sfj["xpos"].setValue(608)
        sfj["ypos"].setValue(-900)
        sfj.setInput(0, file)
        # specular_fill
        specular_fill = nuke.createNode("Shuffle")
        specular_fill['in'].setValue("specular_fill")
        specular_fill['name'].setValue("specular_fill")
        specular_fill.setInput(0, sfj)
        specular_fill['xpos'].setValue(574.0)
        specular_fill['ypos'].setValue(-173.0)
        specular_fill_dot = nuke.createNode("Dot")
        specular_fill_dot.setInput(0, specular_fill)
        specular_fill_dot['xpos'].setValue(608.0)
        specular_fill_dot['ypos'].setValue(47.0)
        # block_7
        bdn_7 = nuke.createNode("BackdropNode")
        bdn_7["xpos"].setValue(550)
        bdn_7["ypos"].setValue(-250)
        bdn_7["bdheight"].setValue(246)
        bdn_7["bdwidth"].setValue(166)
        bdn_7["label"].setValue("fill_spc")
        bdn_7["note_font_size"].setValue(20)
        bdn_7["tile_color"].setValue(11113211)
    if "specular_rim" in channels:
        sr = True
        # srj
        srj = nuke.createNode("Dot")
        srj["xpos"].setValue(836)
        srj["ypos"].setValue(-900)
        srj.setInput(0, file)
        # specular_rim
        specular_rim = nuke.createNode("Shuffle")
        specular_rim['in'].setValue("specular_rim")
        specular_rim['name'].setValue("specular_rim")
        specular_rim.setInput(0, srj)
        specular_rim['xpos'].setValue(802.0)
        specular_rim['ypos'].setValue(-177.0)
        specular_rim_dot = nuke.createNode("Dot")
        specular_rim_dot.setInput(0, specular_rim)
        specular_rim_dot['xpos'].setValue(836)
        specular_rim_dot['ypos'].setValue(47)
        # block_8
        bdn_8 = nuke.createNode("BackdropNode")
        bdn_8["xpos"].setValue(770)
        bdn_8["ypos"].setValue(-250)
        bdn_8["bdheight"].setValue(246)
        bdn_8["bdwidth"].setValue(166)
        bdn_8["label"].setValue("rim_spc")
        bdn_8["note_font_size"].setValue(20)
        bdn_8["tile_color"].setValue(23658749)

    if sf or sk or sr:
        # sp_m2
        sp_m2 = nuke.createNode("Merge2")
        if sf:
            sp_m2.setInput(0, specular_fill_dot)
        if sk:
            sp_m2.setInput(1, specular_key)
        if sr:
            sp_m2.setInput(3, specular_rim_dot)
        sp_m2["operation"].setValue("plus")
        sp_m2['xpos'].setValue(362)
        sp_m2['ypos'].setValue(43)

    if sf or sk or sr or sda or sia:
        # sp_m3
        sp_m3 = nuke.createNode("Merge2")
        if sf or sk or sr:
            sp_m3.setInput(0, sp_m2)
        if sda or sia:
            sp_m3.setInput(1, sp_m1)
        sp_m3["operation"].setValue("plus")
        sp_m3['xpos'].setValue(-64)
        sp_m3['ypos'].setValue(43)
        # sp_diff
        sp_diff = nuke.createNode("Merge2")
        if dia or dda or df or dk or dr:
            sp_diff.setInput(0, diff_m)
        else:
            sp_diff.setInput(0, file)
        sp_diff.setInput(1, sp_m3)
        sp_diff["operation"].setValue("plus")
        sp_diff['xpos'].setValue(-313)
        sp_diff['ypos'].setValue(43)
    # ----------------------------------------------------------------------
    if "emission" in channels:
        em = True
        # emission
        emission = nuke.createNode("Shuffle")
        emission['in'].setValue("emission")
        emission['name'].setValue("emission")
        emission.setInput(0, file)
        emission['xpos'].setValue(-64)
        emission['ypos'].setValue(179)
        # block_9
        bdn_9 = nuke.createNode("BackdropNode")
        bdn_9["xpos"].setValue(-150)
        bdn_9["ypos"].setValue(125)
        bdn_9["bdheight"].setValue(100)
        bdn_9["bdwidth"].setValue(200)
        bdn_9["label"].setValue("emission")
        bdn_9["note_font_size"].setValue(20)
        bdn_9["tile_color"].setValue(2313238749)
        # emi_m
        emi_m = nuke.createNode("Merge2")
        if sf or sk or sr or sda or sia:
            emi_m.setInput(0, sp_diff)
        elif dia or dda or df or dk or dr:
            emi_m.setInput(0, diff_m)
        else:
            emi_m.setInput(0, file)
        emi_m.setInput(1, emission)
        emi_m["operation"].setValue("plus")
        emi_m['xpos'].setValue(-313)
        emi_m['ypos'].setValue(179)
    # ----------------------------------------------------------------------
    if "sss" in channels:
        sss = True
        # sss
        sss = nuke.createNode("Shuffle")
        sss['in'].setValue("sss")
        sss['name'].setValue("sss")
        sss.setInput(0, file)
        sss['xpos'].setValue(-62.0)
        sss['ypos'].setValue(331.0)
        # block_10
        bdn_10 = nuke.createNode("BackdropNode")
        bdn_10["xpos"].setValue(-150)
        bdn_10["ypos"].setValue(300)
        bdn_10["bdheight"].setValue(100)
        bdn_10["bdwidth"].setValue(200)
        bdn_10["label"].setValue("sss")
        bdn_10["note_font_size"].setValue(20)
        bdn_10["tile_color"].setValue(12313212)
        # sss_m
        sss_m = nuke.createNode("Merge2")
        if em:
            sss_m.setInput(0, emi_m)
        elif sf or sk or sr or sda or sia:
            sss_m.setInput(0, sp_diff)
        elif dia or dda or df or dk or dr:
            sss_m.setInput(0, diff_m)
        else:
            sss_m.setInput(0, file)
        sss_m.setInput(1, sss)
        sss_m["operation"].setValue("plus")
        sss_m['xpos'].setValue(-313)
        sss_m['ypos'].setValue(331)

    # ----------------------------------------------------------------------
    if "transmission" in channels:
        trans = True
        # transmission
        transmission = nuke.createNode("Shuffle")
        transmission['in'].setValue("transmission")
        transmission['name'].setValue("transmission")
        transmission.setInput(0, file)
        transmission['xpos'].setValue(-59)
        transmission['ypos'].setValue(485)
        # block_11
        bdn_11 = nuke.createNode("BackdropNode")
        bdn_11["xpos"].setValue(-150)
        bdn_11["ypos"].setValue(450)
        bdn_11["bdheight"].setValue(100)
        bdn_11["bdwidth"].setValue(200)
        bdn_11["label"].setValue("transmission")
        bdn_11["note_font_size"].setValue(20)
        bdn_11["tile_color"].setValue(22222222)
        # transmission_m
        transmission_m = nuke.createNode("Merge2")
        if sss:
            transmission_m.setInput(0, sss_m)
        elif em:
            transmission_m.setInput(0, emi_m)
        elif sf or sk or sr or sda or sia:
            transmission_m.setInput(0, sp_diff)
        elif dia or dda or df or dk or dr:
            transmission_m.setInput(0, diff_m)
        else:
            transmission_m.setInput(0, file)
        transmission_m.setInput(1, transmission)
        transmission_m["operation"].setValue("plus")
        transmission_m['xpos'].setValue(-313)
        transmission_m['ypos'].setValue(485)

    # ----------------------------------------------------------------------

    # copy_alpha
    copy_alpha = nuke.createNode("Copy")
    if trans:
        copy_alpha.setInput(0, transmission_m)
    elif sss:
        copy_alpha.setInput(0, sss_m)
    elif em:
        copy_alpha.setInput(0, emi_m)
    elif sf or sk or sr or sda or sia:
        copy_alpha.setInput(0, sp_diff)
    elif dia or dda or df or dk or dr:
        copy_alpha.setInput(0, diff_m)
    else:
        copy_alpha.setInput(0, file)

    copy_alpha.setInput(1, diaj)
    copy_alpha['xpos'].setValue(-313)
    copy_alpha['ypos'].setValue(600)

    # ----------------------------------------------------------------------
    if "motionvector" in channels:
        mov = True
        # motionvector
        motionvector = nuke.createNode("Shuffle")
        motionvector['in'].setValue("motionvector")
        motionvector['name'].setValue("motionvector")
        motionvector.setInput(0, file)
        motionvector['xpos'].setValue(-57)
        motionvector['ypos'].setValue(778)

        # copy
        copy_m = nuke.createNode("Copy")
        copy_m.setInput(1, motionvector)
        copy_m.setInput(0, copy_alpha)
        copy_m["from0"].setValue("rgba.red")
        copy_m["to0"].setValue("forward.u")
        copy_m["from1"].setValue("rgba.green")
        copy_m["to1"].setValue("forward.v")
        copy_m['xpos'].setValue(-313)
        copy_m['ypos'].setValue(765)

        # vector_blur
        vector_blur = nuke.createNode("VectorBlur2")
        vector_blur.setInput(0, copy_m)
        vector_blur["uv"].setValue("forward")
        vector_blur["mv_presets"].setValue("Arnold")
        vector_blur["scale"].setValue(2)
        vector_blur['xpos'].setValue(-313)
        vector_blur['ypos'].setValue(860)
        # block_12
        bdn_12 = nuke.createNode("BackdropNode")
        bdn_12["xpos"].setValue(-350)
        bdn_12["ypos"].setValue(750)
        bdn_12["bdheight"].setValue(200)
        bdn_12["bdwidth"].setValue(500)
        bdn_12["label"].setValue("motion_blur")
        bdn_12["note_font_size"].setValue(20)
        bdn_12["tile_color"].setValue(111111111111)

    # ----------------------------------------------------------------------
    if "N" in channels:
        # nj
        nj = nuke.createNode("Dot")
        nj["xpos"].setValue(575)
        nj["ypos"].setValue(-900)
        nj.setInput(0, file)
        # N
        N = nuke.createNode("Shuffle")
        N['in'].setValue("N")
        N['name'].setValue("N")
        N.setInput(0, nj)
        N['xpos'].setValue(541)
        N['ypos'].setValue(-1158)

        # block_13
        bdn_13 = nuke.createNode("BackdropNode")
        bdn_13["xpos"].setValue(500)
        bdn_13["ypos"].setValue(-1200)
        bdn_13["bdheight"].setValue(100)
        bdn_13["bdwidth"].setValue(150)
        bdn_13["label"].setValue("N")
        bdn_13["note_font_size"].setValue(20)
        bdn_13["tile_color"].setValue(123123321)

    if "P" in channels:
        # pj
        pj = nuke.createNode("Dot")
        pj["xpos"].setValue(754)
        pj["ypos"].setValue(-900)
        pj.setInput(0, file)
        # P
        P = nuke.createNode("Shuffle")
        P['in'].setValue("P")
        P['name'].setValue("P")
        P.setInput(0, pj)
        P['xpos'].setValue(720)
        P['ypos'].setValue(-1160)
        # block_14
        bdn_14 = nuke.createNode("BackdropNode")
        bdn_14["xpos"].setValue(680)
        bdn_14["ypos"].setValue(-1200)
        bdn_14["bdheight"].setValue(100)
        bdn_14["bdwidth"].setValue(150)
        bdn_14["label"].setValue("P")
        bdn_14["note_font_size"].setValue(20)
        bdn_14["tile_color"].setValue(12312323321)

    if "Z" in channels:
        # zj
        zj = nuke.createNode("Dot")
        zj["xpos"].setValue(952)
        zj["ypos"].setValue(-900)
        zj.setInput(0, file)
        # Z
        Z = nuke.createNode("Shuffle")
        Z['in'].setValue("Z")
        Z['name'].setValue("Z")
        Z.setInput(0, zj)
        Z['xpos'].setValue(918)
        Z['ypos'].setValue(-1160)
        # block_15
        bdn_15 = nuke.createNode("BackdropNode")
        bdn_15["xpos"].setValue(880)
        bdn_15["ypos"].setValue(-1200)
        bdn_15["bdheight"].setValue(100)
        bdn_15["bdwidth"].setValue(150)
        bdn_15["label"].setValue("Z")
        bdn_15["note_font_size"].setValue(20)
        bdn_15["tile_color"].setValue(1257323321)

    if "diffuse" in channels or "diffuse_albedo" in channels:
        # dj
        dj = nuke.createNode("Dot")
        dj["xpos"].setValue(1715)
        dj["ypos"].setValue(-900)
        dj.setInput(0, file)
        # block_16
        bdn_16 = nuke.createNode("BackdropNode")
        bdn_16["xpos"].setValue(1650)
        bdn_16["ypos"].setValue(-1200)
        bdn_16["bdheight"].setValue(200)
        bdn_16["bdwidth"].setValue(150)
        bdn_16["label"].setValue("diff_left")
        bdn_16["note_font_size"].setValue(20)
        bdn_16["tile_color"].setValue(125321)
    if "diffuse" in channels:
        # diffuse
        diffuse = nuke.createNode("Shuffle")
        diffuse['in'].setValue("diffuse")
        diffuse['name'].setValue("diffuse")
        diffuse.setInput(0, dj)
        diffuse['xpos'].setValue(1681)
        diffuse['ypos'].setValue(-1160)
    if "diffuse_albedo" in channels:
        # diffuse_albedo
        diffuse_albedo = nuke.createNode("Shuffle")
        diffuse_albedo['in'].setValue("diffuse_albedo")
        diffuse_albedo['name'].setValue("diffuse_albedo")
        diffuse_albedo.setInput(0, dj)
        diffuse_albedo['xpos'].setValue(1681)
        diffuse_albedo['ypos'].setValue(-1100)

    if "specular" in channels or "specular_albedo" in channels or "specular_amb" in channels:
        # sj
        sj = nuke.createNode("Dot")
        sj["xpos"].setValue(1153)
        sj["ypos"].setValue(-900)
        sj.setInput(0, file)
        # block_17
        bdn_17 = nuke.createNode("BackdropNode")
        bdn_17["xpos"].setValue(1100)
        bdn_17["ypos"].setValue(-1200)
        bdn_17["bdheight"].setValue(250)
        bdn_17["bdwidth"].setValue(150)
        bdn_17["label"].setValue("spec_left")
        bdn_17["note_font_size"].setValue(20)
        bdn_17["tile_color"].setValue(121115321)
    if "specular" in channels:
        # specular
        specular = nuke.createNode("Shuffle")
        specular['in'].setValue("specular")
        specular['name'].setValue("specular")
        specular.setInput(0, sj)
        specular['xpos'].setValue(1119)
        specular['ypos'].setValue(-1160)
    if "specular_albedo" in channels:
        # specular_albedo
        specular_albedo = nuke.createNode("Shuffle")
        specular_albedo['in'].setValue("specular_albedo")
        specular_albedo['name'].setValue("specular_albedo")
        specular_albedo.setInput(0, sj)
        specular_albedo['xpos'].setValue(1119)
        specular_albedo['ypos'].setValue(-1081.0)
    if "specular_amb" in channels:
        # specular_amb
        specular_amb = nuke.createNode("Shuffle")
        specular_amb['in'].setValue("specular_amb")
        specular_amb['name'].setValue("specular_amb")
        specular_amb.setInput(0, sj)
        specular_amb['xpos'].setValue(1119)
        specular_amb['ypos'].setValue(-1012)

    if "sss_albedo" in channels:
        # sssj
        sssj = nuke.createNode("Dot")
        sssj["xpos"].getValue()
        sssj["xpos"].setValue(1440)
        sssj["ypos"].setValue(-900)
        sssj.setInput(0, file)
        # sss_albedo
        sss_albedo = nuke.createNode("Shuffle")
        sss_albedo['in'].setValue("sss_albedo")
        sss_albedo['name'].setValue("sss_albedo")
        sss_albedo.setInput(0, sssj)
        sss_albedo['xpos'].setValue(1406)
        sss_albedo['ypos'].setValue(-1160)
        # block_18
        bdn_18 = nuke.createNode("BackdropNode")
        bdn_18["xpos"].setValue(1380)
        bdn_18["ypos"].setValue(-1200)
        bdn_18["bdheight"].setValue(100)
        bdn_18["bdwidth"].setValue(150)
        bdn_18["label"].setValue("sss_left")
        bdn_18["note_font_size"].setValue(20)
        bdn_18["tile_color"].setValue(22222)

    if src_path:
        readfile = nuke.createNode("Read")
        readfile['name'].setValue("source")
        readfile['file'].fromUserText(src_path)
        readfile["xpos"].setValue(41)
        readfile["ypos"].setValue(1259)
        basic_format = readfile["format"].toScript()
        nuke.addFormat('%s %s' % (basic_format, "basic_res"))

    if dist_path:
        nuke.nodePaste(dist_path)
        packs = nuke.selectedNodes()
        for node in packs:
            if node.Class() == "GridWarp":
                dist_node = node
                break
        for node in packs:
            if node == dist_node:
                continue
            else:
                nuke.delete(node)

        dist_node["dst_hide"].setValue(1)
        dist_node["reverse"].setValue(1)
        dist_node["background"].setValue(0)
        dist_node["xpos"].setValue(-313)
        dist_node["ypos"].setValue(1040)
        if mov:
            dist_node.setInput(0, vector_blur)
        elif trans:
            dist_node.setInput(0, transmission_m)
        elif sss:
            dist_node.setInput(0, sss_m)
        elif em:
            dist_node.setInput(0, emi_m)
        elif sf or sk or sr or sda or sia:
            dist_node.setInput(0, sp_diff)
        elif dia or dda or df or dk or dr:
            dist_node.setInput(0, diff_m)
        else:
            dist_node.setInput(0, file)
        reformat = nuke.createNode("Reformat")
        reformat["resize"].setValue(0)
        reformat.setInput(0, dist_node)
        reformat["xpos"].setValue(-313)
        reformat["ypos"].setValue(1190)
        reformat["clamp"].setValue(1)
        try:
            reformat["format"].setValue("basic_res")
        except:
            reformat["format"].setValue("%s basic_res" % basic_format.split(" ")[-1])
    else:
        reformat = nuke.createNode("Reformat")
        reformat["resize"].setValue(0)
        if mov:
            reformat.setInput(0, vector_blur)
        elif trans:
            reformat.setInput(0, transmission_m)
        elif sss:
            reformat.setInput(0, sss_m)
        elif em:
            reformat.setInput(0, emi_m)
        elif sf or sk or sr or sda or sia:
            reformat.setInput(0, sp_diff)
        elif dia or dda or df or dk or dr:
            reformat.setInput(0, diff_m)
        else:
            reformat.setInput(0, file)
        reformat["xpos"].setValue(-313)
        reformat["ypos"].setValue(1119)
        reformat["clamp"].setValue(1)
        reformat["format"].setValue("basic_res")
    # block_d
    block_d = nuke.createNode("BackdropNode")
    block_d["xpos"].setValue(-380.0)
    block_d["ypos"].setValue(1000)
    block_d["bdheight"].setValue(275)
    block_d["bdwidth"].setValue(250)
    block_d["label"].setValue("distort")
    block_d["note_font_size"].setValue(20)
    block_d["tile_color"].setValue(1129690623)

    finalmerge = nuke.createNode("Merge2")
    finalmerge.setInput(0, readfile)
    finalmerge.setInput(1, reformat)
    finalmerge["operation"].setValue("over")
    finalmerge['xpos'].setValue(-313)
    finalmerge['ypos'].setValue(1300)

    write = nuke.createNode("Write")
    write["file"].setValue(outpath)
    write["file_type"].setValue("targa")
    write.setInput(0, finalmerge)
    write['xpos'].setValue(-313)
    write['ypos'].setValue(1500)
