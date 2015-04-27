#python
'''
This script allows you to use xNormal within Modo
It uses xml bake settings files and runs them through xnormal.exe
All of these settings can be set from within Modo

'''
__author__ = 'Chris Sprance'
import lx
import xml.etree.ElementTree as ET
import subprocess
import tempfile
import os, sys

settings = dict()
class Baker(object):
	"""This Class Contains all the methods necessary to modify xml files based on settings and tweak and save the xml file"""
	def __init__(self):
		super(Baker, self).__init__()
		self.settings = self.parseXML()
		self.settings_file = str()
		self.xpath = str()
		self.hi_poly_settings = self.settings.find('HighPolyModel').find('Mesh').attrib
		self.lo_poly_settings = self.settings.find('LowPolyModel').find('Mesh').attrib
		self.generate_maps_settings = self.settings.find('GenerateMaps').attrib
		self.settings_path = str()

	
	def parseXML(self):
		xmlfile = r'''<?xml version="1.0" encoding="UTF-8"?>
<Settings Version="3.18.10" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
	<HighPolyModel DefaultMeshScale="16.000000">
		<Mesh AverageNormals="AverageNormals" BaseTex="D:\perforce\GameSDK\Objects\weapons\craftedbow\textures\birch.tga" BaseTexIsTSNM="false" File="C:\pipeline_hi.obj" IgnorePerVertexColor="false" PositionOffset="0.0000;0.0000;0.0000" Scale="10.000000" Visible="true"/>
	</HighPolyModel>
	<LowPolyModel DefaultMeshScale="16.000000">
		<Mesh AlphaTestValue="127" AverageNormals="UseExportedNormals" BackfaceCull="true" BatchProtect="false" CageFile="C:\pipeline_cage.obj" CastShadows="true" File="C:\pipeline_bake.obj" FresnelRefractiveIndex="1.330000" HighpolyNormalsOverrideTangentSpace="false" MatchUVs="false" Matte="false" MaxRayDistanceBack="8.753330" MaxRayDistanceFront="0.322190" NMSwizzleX="X+" NMSwizzleY="Y+" NMSwizzleZ="Z+" NormapMapType="Tangent-space" PositionOffset="0.0000;0.0000;0.0000" ReceiveShadows="true" ReflectHDRMult="1.000000" Scale="10.000000" TransparencyMode="None" UOffset="0.000000" UseCage="true" UseFresnel="false" UsePerVertexColors="true" VDMSwizzleX="X+" VDMSwizzleY="Y+" VDMSwizzleZ="Z+" VOffset="0.000000" VectorDisplacementTS="false" Visible="true"/>
	</LowPolyModel>
	<GenerateMaps AA="1" AOAllowPureOccluded="true" AOAttenConstant="1.000000" AOAttenCuadratic="0.000000" AOAttenLinear="0.000000" AOBias="0.080000" AOConeAngle="179.500000" AODistribution="Uniform" AOIgnoreBackfaceHits="false" AOJitter="false" AOLimitRayDistance="false" AORaysPerSample="64" BakeHighpolyBaseTex="false" BakeHighpolyBaseTextureDrawObjectIDIfNoTexture="true" BakeHighpolyVCols="false" BentBias="0.080000" BentConeAngle="162.000000" BentDistribution="Uniform" BentJitter="false" BentLimitRayDistance="false" BentRaysPerSample="128" BentSwizzleX="X+" BentSwizzleY="Y+" BentSwizzleZ="Z+" BentTangentSpace="false" BucketSize="512" CavityContrast="1.250000" CavityJitter="false" CavityRaysPerSample="900" CavitySearchRadius="0.500000" CavitySteps="4" ClosestIfFails="true" ConvexityScale="1.000000" CurvAlgorithm="Average" CurvBias="0.000100" CurvConeAngle="179.500000" CurvDistribution="Uniform" CurvJitter="false" CurvRaysPerSample="512" CurvSearchDistance="1.000000" CurvSmoothing="true" CurvTonemap="Monocrome" DirectionsSwizzleX="X+" DirectionsSwizzleY="Y+" DirectionsSwizzleZ="Z+" DirectionsTS="false" DirectionsTonemap="Interactive" DirectionsTonemapMax="false" DirectionsTonemapMin="false" DiscardRayBackFacesHits="true" EdgePadding="16" File="C:\pipeline.tga" GenAO="false" GenBent="false" GenCavity="false" GenConvexity="false" GenCurv="false" GenDerivNM="false" GenDirections="false" GenHeights="false" GenNormals="true" GenPRT="false" GenProximity="false" GenRadiosityNormals="false" GenThickness="false" GenTranslu="false" GenWireRays="false" Height="4096" HeightTonemap="Interactive" HeightTonemapMax="false" HeightTonemapMin="false" PRTBias="0.080000" PRTConeAngle="179.500000" PRTJitter="false" PRTLimitRayDistance="false" PRTNormalize="true" PRTRaysPerSample="128" PRTThreshold="0.005000" ProximityConeAngle="80.000000" ProximityFlipNormals="false" ProximityFlipValue="false" ProximityLimitRayDistance="true" ProximityRaysPerSample="128" RadiosityNormalsAllowPureOcclusion="false" RadiosityNormalsAttenConstant="1.000000" RadiosityNormalsAttenCuadratic="0.000000" RadiosityNormalsAttenLinear="0.000000" RadiosityNormalsBias="0.080000" RadiosityNormalsConeAngle="162.000000" RadiosityNormalsContrast="1.000000" RadiosityNormalsCoordSys="AliB" RadiosityNormalsDistribution="Uniform" RadiosityNormalsEncodeAO="true" RadiosityNormalsJitter="false" RadiosityNormalsLimitRayDistance="false" RadiosityNormalsRaysPerSample="128" RenderRayFails="true" RenderWireframe="true" SwizzleX="X+" SwizzleY="Y-" SwizzleZ="Z+" TangentSpace="true" TransluBias="0.000500" TransluConeAngle="162.000000" TransluDist="1.000000" TransluDistribution="Cosine" TransluJitter="false" TransluRaysPerSample="128" Width="4096">
		<NMBackgroundColor B="255" G="128" R="128"/>
		<BakeHighpolyBaseTextureNoTexCol B="0" G="0" R="255"/>
		<BakeHighpolyBaseTextureBackgroundColor B="13" G="45" R="74"/>
		<HMBackgroundColor B="0" G="0" R="0"/>
		<AOOccludedColor B="0" G="0" R="0"/>
		<AOUnoccludedColor B="255" G="255" R="255"/>
		<AOBackgroundColor B="255" G="255" R="255"/>
		<BentBackgroundColor B="255" G="127" R="127"/>
		<PRTBackgroundColor B="0" G="0" R="0"/>
		<ProximityBackgroundColor B="255" G="255" R="255"/>
		<ConvexityBackgroundColor B="255" G="255" R="255"/>
		<CavityBackgroundColor B="255" G="255" R="255"/>
		<RenderWireframeCol B="255" G="255" R="255"/>
		<RenderCWCol B="255" G="0" R="0"/>
		<RenderSeamCol B="0" G="255" R="0"/>
		<RenderRayFailsCol B="0" G="0" R="255"/>
		<RenderWireframeBackgroundColor B="0" G="0" R="0"/>
		<VDMBackgroundColor B="0" G="0" R="0"/>
		<RadNMBackgroundColor B="0" G="0" R="0"/>
		<BakeHighpolyVColsBackgroundCol B="187" G="215" R="219"/>
		<CurvBackgroundColor B="0" G="0" R="0"/>
		<DerivNMBackgroundColor B="0" G="127" R="127"/>
		<TransluBackgroundColor B="0" G="0" R="0"/>
	</GenerateMaps>
	<Detail Method="4Samples" Scale="0.500000"/>
	<Viewer3D AxisScl="0.040000" CageOpacity="0.700000" CameraOrbitAutoCenter="true" CameraOrbitDistance="0.500000" CastShadows="false" DiffuseGIIntensity="1.000000" Exposure="0.180000" GlowIntensity="1.000000" HDRThreshold="0.900000" LightIndirectIntensity="0.000000" LightIntensity="1.000000" MaxTessellationLevel="0" ParallaxStrength="0.000000" SSAOAtten="1.000000" SSAOBlurRadius="2.000000" SSAOBright="1.100000" SSAOContrast="1.000000" SSAOEnabled="false" SSAORadius="0.250000" ShadowArea="0.250000" ShadowBias="0.100000" ShowAO="false" ShowBlockers="false" ShowGrid="true" ShowHighpolys="true" ShowNormals="false" ShowStarfield="false" ShowTangents="false" ShowWireframe="false" UseGlow="true">
		<LightAmbientColor B="33" G="33" R="33"/>
		<LightDiffuseColor B="229" G="229" R="229"/>
		<LightSpecularColor B="255" G="255" R="255"/>
		<LightSecondaryColor B="0" G="0" R="0"/>
		<LightTertiaryColor B="0" G="0" R="0"/>
		<BackgroundColor B="0" G="0" R="0"/>
		<GridColor B="220" G="180" R="180"/>
		<CageColor B="76" G="76" R="76"/>
		<CameraRotation e11="1.000000" e12="0.000000" e13="0.000000" e21="0.000000" e22="1.000000" e23="0.000000" e31="0.000000" e32="0.000000" e33="1.000000"/>
		<CameraPosition x="0.000000" y="1.000000" z="0.000000"/>
		<LightPosition x="0.000000" y="2.000000" z="5.000000"/>
	</Viewer3D>
</Settings>'''
		tree = ET.fromstring(xmlfile)
		#config = open(self.settings_file, 'w+')
		return tree
	
	def writeXML(self):
		'''This method writes settings from a dictionary of settings'''
		print ("XML File Written Successfully")
		tf = tempfile.NamedTemporaryFile(suffix='.xml')
		print (self.settings.tag)
		return tf.name

	def configExists(self):
		print(os.path.dirname(os.path.realpath(__file__)))
		if True:
			return True
	
	
	def startBake(self):
		'''This kicks off the xNormal worker thread'''
		x = self.writeXML()
		# Try To Kick off the xNormal worker fail silently
		try:
			retcode = subprocess.Popen(str(self.xpath+ ' ' + self.settings_file ))
			pass
		except:
			pass
		print ("Starting xNormal bake at %s using %s" % (self.xpath, x))


	def changeSettings(self, mesh_type, settings):
		'''Sends the settings dictionary to be written to the xml file'''
		pass

'''
Start the main thread off

'''


def main():
	# create our baker instance
	x = Baker()	
	# set the path for xnormal
	x.xpath = 'c:/program files (x86)/santiago orgaz/x64/xnormal.exe'
	# where do we want to store our file for the settings or if it already exists it will use that file
	x.settings_file = 'c:/baker'
	x.startBake()
	x.changeSettings
	print x.xpath
if __name__ == '__main__':
	main()