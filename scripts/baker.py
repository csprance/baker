# python
'''
This script allows you to use xNormal within Modo
It uses xml bake settings files and runs them through xnormal.exe
All of these settings can be set from within Modo

'''
__author__ = 'Chris Sprance'
import xml.etree.ElementTree as ET
import subprocess
import tempfile
import os
import sys
import lx
import lxu.object


class Baker(object):

    """This Class Contains all the methods necessary to modify xml files based on settings and tweak and save the xml file"""

    def __init__(self):
        super(Baker, self).__init__()

        # this is the path to the settings file
        self.settings_file = lx.eval('user.value settings_file ?')

        self.xpath = lx.eval('user.value baker_xpath ?')

        # bake_settings.xml file for xNormal to run
        self.settings = self.parseXML()

        # hi poly settings
        self.hi_poly_settings = self.settings.find(
            'HighPolyModel').find('Mesh').attrib

        # low poly settings
        self.lo_poly_settings = self.settings.find(
            'LowPolyModel').find('Mesh').attrib
        # generate map settings
        self.generate_maps_settings = self.settings.find('GenerateMaps').attrib

        # path to xNormal
        self.xpath = lx.eval('user.value baker_xpath ?')

        # dictionary that contains all the user values
        self.user_values = self.get_user_values()

        # this is the base directory of the kit
        self.BASE_PATH = (lx.eval(
            'query platformservice path.path ? scripts') + "\\baker").replace("\\", "/")

    def get_user_values(self):
        user_values = dict()

        uv = ['low_poly_mesh', 'hi_poly_mesh', 'cage_mesh', 'settings_file', 'baker_ao_map', 'baker_norm_map', 'baker_cavity_map',
              'baker_norm_map', 'baker_tangent_space', 'baker_edge_padding', 'baker_map_size_x', 'baker_map_size_y', 'baker_map_output']

        for x in uv:
            user_values[x] = lx.eval('user.value %s ?' % x)
        return user_values

    def parseXML(self):
        bake_settings = open(self.settings_file)
        tree = ET.parse(bake_settings).getroot()
        return tree

    def writeXML(self):
        '''This method writes settings from the settings dictionary'''
        # open the settings file
        f = open(self.settings_file + '_bake', 'w+')
        # write the file using utf-8 encoding
        f.write(ET.tostring(self.settings, encoding='UTF-8'))
        f.close()
        return f

    def set_user_values(self):
        self.lo_poly_settings['File'] = self.user_values['low_poly_mesh']
        self.lo_poly_settings['CageFile'] = self.user_values['cage_mesh']
        self.hi_poly_settings['File'] = self.user_values['hi_poly_mesh']
        self.generate_maps_settings['EdgePadding'] = str(
            self.user_values['baker_edge_padding'])
        self.generate_maps_settings[
            'File'] = self.user_values['baker_map_output']
        self.generate_maps_settings['GenNormals'] = 'true' if self.user_values[
            'baker_norm_map'] == 1 else 'false'
        self.generate_maps_settings['GenAO'] = 'true' if self.user_values[
            'baker_ao_map'] == 1 else 'false'
        self.generate_maps_settings['GenCavity'] = 'true' if self.user_values[
            'baker_cavity_map'] == 1 else 'false'
        self.generate_maps_settings['TangentSpace'] = 'true' if self.user_values[
            'baker_tangent_space'] == 1 else 'false'

        if self.user_values['baker_map_size_x'] == '0':
            self.generate_maps_settings['Width'] = str(256)
        elif self.user_values['baker_map_size_x'] == '1':
            self.generate_maps_settings['Width'] = str(512)
        elif self.user_values['baker_map_size_x'] == '2':
            self.generate_maps_settings['Width'] = str(1024)
        elif self.user_values['baker_map_size_x'] == '3':
            self.generate_maps_settings['Width'] = str(2048)
        elif self.user_values['baker_map_size_x'] == '4':
            self.generate_maps_settings['Width'] = str(4096)
        elif self.user_values['baker_map_size_x'] == '5':
            self.generate_maps_settings['Width'] = str(8192)

        if self.user_values['baker_map_size_y'] == '0':
            self.generate_maps_settings['Height'] = str(256)
        elif self.user_values['baker_map_size_y'] == '1':
            self.generate_maps_settings['Height'] = str(512)
        elif self.user_values['baker_map_size_y'] == '2':
            self.generate_maps_settings['Height'] = str(1024)
        elif self.user_values['baker_map_size_y'] == '3':
            self.generate_maps_settings['Height'] = str(2048)
        elif self.user_values['baker_map_size_y'] == '4':
            self.generate_maps_settings['Height'] = str(4096)
        elif self.user_values['baker_map_size_y'] == '5':
            self.generate_maps_settings['Height'] = str(8192)

        #self.generate_maps_settings['Height'] = self.user_values['baker_map_size_y']

    def startBake(self):
        '''This kicks off the xNormal worker thread'''
        self.set_user_values()
        config_file = self.writeXML()
        # Try To Kick off the xNormal worker fail silently
        try:
            subprocess.Popen(
                str(self.xpath + ' ' + self.settings_file + '_bake'))
            return config_file
        except:
            lx.out("Bake Failed Please Check Settings and try again")

'''
Start the main thread off

'''


def main():
    # create our baker instance
    x = Baker()
    config = x.startBake()
    lx.out(config.name)


if __name__ == '__main__':
    main()
