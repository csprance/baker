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

        uv = [
        'low_poly_mesh', #low poly mesh
        'baker_xpath',
        'hi_poly_mesh', # hi poly mesh
        'cage_mesh', #cage mesh
        'settings_file', # where the settings file is stored at
        'baker_overwrite_warn',
        'baker_bucket_size',
        'baker_aa',
				'baker_map_size_x', # what size to output the width
				'baker_map_size_y', # what size to output the height
				'baker_map_output', # where to output the maps to
				'baker_edge_padding',              
        'baker_height_map' , #bool bake height map
        'baker_height_normalization' , # method used to normalize height map
        'baker_base_texture_map', # bool bake base texture
        'baker_ao_map', #bool bake AO
				'baker_ao_rays', #int num rays
				'baker_ao_distribution', # list choice
				'baker_ao_bias', # int
				'baker_ao_spread_angle', # int
				'baker_ao_limit_ray_distance', # bool 
				'baker_ao_attenuation_x', #int 
				'baker_ao_attenuation_y', # int
				'baker_ao_attenuation_z', # int
				'baker_ao_jitter', 
				'baker_ao_ignore_backface_hits', 
				'baker_ao_allow_full_occlusion', 
        'baker_cavity_map', 
        'baker_cavity_rays',
        'baker_cavity_radius',
        'baker_cavity_contrast',
        'baker_cavity_steps',
				'baker_norm_map', 
				'baker_tangent_space', 
				'baker_norm_swiz_x', 
				'baker_norm_swiz_y',
				'baker_norm_swiz_z',
				'baker_curvature_map', # bool bake curvature map
				'baker_curvature_rays', # 
				'baker_curvature_jitter', # 
				'baker_curvature_bias', # 
				'baker_curvature_spread_angle', # 
				'baker_curvature_algorithm', # 
				'baker_curvature_distribution', # 
				'baker_curvature_search_distance', # 
				'baker_curvature_tone_mapping', # 
				'baker_curvature_smoothing', # 
				]

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
		

		baker_sizes = {'0':'256','1':'512','2':'1024','3':'2048','4':'4096','5':'8192',}

        self.generate_maps_settings['Width'] = bake_sizes[self.user_values['baker_map_size_x']]
        self.generate_maps_settings['Height'] = bake_sizes[self.user_values['baker_map_size_y']]
        
        # if self.user_values['baker_map_size_x'] == '0':
        #     self.generate_maps_settings['Width'] = str(256)
        # elif self.user_values['baker_map_size_x'] == '1':
        #     self.generate_maps_settings['Width'] = str(512)
        # elif self.user_values['baker_map_size_x'] == '2':
        #     self.generate_maps_settings['Width'] = str(1024)
        # elif self.user_values['baker_map_size_x'] == '3':
        #     self.generate_maps_settings['Width'] = str(2048)
        # elif self.user_values['baker_map_size_x'] == '4':
        #     self.generate_maps_settings['Width'] = str(4096)
        # elif self.user_values['baker_map_size_x'] == '5':
        #     self.generate_maps_settings['Width'] = str(8192)

        # if self.user_values['baker_map_size_y'] == '0':
        #     self.generate_maps_settings['Height'] = str(256)
        # elif self.user_values['baker_map_size_y'] == '1':
        #     self.generate_maps_settings['Height'] = str(512)
        # elif self.user_values['baker_map_size_y'] == '2':
        #     self.generate_maps_settings['Height'] = str(1024)
        # elif self.user_values['baker_map_size_y'] == '3':
        #     self.generate_maps_settings['Height'] = str(2048)
        # elif self.user_values['baker_map_size_y'] == '4':
        #     self.generate_maps_settings['Height'] = str(4096)
        # elif self.user_values['baker_map_size_y'] == '5':
        #     self.generate_maps_settings['Height'] = str(8192)

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
    lx.out(x.BASE_PATH)


if __name__ == '__main__':
    main()
