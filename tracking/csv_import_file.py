#coding=utf-8
import csv
import os
import nuke

def main():
    csv_path = nuke.getFilename("get the csv file", "*.csv")
    if not csv_path or not csv_path.endswith(".csv"):
        nuke.message("Select csv file please")
        return
    print csv_path
    project_path = nuke.getFilename("select folder")
    print(project_path)
    if not project_path or not project_path.endswith("sequences") and not project_path.endswith("sequences/"):
        nuke.message("Select sequence folder")
        return
    shot_list = []
    first = r"3d\tracking\sourceimages"
    second = r"elements\iplate"
    with open(csv_path, mode="r") as file_in:
        reader = csv.reader(file_in)
        for rows in reader:
            if rows[0]:
                shot_list.append(rows[0])

    id = 1
    for shot in shot_list:
        shot = "dp_%s" % shot
        shot_path = os.path.join(project_path, shot)
        if os.path.exists(shot_path):
            path_test = os.path.join(shot_path, first)
            if os.listdir(path_test):
                version = max(os.listdir(path_test))
                version_path = os.path.join(path_test, version)
                print version_path
            else:
                path_test = os.path.join(shot_path, second)
                version = max(os.listdir(path_test))
                version_path = os.path.join(path_test, version)
                print version_path
            file = [x for x in nuke.getFileNameList(version_path) if not ".ifl" in x and not ".db" in x][0]
            pathfile = os.path.join(version_path, file)
            read_node = nuke.createNode("Read")
            read_node['file'].fromUserText(pathfile)
            read_node["xpos"].setValue(100 * (id % 5))
            read_node["ypos"].setValue(100 * (id / 5))
            id += 1
