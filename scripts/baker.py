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
        self.generate_maps_settings = self.settings.find(
            'GenerateMaps').attrib

        # path to xNormal
        self.xpath = lx.eval('user.value baker_xpath ?')

        # dictionary that contains all the user values
        self.user_values = self.get_user_values()

        # this is the base directory of the kit
        self.BASE_PATH 	= (lx.eval('query platformservice path.path ? scripts') + "\\baker").replace("\\", "/")

    def get_user_values(self):
        user_values = dict()
        uv = ['low_poly_mesh', 'hi_poly_mesh', 'cage_mesh', 'settings_file', 'baker_ao_map', 'baker_norm_map', 'baker_cavity_map',
              'baker_norm_map', 'baker_tangent_space', 'baker_edge_padding', 'baker_map_size_x', 'baker_map_size_y']
        for x in uv:
            if x == 'baker_map_size_y' or x == 'baker_map_size_x':
                user_values[x] = lx.eval('user.value %s ?' % x)
            else:
                user_values[x] = lx.eval('user.value %s ?' % x)
        return user_values

    def parseXML(self):
        bake_settings = open(self.settings_file)
        tree = ET.parse(bake_settings).getroot()
        return tree

    def writeXML(self):
        '''This method writes settings from a dictionary of settings'''

        lx.out("XML File Written Successfully")
        tf = tempfile.NamedTemporaryFile(suffix='.xml', delete=False)
        tf.write(xmlstring)
        return tf.name

    def startBake(self):
        '''This kicks off the xNormal worker thread'''
        x = self.writeXML()
        # Try To Kick off the xNormal worker fail silently
        try:
            #retcode = subprocess.Popen(str(self.xpath+ ' ' + self.settings_file ))
            retcode = 'Opening xNormal (SimulaTED)'
            lx.out(retcode)
        except:
            lx.out("Bake Failed Please Check Settings and try again")
            pass
        lx.out("Starting xNormal bake at %s using %s" % (self.xpath, x))

'''
Start the main thread off

'''


def main():
    # create our baker instance
    x = Baker()
    lx.out(x.user_values)


if __name__ == '__main__':
    main()
