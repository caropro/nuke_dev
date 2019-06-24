# coding=utf-8
import os
import nuke

def main():
    current_path = nuke.root()["name"].getValue()
    filename = current_path.split("/")[-1].split(".")[0]
    step_root = current_path.split("nuke")[0]
    outname = filename + ".%04d.tga"
    outpath = os.path.join(step_root, "osc", filename, outname).replace("\\", '/')

    dist_path = nuke.getFilename(message="get the distortfile")
    if not dist_path:
        nuke.message("get the distort file!")
    src_path = nuke.getClipname("get the scr_path")
    if not src_path:
        nuke.message("get the iplate file!")
    fileread = nuke.selectedNode()
    channels = list(set([x.split(".")[0] for x in fileread.channels()]))
    fileread["xpos"].setValue(-9)
    fileread["ypos"].setValue(-1155)
    #unpremult
    unpre = nuke.createNode("Unpremult")
    unpre["xpos"].setValue(-9)
    unpre["ypos"].setValue(-992)
    unpre.setInput(0, fileread)
    #center joint
    cj = nuke.createNode("Dot")
    cj["xpos"].setValue(25)
    cj["ypos"].setValue(-868)
    cj.setInput(0, unpre)
    #joint_for_emission_sss_transmission_and_motion_blur
    cj2 = nuke.createNode("Dot")
    cj2["xpos"].setValue(785)
    cj2["ypos"].setValue(-868)
    cj2.setInput(0, cj)
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

    if "diffuse_direct_amb" in channels:
        dda = True
        # ddaj
        ddaj = nuke.createNode("Dot")
        ddaj["xpos"].setValue(-369)
        ddaj["ypos"].setValue(-868)
        ddaj.setInput(0, cj)
        # diffuse_direct_amb
        diffuse_direct_amb = nuke.createNode("Shuffle")
        diffuse_direct_amb['in'].setValue("diffuse_direct_amb")
        diffuse_direct_amb['name'].setValue("diffuse_direct_amb")
        diffuse_direct_amb['xpos'].setValue(-403.0)
        diffuse_direct_amb['ypos'].setValue(-735.0)
        diffuse_direct_amb.setInput(0, ddaj)
        grade_dda = nuke.createNode("Grade")
        grade_dda['name'].setValue("Grade_diffuse_direct_amb")
        grade_dda['xpos'].setValue(-403.0)
        grade_dda['ypos'].setValue(-683.0)
        grade_dda.setInput(0, diffuse_direct_amb)
        cc_dda = nuke.createNode("ColorCorrect")
        cc_dda['name'].setValue("ColorCorrect_diffuse_direct_amb")
        cc_dda['xpos'].setValue(-403.0)
        cc_dda['ypos'].setValue(-647.0)
        cc_dda.setInput(0, grade_dda)
    if "diffuse_indirect_amb" in channels:
        dia=True
        # diaj
        diaj = nuke.createNode("Dot")
        diaj["xpos"].setValue(-199)
        diaj["ypos"].setValue(-868)
        diaj.setInput(0, cj)
        # diffuse_indirect_amb
        diffuse_indirect_amb = nuke.createNode("Shuffle")
        diffuse_indirect_amb['in'].setValue("diffuse_indirect_amb")
        diffuse_indirect_amb['name'].setValue("diffuse_indirect_amb")
        diffuse_indirect_amb['xpos'].setValue(-233.0)
        diffuse_indirect_amb['ypos'].setValue(-648.0)
        diffuse_indirect_amb.setInput(0, diaj)
        grade_dia = nuke.createNode("Grade")
        grade_dia['name'].setValue("Grade_diffuse_indirect_amb")
        grade_dia['xpos'].setValue(-233.0)
        grade_dia['ypos'].setValue(-614.0)
        grade_dia.setInput(0, diffuse_indirect_amb)
        cc_dia = nuke.createNode("ColorCorrect")
        cc_dia['name'].setValue("ColorCorrect_diffuse_indirect_amb")
        cc_dia['xpos'].setValue(-233.0)
        cc_dia['ypos'].setValue(-588.0)
        cc_dia.setInput(0, grade_dia)
    if dda or dia:
        # block_1
        bdn_1 = nuke.createNode("BackdropNode")
        bdn_1["xpos"].setValue(-440.0)
        bdn_1["ypos"].setValue(-778.0)
        bdn_1["bdheight"].setValue(240)
        bdn_1["bdwidth"].setValue(317)
        bdn_1["label"].setValue("amb_dif")
        bdn_1["note_font_size"].setValue(20)
        bdn_1["tile_color"].setValue(1129690623)
        # m1
        m1 = nuke.createNode("Merge2")
        if dda:
            m1.setInput(1, cc_dda)
        if dia:
            m1.setInput(0, cc_dia)
        m1["operation"].setValue("plus")
        m1['xpos'].setValue(-403.0)
        m1['ypos'].setValue(-588.0)

        m1j = nuke.createNode("Dot")
        m1j["xpos"].setValue(-369)
        m1j["ypos"].setValue(-411)
        m1j.setInput(0, m1)

    if "diffuse_fill" in channels:
        df = True
        # diffuse_fill
        diffuse_fill = nuke.createNode("Shuffle")
        diffuse_fill['in'].setValue("diffuse_fill")
        diffuse_fill['name'].setValue("diffuse_fill")
        diffuse_fill.setInput(0, cj)
        diffuse_fill['xpos'].setValue(-9.0)
        diffuse_fill['ypos'].setValue(-717.0)

        grade_df = nuke.createNode("Grade")
        grade_df['name'].setValue("Grade_diffuse_fill")
        grade_df['xpos'].setValue(-9.0)
        grade_df['ypos'].setValue(-659.0)
        grade_df.setInput(0, diffuse_fill)
        cc_df = nuke.createNode("ColorCorrect")
        cc_df['name'].setValue("ColorCorrect_diffuse_fill")
        cc_df['xpos'].setValue(-9.0)
        cc_df['ypos'].setValue(-614.0)
        cc_df.setInput(0, grade_df)
        # block_2
        bdn_2 = nuke.createNode("BackdropNode")
        bdn_2["xpos"].setValue(-61.0)
        bdn_2["ypos"].setValue(-796)
        bdn_2["bdheight"].setValue(246)
        bdn_2["bdwidth"].setValue(166)
        bdn_2["label"].setValue("fill_dif")
        bdn_2["note_font_size"].setValue(20)
        bdn_2["tile_color"].setValue(14532120623)
    if "diffuse_key" in channels:
        dk = True
        # dkj
        dkj = nuke.createNode("Dot")
        dkj["xpos"].setValue(309)
        dkj["ypos"].setValue(-868)
        dkj.setInput(0, cj)
        # diffuse_key
        diffuse_key = nuke.createNode("Shuffle")
        diffuse_key['in'].setValue("diffuse_key")
        diffuse_key['name'].setValue("diffuse_key")
        diffuse_key['xpos'].setValue(275.0)
        diffuse_key['ypos'].setValue(-744.0)
        diffuse_key.setInput(0, dkj)

        grade_dk = nuke.createNode("Grade")
        grade_dk['name'].setValue("Grade_diffuse_key")
        grade_dk['xpos'].setValue(275.0)
        grade_dk['ypos'].setValue(-705.0)
        grade_dk.setInput(0, diffuse_key)
        cc_dk = nuke.createNode("ColorCorrect")
        cc_dk['name'].setValue("ColorCorrect_diffuse_key")
        cc_dk['xpos'].setValue(275.0)
        cc_dk['ypos'].setValue(-679.0)
        cc_dk.setInput(0, grade_dk)

        key_dot = nuke.createNode("Dot")
        key_dot.setInput(0, cc_dk)
        key_dot['xpos'].setValue(309.0)
        key_dot['ypos'].setValue(-488.0)
        # block_3
        bdn_3 = nuke.createNode("BackdropNode")
        bdn_3["xpos"].setValue(242.0)
        bdn_3["ypos"].setValue(-807)
        bdn_3["bdheight"].setValue(246)
        bdn_3["bdwidth"].setValue(166)
        bdn_3["label"].setValue("key_dif")
        bdn_3["note_font_size"].setValue(20)
        bdn_3["tile_color"].setValue(1451560623)
    if "diffuse_rim" in channels:
        dr = True
        # drj
        drj = nuke.createNode("Dot")
        drj["xpos"].setValue(552)
        drj["ypos"].setValue(-868)
        drj.setInput(0, cj)
        # diffuse_rim
        diffuse_rim = nuke.createNode("Shuffle")
        diffuse_rim['in'].setValue("diffuse_rim")
        diffuse_rim['name'].setValue("diffuse_rim")
        diffuse_rim.setInput(0, drj)
        diffuse_rim['xpos'].setValue(518.0)
        diffuse_rim['ypos'].setValue(-735.0)

        grade_dr = nuke.createNode("Grade")
        grade_dr['name'].setValue("Grade_diffuse_rim")
        grade_dr['xpos'].setValue(518.0)
        grade_dr['ypos'].setValue(-709.0)
        grade_dr.setInput(0, diffuse_rim)
        cc_dr = nuke.createNode("ColorCorrect")
        cc_dr['name'].setValue("ColorCorrect_diffuse_rim")
        cc_dr['xpos'].setValue(518.0)
        cc_dr['ypos'].setValue(-683.0)
        cc_dr.setInput(0, grade_dr)

        rim_dot = nuke.createNode("Dot")
        rim_dot.setInput(0, cc_dr)
        rim_dot['xpos'].setValue(552.0)
        rim_dot['ypos'].setValue(-488.0)
        # block_4
        bdn_4 = nuke.createNode("BackdropNode")
        bdn_4["xpos"].setValue(512.0)
        bdn_4["ypos"].setValue(-807)
        bdn_4["bdheight"].setValue(246)
        bdn_4["bdwidth"].setValue(166)
        bdn_4["label"].setValue("rim_dif")
        bdn_4["note_font_size"].setValue(20)
        bdn_4["tile_color"].setValue(11251560623)
    if df or dk or dr:
        # m2
        m2 = nuke.createNode("Merge2")
        if df:
            m2.setInput(0, cc_df)
        if dk:
            m2.setInput(1, key_dot)
        if dr:
            m2.setInput(3, rim_dot)
        m2["operation"].setValue("plus")
        m2['xpos'].setValue(-9.0)
        m2['ypos'].setValue(-492.0)
    if dia or dda or df or dk or dr:
        # diff_m
        diff_m = nuke.createNode("Merge2")
        if dia or dda:
            diff_m.setInput(0, m1j)
        else:
            diff_m.setInput(0, cj)
        if dk or df or dr:
            diff_m.setInput(1, m2)
        diff_m["operation"].setValue("plus")
        diff_m['xpos'].setValue(-9.0)
        diff_m['ypos'].setValue(-415.0)
    # ----------------------------------------------------------------------
    if "specular_direct_amb" in channels:
        sda = True
        # sdaj
        sdaj = nuke.createNode("Dot")
        sdaj["xpos"].setValue(624)
        sdaj["ypos"].setValue(-868)
        sdaj.setInput(0, cj)
        # specular_direct_amb
        specular_direct_amb = nuke.createNode("Shuffle")
        specular_direct_amb['in'].setValue("specular_direct_amb")
        specular_direct_amb['name'].setValue("specular_direct_amb")
        specular_direct_amb.setInput(0, sdaj)
        specular_direct_amb['xpos'].setValue(590.0)
        specular_direct_amb['ypos'].setValue(46.0)

        grade_sda = nuke.createNode("Grade")
        grade_sda['name'].setValue("Grade_specular_direct_amb")
        grade_sda['xpos'].setValue(590.0)
        grade_sda['ypos'].setValue(72.0)
        grade_sda.setInput(0, specular_direct_amb)
        cc_sda = nuke.createNode("ColorCorrect")
        cc_sda['name'].setValue("ColorCorrect_specular_direct_amb")
        cc_sda['xpos'].setValue(590.0)
        cc_sda['ypos'].setValue(140.0)
        cc_sda.setInput(0, grade_sda)

    if "specular_indirect_amb" in channels:
        sia = True
        # siaj
        siaj = nuke.createNode("Dot")
        siaj["xpos"].setValue(446)
        siaj["ypos"].setValue(-868)
        siaj.setInput(0, cj)
        # specular_indirect_amb
        specular_indirect_amb = nuke.createNode("Shuffle")
        specular_indirect_amb['in'].setValue("specular_indirect_amb")
        specular_indirect_amb['name'].setValue("specular_indirect_amb")
        specular_indirect_amb.setInput(0, siaj)
        specular_indirect_amb['xpos'].setValue(412.0)
        specular_indirect_amb['ypos'].setValue(47.0)

        grade_sia = nuke.createNode("Grade")
        grade_sia['name'].setValue("Grade_specular_indirect_amb")
        grade_sia['xpos'].setValue(412.0)
        grade_sia['ypos'].setValue(77.0)
        grade_sia.setInput(0, specular_indirect_amb)
        cc_sia = nuke.createNode("ColorCorrect")
        cc_sia['name'].setValue("ColorCorrect_specular_indirect_amb")
        cc_sia['xpos'].setValue(412.0)
        cc_sia['ypos'].setValue(103.0)
        cc_sia.setInput(0, grade_sia)
    if sia or sda:
        # sp_m1
        sp_m1 = nuke.createNode("Merge2")
        if sda:
            sp_m1.setInput(0, cc_sda)
        if sia:
            sp_m1.setInput(1, cc_sia)
        sp_m1["operation"].setValue("plus")
        sp_m1['xpos'].setValue(412.0)
        sp_m1['ypos'].setValue(140.0)
        # block_5
        bdn_5 = nuke.createNode("BackdropNode")
        bdn_5["xpos"].setValue(370)
        bdn_5["ypos"].setValue(-16)
        bdn_5["bdheight"].setValue(219)
        bdn_5["bdwidth"].setValue(322)
        bdn_5["label"].setValue("amb_spc")
        bdn_5["note_font_size"].setValue(20)
        bdn_5["tile_color"].setValue(1125410623)
    if "specular_key" in channels:
        sk = True
        # skj
        skj = nuke.createNode("Dot")
        skj["xpos"].setValue(208)
        skj["ypos"].setValue(-868)
        skj.setInput(0, cj)
        # specular_key
        specular_key = nuke.createNode("Shuffle")
        specular_key['in'].setValue("specular_key")
        specular_key['name'].setValue("specular_key")
        specular_key.setInput(0, skj)
        specular_key['xpos'].setValue(174.0)
        specular_key['ypos'].setValue(-301.0)

        grade_sk = nuke.createNode("Grade")
        grade_sk['name'].setValue("Grade_specular_key")
        grade_sk['xpos'].setValue(174.0)
        grade_sk['ypos'].setValue(-275.0)
        grade_sk.setInput(0, specular_key)
        cc_sk = nuke.createNode("ColorCorrect")
        cc_sk['name'].setValue("ColorCorrect_specular_key")
        cc_sk['xpos'].setValue(174)
        cc_sk['ypos'].setValue(-249.0)
        cc_sk.setInput(0, grade_sk)

        # block_6
        bdn_6 = nuke.createNode("BackdropNode")
        bdn_6["xpos"].setValue(112)
        bdn_6["ypos"].setValue(-381)
        bdn_6["bdheight"].setValue(246)
        bdn_6["bdwidth"].setValue(166)
        bdn_6["label"].setValue("key_spc")
        bdn_6["note_font_size"].setValue(20)
        bdn_6["tile_color"].setValue(11112360623)

    if "specular_fill" in channels:
        sf = True
        # sfj
        sfj = nuke.createNode("Dot")
        sfj["xpos"].setValue(420)
        sfj["ypos"].setValue(-868)
        sfj.setInput(0, cj)
        # specular_fill
        specular_fill = nuke.createNode("Shuffle")
        specular_fill['in'].setValue("specular_fill")
        specular_fill['name'].setValue("specular_fill")
        specular_fill.setInput(0, sfj)
        specular_fill['xpos'].setValue(386.0)
        specular_fill['ypos'].setValue(-304.0)

        grade_specular_fill = nuke.createNode("Grade")
        grade_specular_fill['name'].setValue("Grade_specular_fill")
        grade_specular_fill['xpos'].setValue(386.0)
        grade_specular_fill['ypos'].setValue(-278.0)
        grade_specular_fill.setInput(0, specular_fill)
        cc_specular_fill = nuke.createNode("ColorCorrect")
        cc_specular_fill['name'].setValue("ColorCorrect_specular_fill")
        cc_specular_fill['xpos'].setValue(386.0)
        cc_specular_fill['ypos'].setValue(-238.0)
        cc_specular_fill.setInput(0, grade_specular_fill)

        specular_fill_dot = nuke.createNode("Dot")
        specular_fill_dot.setInput(0, cc_specular_fill)
        specular_fill_dot['xpos'].setValue(420.0)
        specular_fill_dot['ypos'].setValue(-84.0)
        # block_7
        bdn_7 = nuke.createNode("BackdropNode")
        bdn_7["xpos"].setValue(362)
        bdn_7["ypos"].setValue(-381)
        bdn_7["bdheight"].setValue(246)
        bdn_7["bdwidth"].setValue(166)
        bdn_7["label"].setValue("fill_spc")
        bdn_7["note_font_size"].setValue(20)
        bdn_7["tile_color"].setValue(11113211)
    #specular_rim_block
    if "specular_rim" in channels:
        sr = True
        # srj
        srj = nuke.createNode("Dot")
        srj["xpos"].setValue(648)
        srj["ypos"].setValue(-868)
        srj.setInput(0, cj)
        # specular_rim
        specular_rim = nuke.createNode("Shuffle")
        specular_rim['in'].setValue("specular_rim")
        specular_rim['name'].setValue("specular_rim")
        specular_rim.setInput(0, srj)
        specular_rim['xpos'].setValue(614.0)
        specular_rim['ypos'].setValue(-308.0)

        grade_specular_rim = nuke.createNode("Grade")
        grade_specular_rim['name'].setValue("Grade_specular_rim")
        grade_specular_rim['xpos'].setValue(614.0)
        grade_specular_rim['ypos'].setValue(-278.0)
        grade_specular_rim.setInput(0, specular_rim)
        cc_specular_rim = nuke.createNode("ColorCorrect")
        cc_specular_rim['name'].setValue("ColorCorrect_specular_rim")
        cc_specular_rim['xpos'].setValue(614.0)
        cc_specular_rim['ypos'].setValue(-238.0)
        cc_specular_rim.setInput(0, grade_specular_rim)

        specular_rim_dot = nuke.createNode("Dot")
        specular_rim_dot.setInput(0, cc_specular_rim)
        specular_rim_dot['xpos'].setValue(648)
        specular_rim_dot['ypos'].setValue(-84)
        # block_8
        bdn_8 = nuke.createNode("BackdropNode")
        bdn_8["xpos"].setValue(582)
        bdn_8["ypos"].setValue(-381)
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
            sp_m2.setInput(1, cc_sk)
        if sr:
            sp_m2.setInput(3, specular_rim_dot)
        sp_m2["operation"].setValue("plus")
        sp_m2['xpos'].setValue(174)
        sp_m2['ypos'].setValue(-88)

    if sf or sk or sr or sda or sia:
        # sp_m3
        sp_m3 = nuke.createNode("Merge2")
        if sf or sk or sr:
            sp_m3.setInput(0, sp_m2)
        if sda or sia:
            sp_m3.setInput(1, sp_m1)
        sp_m3["operation"].setValue("plus")
        sp_m3['xpos'].setValue(174)
        sp_m3['ypos'].setValue(140)
        # sp_diff
        sp_diff = nuke.createNode("Merge2")
        if dia or dda or df or dk or dr:
            sp_diff.setInput(0, diff_m)
        else:
            sp_diff.setInput(0, cj)
        sp_diff.setInput(1, sp_m3)
        sp_diff["operation"].setValue("plus")
        sp_diff['xpos'].setValue(-9)
        sp_diff['ypos'].setValue(140)
    # ----------------------------------------------------------------------
    if "emission" in channels:
        em = True

        emission_dot = nuke.createNode("Dot")
        emission_dot["xpos"].setValue(785)
        emission_dot["ypos"].setValue(294)
        emission_dot.setInput(0, cj2)
        # emission
        emission = nuke.createNode("Shuffle")
        emission['in'].setValue("emission")
        emission['name'].setValue("emission")
        emission.setInput(0, emission_dot)
        emission['xpos'].setValue(246)
        emission['ypos'].setValue(290)

        grade_emission = nuke.createNode("Grade")
        grade_emission['name'].setValue("Grade_emission")
        grade_emission['xpos'].setValue(246.0)
        grade_emission['ypos'].setValue(316.0)
        grade_emission.setInput(0, emission)
        cc_emission = nuke.createNode("ColorCorrect")
        cc_emission['name'].setValue("ColorCorrect_emission")
        cc_emission['xpos'].setValue(246.0)
        cc_emission['ypos'].setValue(342.0)
        cc_emission.setInput(0, grade_emission)
        # block_9
        bdn_9 = nuke.createNode("BackdropNode")
        bdn_9["xpos"].setValue(181)
        bdn_9["ypos"].setValue(236)
        bdn_9["bdheight"].setValue(144)
        bdn_9["bdwidth"].setValue(193)
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
            emi_m.setInput(0, cj)
        emi_m.setInput(1, cc_emission)
        emi_m["operation"].setValue("plus")
        emi_m['xpos'].setValue(-9)
        emi_m['ypos'].setValue(342)
    # ----------------------------------------------------------------------
    if "sss" in channels:
        sss = True

        sss_dot = nuke.createNode("Dot")
        sss_dot["xpos"].setValue(785)
        sss_dot["ypos"].setValue(453)
        sss_dot.setInput(0, cj2)
        # sss
        sss_node = nuke.createNode("Shuffle")
        sss_node['in'].setValue("sss")
        sss_node['name'].setValue("sss")
        sss_node.setInput(0, sss_dot)
        sss_node['xpos'].setValue(264.0)
        sss_node['ypos'].setValue(449.0)

        grade_sss = nuke.createNode("Grade")
        grade_sss['name'].setValue("Grade_sss")
        grade_sss['xpos'].setValue(264.0)
        grade_sss['ypos'].setValue(475.0)
        grade_sss.setInput(0, sss_node)
        cc_sss = nuke.createNode("ColorCorrect")
        cc_sss['name'].setValue("ColorCorrect_sss")
        cc_sss['xpos'].setValue(264.0)
        cc_sss['ypos'].setValue(501.0)
        cc_sss.setInput(0, grade_sss)

        # block_10
        bdn_10 = nuke.createNode("BackdropNode")
        bdn_10["xpos"].setValue(176)
        bdn_10["ypos"].setValue(418)
        bdn_10["bdheight"].setValue(118)
        bdn_10["bdwidth"].setValue(188)
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
            sss_m.setInput(0, cj)
        sss_m.setInput(1, cc_sss)
        sss_m["operation"].setValue("plus")
        sss_m['xpos'].setValue(-9)
        sss_m['ypos'].setValue(501)

    # ----------------------------------------------------------------------
    if "transmission" in channels:
        trans = True

        trans_dot = nuke.createNode("Dot")
        trans_dot["xpos"].setValue(785)
        trans_dot["ypos"].setValue(604)
        trans_dot.setInput(0, cj2)
        # transmission
        transmission = nuke.createNode("Shuffle")
        transmission['in'].setValue("transmission")
        transmission['name'].setValue("transmission")
        transmission.setInput(0, trans_dot)
        transmission['xpos'].setValue(267)
        transmission['ypos'].setValue(600)

        grade_transmission = nuke.createNode("Grade")
        grade_transmission['name'].setValue("Grade_transmission")
        grade_transmission['xpos'].setValue(267.0)
        grade_transmission['ypos'].setValue(626.0)
        grade_transmission.setInput(0, transmission)
        cc_transmission = nuke.createNode("ColorCorrect")
        cc_transmission['name'].setValue("ColorCorrect_transmission")
        cc_transmission['xpos'].setValue(267.0)
        cc_transmission['ypos'].setValue(652.0)
        cc_transmission.setInput(0, grade_transmission)
        # block_11
        bdn_11 = nuke.createNode("BackdropNode")
        bdn_11["xpos"].setValue(176)
        bdn_11["ypos"].setValue(565)
        bdn_11["bdheight"].setValue(127)
        bdn_11["bdwidth"].setValue(196)
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
            transmission_m.setInput(0, cj)
        transmission_m.setInput(1, cc_transmission)
        transmission_m["operation"].setValue("plus")
        transmission_m['xpos'].setValue(-9)
        transmission_m['ypos'].setValue(652)

    # ----------------------------------------------------------------------

    # copy_alpha

    alpha_dot = nuke.createNode("Dot")
    alpha_dot["xpos"].setValue(-512)
    alpha_dot["ypos"].setValue(-868)
    alpha_dot.setInput(0, cj)

    alpha_dot2 = nuke.createNode("Dot")
    alpha_dot2["xpos"].setValue(-512)
    alpha_dot2["ypos"].setValue(727)
    alpha_dot2.setInput(0, alpha_dot)

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
        copy_alpha.setInput(0, cj)

    copy_alpha['name'].setValue("copy_alpha")
    copy_alpha.setInput(1, alpha_dot2)
    copy_alpha['xpos'].setValue(-9)
    copy_alpha['ypos'].setValue(717)

    # ----------------------------------------------------------------------
    if "motionvector" in channels:
        mov = True

        mov_dot = nuke.createNode("Dot")
        mov_dot["xpos"].setValue(785)
        mov_dot["ypos"].setValue(870)
        mov_dot.setInput(0, cj2)
        # motionvector
        motionvector = nuke.createNode("Shuffle")
        motionvector['in'].setValue("motionvector")
        motionvector['name'].setValue("motionvector")
        motionvector.setInput(0, mov_dot)
        motionvector['xpos'].setValue(247)
        motionvector['ypos'].setValue(866)

        # copy
        copy_m = nuke.createNode("Copy")
        copy_m.setInput(1, motionvector)
        copy_m.setInput(0, copy_alpha)
        copy_m["from0"].setValue("rgba.red")
        copy_m["to0"].setValue("forward.u")
        copy_m["from1"].setValue("rgba.green")
        copy_m["to1"].setValue("forward.v")
        copy_m['xpos'].setValue(-9)
        copy_m['ypos'].setValue(853)

        # vector_blur
        vector_blur = nuke.createNode("VectorBlur2")
        vector_blur.setInput(0, copy_m)
        vector_blur["uv"].setValue("forward")
        vector_blur["mv_presets"].setValue("Arnold")
        vector_blur["scale"].setValue(2)
        vector_blur['xpos'].setValue(-9)
        vector_blur['ypos'].setValue(948)
        # block_12
        bdn_12 = nuke.createNode("BackdropNode")
        bdn_12["xpos"].setValue(-46)
        bdn_12["ypos"].setValue(788)
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
        nj["ypos"].setValue(-988)
        nj.setInput(0, unpre)
        # N
        N = nuke.createNode("Shuffle")
        N['in'].setValue("N")
        N['name'].setValue("N")
        N.setInput(0, nj)
        N['xpos'].setValue(541)
        N['ypos'].setValue(-1236)

        # block_13
        bdn_13 = nuke.createNode("BackdropNode")
        bdn_13["xpos"].setValue(492)
        bdn_13["ypos"].setValue(-1282)
        bdn_13["bdheight"].setValue(100)
        bdn_13["bdwidth"].setValue(150)
        bdn_13["label"].setValue("N")
        bdn_13["note_font_size"].setValue(20)
        bdn_13["tile_color"].setValue(123123321)

    if "P" in channels:
        # pj
        pj = nuke.createNode("Dot")
        pj["xpos"].setValue(746)
        pj["ypos"].setValue(-988)
        pj.setInput(0, unpre)
        # P
        P = nuke.createNode("Shuffle")
        P['in'].setValue("P")
        P['name'].setValue("P")
        P.setInput(0, pj)
        P['xpos'].setValue(712)
        P['ypos'].setValue(-1242)
        # block_14
        bdn_14 = nuke.createNode("BackdropNode")
        bdn_14["xpos"].setValue(672)
        bdn_14["ypos"].setValue(-1282)
        bdn_14["bdheight"].setValue(100)
        bdn_14["bdwidth"].setValue(150)
        bdn_14["label"].setValue("P")
        bdn_14["note_font_size"].setValue(20)
        bdn_14["tile_color"].setValue(12312323321)

    if "Z" in channels:
        # zj
        zj = nuke.createNode("Dot")
        zj["xpos"].setValue(954)
        zj["ypos"].setValue(-982)
        zj.setInput(0, unpre)
        # Z
        Z = nuke.createNode("Shuffle")
        Z['in'].setValue("Z")
        Z['name'].setValue("Z")
        Z.setInput(0, zj)
        Z['xpos'].setValue(920)
        Z['ypos'].setValue(-1240)
        # block_15
        bdn_15 = nuke.createNode("BackdropNode")
        bdn_15["xpos"].setValue(879)
        bdn_15["ypos"].setValue(-1282)
        bdn_15["bdheight"].setValue(100)
        bdn_15["bdwidth"].setValue(150)
        bdn_15["label"].setValue("Z")
        bdn_15["note_font_size"].setValue(20)
        bdn_15["tile_color"].setValue(1257323321)

    if "diffuse" in channels or "diffuse_albedo" in channels:
        # dj
        dj = nuke.createNode("Dot")
        dj["xpos"].setValue(1707)
        dj["ypos"].setValue(-988)
        dj.setInput(0, unpre)
        # block_16
        bdn_16 = nuke.createNode("BackdropNode")
        bdn_16["xpos"].setValue(1642)
        bdn_16["ypos"].setValue(-1282)
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
        diffuse['xpos'].setValue(1673)
        diffuse['ypos'].setValue(-1236)
    if "diffuse_albedo" in channels:
        # diffuse_albedo
        diffuse_albedo = nuke.createNode("Shuffle")
        diffuse_albedo['in'].setValue("diffuse_albedo")
        diffuse_albedo['name'].setValue("diffuse_albedo")
        diffuse_albedo.setInput(0, dj)
        diffuse_albedo['xpos'].setValue(1673)
        diffuse_albedo['ypos'].setValue(-1182)

    if "specular" in channels or "specular_albedo" in channels or "specular_amb" in channels:
        # sj
        sj = nuke.createNode("Dot")
        sj["xpos"].setValue(1145)
        sj["ypos"].setValue(-988)
        sj.setInput(0, unpre)
        # block_17
        bdn_17 = nuke.createNode("BackdropNode")
        bdn_17["xpos"].setValue(1092)
        bdn_17["ypos"].setValue(-1282)
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
        specular['xpos'].setValue(1111)
        specular['ypos'].setValue(-1242)
    if "specular_albedo" in channels:
        # specular_albedo
        specular_albedo = nuke.createNode("Shuffle")
        specular_albedo['in'].setValue("specular_albedo")
        specular_albedo['name'].setValue("specular_albedo")
        specular_albedo.setInput(0, sj)
        specular_albedo['xpos'].setValue(1111)
        specular_albedo['ypos'].setValue(-1163.0)
    if "specular_amb" in channels:
        # specular_amb
        specular_amb = nuke.createNode("Shuffle")
        specular_amb['in'].setValue("specular_amb")
        specular_amb['name'].setValue("specular_amb")
        specular_amb.setInput(0, sj)
        specular_amb['xpos'].setValue(1111)
        specular_amb['ypos'].setValue(-1094)

    if "sss_albedo" in channels:
        # sssj
        sssj = nuke.createNode("Dot")
        sssj["xpos"].getValue()
        sssj["xpos"].setValue(1432)
        sssj["ypos"].setValue(-988)
        sssj.setInput(0, unpre)
        # sss_albedo
        sss_albedo = nuke.createNode("Shuffle")
        sss_albedo['in'].setValue("sss_albedo")
        sss_albedo['name'].setValue("sss_albedo")
        sss_albedo.setInput(0, sssj)
        sss_albedo['xpos'].setValue(1398)
        sss_albedo['ypos'].setValue(-1242)
        # block_18
        bdn_18 = nuke.createNode("BackdropNode")
        bdn_18["xpos"].setValue(1372)
        bdn_18["ypos"].setValue(-1282)
        bdn_18["bdheight"].setValue(100)
        bdn_18["bdwidth"].setValue(150)
        bdn_18["label"].setValue("sss_left")
        bdn_18["note_font_size"].setValue(20)
        bdn_18["tile_color"].setValue(22222)

    premult = nuke.createNode("Premult")
    premult["xpos"].getValue()
    premult["xpos"].setValue(-9)
    premult["ypos"].setValue(1029)
    if mov:
        premult.setInput(0, vector_blur)
    elif trans:
        premult.setInput(0, transmission_m)
    elif sss:
        premult.setInput(0, sss_m)
    elif em:
        premult.setInput(0, emi_m)
    elif sf or sk or sr or sda or sia:
        premult.setInput(0, sp_diff)
    elif dia or dda or df or dk or dr:
        premult.setInput(0, diff_m)
    else:
        premult.setInput(0, cj)

    final_cc = nuke.createNode("ColorCorrect")
    final_cc["xpos"].getValue()
    final_cc["xpos"].setValue(-9)
    final_cc["ypos"].setValue(1055)
    final_cc.setInput(0, premult)

    soften = nuke.createNode("Soften")
    soften["xpos"].getValue()
    soften["xpos"].setValue(-9)
    soften["ypos"].setValue(1081)
    soften.setInput(0, final_cc)

    if src_path:
        readfile = nuke.createNode("Read")
        readfile['name'].setValue("source")
        readfile['file'].fromUserText(src_path)
        readfile["xpos"].setValue(345)
        readfile["ypos"].setValue(1432)
        basic_format = readfile["format"].toScript()
        back_up_format=basic_format.split(" ")[-1]
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
        dist_node["xpos"].setValue(-9)
        dist_node["ypos"].setValue(1207)

        dist_node.setInput(0, soften)

        reformat = nuke.createNode("Reformat")
        reformat["resize"].setValue(0)
        reformat.setInput(0, dist_node)
        reformat["xpos"].setValue(-9)
        reformat["ypos"].setValue(1315)
        reformat["clamp"].setValue(1)
        if src_path:
            try:
                reformat["format"].setValue("basic_res")
            except:
                reformat["format"].setValue("%s"%back_up_format)
    else:
        reformat = nuke.createNode("Reformat")
        reformat["resize"].setValue(0)
        reformat.setInput(0, soften)
        reformat["xpos"].setValue(-9)
        reformat["ypos"].setValue(1315)
        reformat["clamp"].setValue(1)
        if src_path:
            try:
                reformat["format"].setValue("basic_res")
            except:
                reformat["format"].setValue("%s"%back_up_format)
    # block_d
    block_d = nuke.createNode("BackdropNode")
    block_d["xpos"].setValue(-76.0)
    block_d["ypos"].setValue(1162)
    block_d["bdheight"].setValue(275)
    block_d["bdwidth"].setValue(250)
    block_d["label"].setValue("distort")
    block_d["note_font_size"].setValue(20)
    block_d["tile_color"].setValue(1129690623)

    finalmerge = nuke.createNode("Merge2")
    if src_path:
        finalmerge.setInput(0, readfile)
    finalmerge.setInput(1, reformat)
    finalmerge["operation"].setValue("over")
    finalmerge['xpos'].setValue(-9)
    finalmerge['ypos'].setValue(1473)

    write = nuke.createNode("Write")
    write["file"].setValue(outpath)
    write["file_type"].setValue("exr")
    write.setInput(0, finalmerge)
    write['xpos'].setValue(-9)
    write['ypos'].setValue(1544)
