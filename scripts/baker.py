#python
'''
This script allows you to use xNormal within Modo
It uses xml bake settings files and runs them through xnormal.exe
All of these settings can be set from within Modo

'''
__author__ = 'Chris Sprance'
# import lx
import xml.etree.ElementTree as ET
import subprocess
import tempfile
import os, sys


class Baker(object):
	"""This Class Contains all the methods necessary to modify xml files based on settings and tweak and save the xml file"""
	def __init__(self):
		super(Baker, self).__init__()
		self.settings = self.parseXML()
		self.settings_file = 'testfile'
		self.hi_poly_settings = self.settings.find('HighPolyModel').find('Mesh').attrib
		self.lo_poly_settings = self.settings.find('LowPolyModel').find('Mesh').attrib
		self.generate_maps_settings = self.settings.find('GenerateMaps').attrib

	'''This grabs the default settings from the string if the xml file does not exist in the config directory'''
	def parseXML(self):
		# if the config doesn't exist create it
		if self.configExists():
			pass
		xmlfile = r'''<?xml version="1.0" encoding="UTF-8"?><Settings xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="3.18.10"><HighPolyModel DefaultMeshScale="16.000000"><Mesh Visible="true" Scale="10.000000" IgnorePerVertexColor="false" AverageNormals="AverageNormals" BaseTexIsTSNM="false" File="C:\pipeline_hi.obj" PositionOffset="0.0000;0.0000;0.0000" BaseTex="D:\perforce\GameSDK\Objects\weapons\craftedbow\textures\birch.tga"/></HighPolyModel><LowPolyModel DefaultMeshScale="16.000000"><Mesh Visible="true" File="C:\pipeline_bake.obj" AverageNormals="UseExportedNormals" MaxRayDistanceFront="0.322190" MaxRayDistanceBack="8.753330" UseCage="true" NormapMapType="Tangent-space" UsePerVertexColors="true" UseFresnel="false" FresnelRefractiveIndex="1.330000" ReflectHDRMult="1.000000" VectorDisplacementTS="false" VDMSwizzleX="X+" VDMSwizzleY="Y+" VDMSwizzleZ="Z+" BatchProtect="false" CastShadows="true" ReceiveShadows="true" BackfaceCull="true" NMSwizzleX="X+" NMSwizzleY="Y+" NMSwizzleZ="Z+" CageFile="C:\pipeline_cage.obj" HighpolyNormalsOverrideTangentSpace="false" TransparencyMode="None" AlphaTestValue="127" Matte="false" Scale="10.000000" MatchUVs="false" UOffset="0.000000" VOffset="0.000000" PositionOffset="0.0000;0.0000;0.0000"/></LowPolyModel><GenerateMaps GenNormals="true" Width="4096" Height="4096" EdgePadding="16" BucketSize="512" TangentSpace="true" ClosestIfFails="true" DiscardRayBackFacesHits="true" File="C:\pipeline.tga" SwizzleX="X+" SwizzleY="Y-" SwizzleZ="Z+" AA="1" BakeHighpolyBaseTex="false" BakeHighpolyBaseTextureDrawObjectIDIfNoTexture="true" GenHeights="false" HeightTonemap="Interactive" HeightTonemapMin="false" HeightTonemapMax="false" GenAO="false" AORaysPerSample="64" AODistribution="Uniform" AOConeAngle="179.500000" AOBias="0.080000" AOAllowPureOccluded="true" AOLimitRayDistance="false" AOAttenConstant="1.000000" AOAttenLinear="0.000000" AOAttenCuadratic="0.000000" AOJitter="false" AOIgnoreBackfaceHits="false" GenBent="false" BentRaysPerSample="128" BentConeAngle="162.000000" BentBias="0.080000" BentTangentSpace="false" BentLimitRayDistance="false" BentJitter="false" BentDistribution="Uniform" BentSwizzleX="X+" BentSwizzleY="Y+" BentSwizzleZ="Z+" GenPRT="false" PRTRaysPerSample="128" PRTConeAngle="179.500000" PRTBias="0.080000" PRTLimitRayDistance="false" PRTJitter="false" PRTNormalize="true" PRTThreshold="0.005000" GenProximity="false" ProximityRaysPerSample="128" ProximityConeAngle="80.000000" ProximityLimitRayDistance="true" ProximityFlipNormals="false" ProximityFlipValue="false" GenConvexity="false" ConvexityScale="1.000000" GenThickness="false" GenCavity="false" CavityRaysPerSample="900" CavityJitter="false" CavitySearchRadius="0.500000" CavityContrast="1.250000" CavitySteps="4" GenWireRays="false" RenderRayFails="true" RenderWireframe="true" GenDirections="false" DirectionsTS="false" DirectionsSwizzleX="X+" DirectionsSwizzleY="Y+" DirectionsSwizzleZ="Z+" DirectionsTonemap="Interactive" DirectionsTonemapMin="false" DirectionsTonemapMax="false" GenRadiosityNormals="false" RadiosityNormalsRaysPerSample="128" RadiosityNormalsDistribution="Uniform" RadiosityNormalsConeAngle="162.000000" RadiosityNormalsBias="0.080000" RadiosityNormalsLimitRayDistance="false" RadiosityNormalsAttenConstant="1.000000" RadiosityNormalsAttenLinear="0.000000" RadiosityNormalsAttenCuadratic="0.000000" RadiosityNormalsJitter="false" RadiosityNormalsContrast="1.000000" RadiosityNormalsEncodeAO="true" RadiosityNormalsCoordSys="AliB" RadiosityNormalsAllowPureOcclusion="false" BakeHighpolyVCols="false" GenCurv="false" CurvRaysPerSample="512" CurvBias="0.000100" CurvConeAngle="179.500000" CurvJitter="false" CurvSearchDistance="1.000000" CurvTonemap="Monocrome" CurvDistribution="Uniform" CurvAlgorithm="Average" CurvSmoothing="true" GenDerivNM="false" GenTranslu="false" TransluRaysPerSample="128" TransluDistribution="Cosine" TransluConeAngle="162.000000" TransluBias="0.000500" TransluDist="1.000000" TransluJitter="false"><NMBackgroundColor R="128" G="128" B="255"/><BakeHighpolyBaseTextureNoTexCol R="255" G="0" B="0"/><BakeHighpolyBaseTextureBackgroundColor R="74" G="45" B="13"/><HMBackgroundColor R="0" G="0" B="0"/><AOOccludedColor R="0" G="0" B="0"/><AOUnoccludedColor R="255" G="255" B="255"/><AOBackgroundColor R="255" G="255" B="255"/><BentBackgroundColor R="127" G="127" B="255"/><PRTBackgroundColor R="0" G="0" B="0"/><ProximityBackgroundColor R="255" G="255" B="255"/><ConvexityBackgroundColor R="255" G="255" B="255"/><CavityBackgroundColor R="255" G="255" B="255"/><RenderWireframeCol R="255" G="255" B="255"/><RenderCWCol R="0" G="0" B="255"/><RenderSeamCol R="0" G="255" B="0"/><RenderRayFailsCol R="255" G="0" B="0"/><RenderWireframeBackgroundColor R="0" G="0" B="0"/><VDMBackgroundColor R="0" G="0" B="0"/><RadNMBackgroundColor R="0" G="0" B="0"/><BakeHighpolyVColsBackgroundCol R="219" G="215" B="187"/><CurvBackgroundColor R="0" G="0" B="0"/><DerivNMBackgroundColor R="127" G="127" B="0"/><TransluBackgroundColor R="0" G="0" B="0"/></GenerateMaps><Detail Scale="0.500000" Method="4Samples"/><Viewer3D ShowGrid="true" ShowWireframe="false" ShowTangents="false" ShowNormals="false" ShowBlockers="false" MaxTessellationLevel="0" LightIntensity="1.000000" LightIndirectIntensity="0.000000" Exposure="0.180000" HDRThreshold="0.900000" UseGlow="true" GlowIntensity="1.000000" SSAOEnabled="false" SSAOBright="1.100000" SSAOContrast="1.000000" SSAOAtten="1.000000" SSAORadius="0.250000" SSAOBlurRadius="2.000000" ParallaxStrength="0.000000" ShowHighpolys="true" ShowAO="false" CageOpacity="0.700000" DiffuseGIIntensity="1.000000" CastShadows="false" ShadowBias="0.100000" ShadowArea="0.250000" AxisScl="0.040000" CameraOrbitDistance="0.500000" CameraOrbitAutoCenter="true" ShowStarfield="false"><LightAmbientColor R="33" G="33" B="33"/><LightDiffuseColor R="229" G="229" B="229"/><LightSpecularColor R="255" G="255" B="255"/><LightSecondaryColor R="0" G="0" B="0"/><LightTertiaryColor R="0" G="0" B="0"/><BackgroundColor R="0" G="0" B="0"/><GridColor R="180" G="180" B="220"/><CageColor R="76" G="76" B="76"/><CameraRotation e11="1.000000" e12="0.000000" e13="0.000000" e21="0.000000" e22="1.000000" e23="0.000000" e31="0.000000" e32="0.000000" e33="1.000000"/><CameraPosition x="0.000000" y="1.000000" z="0.000000"/><LightPosition x="0.000000" y="2.000000" z="5.000000"/></Viewer3D></Settings>'''
		tree = ET.fromstring(xmlfile)
		return tree

	'''This method writes settings from a dictionary of settings'''
	def writeXML(self):

		print ("XML File Written Successfully")
		tf = tempfile.NamedTemporaryFile(suffix='.xml')
		print (self.settings.tag)
		return tf.name

	def configExists(self):
		print(os.path.dirname(os.path.realpath(__file__)))
		if True:
			return True
	
	'''This kicks off the xNormal worker thread'''
	def startBake(self):
		x = self.writeXML()
		# Try To Kick off the xNormal worker fail silently
		try:
			retcode = subprocess.Popen('c:/program files (x86)/santiago orgaz/xnormal 3.17.9/x64/xnormal.exe %s' % self.settings_file )
			pass
		except:
			pass
		print ("Starting xNormal bake using %s" % x)

	'''Sends the settings dictionary to be written to the xml file'''
	def changeSettings(self, mesh_type, settings):
		pass

def main():
	# create our baker instance
	x = Baker()	
	x.startBake()
	print(x.settings)

if __name__ == '__main__':
	main()