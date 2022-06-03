# Cantilever Shell1

from abaqus import *
from abaqusConstants import *
import regionToolset

session.viewports['Viewport: 1'].setValues(displayedObject=None)

# ---------------------------------------------------------------
# Create the model
mdb.models.changeKey(fromName='Model-1', toName='Uniform Tank')
tankModel = mdb.models['Uniform Tank']

# ---------------------------------------------------------------
# Create the part

import sketch
import part

# a)Create a 3D deformable part named "Tank" using the sketch
tankPart = tankModel.Part(name='Tank', dimensionality=THREE_D,
                          type=DEFORMABLE_BODY)
tankPart.ReferencePoint(point=(0, 0, 0))
the_reference_point = tankPart.referencePoints[1]

# b)Sketch the tank cross section

tankProfileSketch = tankModel.ConstrainedSketch(name='Tank CS Profile',
                                                sheetSize=32000)
tankProfileSketch.CircleByCenterPerimeter(center=(0, 0), point1=(32000, 0))


tankPart.BaseShellExtrude(sketch=tankProfileSketch, depth=12200)

# ----------------------------------------------------------------
# Create material
import material

# Create material ASTM A36 Steel by assigning mass density, youngs
# modulus and poissons ratio
tankMaterial = tankModel.Material(name='ASTM A36 USin')
tankMaterial.Density(table=((0.284, ),     ))
tankMaterial.Elastic(table=((2.9E7, 0.3), ))

# ----------------------------------------------------------------
# Create homogeneous shell section of specific thickness and assign the tankMaterial to it

import section

# First Partition: Create a Datum plane to partition the shell 
tankPart.DatumPointByOffset(point=the_reference_point, vector=(32000, 0, 2440))
tankPart.DatumPointByOffset(point=the_reference_point, vector=(0, 32000, 2440))
tankPart.DatumPointByOffset(point=the_reference_point, vector=(-32000, 0, 2440))

tankPart_datums_keys = tankPart.datums.keys()
tankPart_datums_keys.sort()
tankPart_datums_point_1 = tankPart.datums[tankPart_datums_keys[2]]
tankPart_datums_point_2 = tankPart.datums[tankPart_datums_keys[1]]
tankPart_datums_point_3 = tankPart.datums[tankPart_datums_keys[0]]
tankPart.DatumPlaneByThreePoints(point1=tankPart_datums_point_1,
                                 point2=tankPart_datums_point_2,
                                 point3=tankPart_datums_point_3)
tankPart.DatumAxisByPrincipalAxis(principalAxis=ZAXIS)

tankPart_datums_keys = tankPart.datums.keys()
tankPart_datums_keys.sort()
index_of_plane = (len(tankPart_datums_keys)-2)
index_of_axis = (len(tankPart_datums_keys)-1)
tank_datum_plane = tankPart.datums[tankPart_datums_keys[index_of_plane]]
tank_datum_axis = tankPart.datums[tankPart_datums_keys[index_of_axis]]
# Select the face to be partitioned
partition_face_pt = (32000, 0, 1220)
partition_face = tankPart.faces.findAt((partition_face_pt,))
tankPart.PartitionFaceByDatumPlane(faces=partition_face,
                                   datumPlane=tank_datum_plane)

# Second partition
tankPart.DatumPlaneByOffset(plane=tank_datum_plane, flip=SIDE2, offset=2440)
tankPart_datums_keys = tankPart.datums.keys()
tankPart_datums_keys.sort()
index_of_plane2 = (len(tankPart_datums_keys)-1)
tank_datum_plane2 = tankPart.datums[tankPart_datums_keys[index_of_plane2]]
# Select the second face to be partitioned
partition_face_pt2 = (32000, 0, 3660)
partition_face2 = tankPart.faces.findAt((partition_face_pt2,))
tankPart.PartitionFaceByDatumPlane(faces=partition_face2,
                                   datumPlane=tank_datum_plane2)

# Third partition
tankPart.DatumPlaneByOffset(plane=beam_datum_plane2, flip=SIDE1, offset=2440)
tankPart_datums_keys = tankPart.datums.keys()
tankPart_datums_keys.sort()
index_of_plane3 = (len(tankPart_datums_keys)-1)
tank_datum_plane3 = tankPart.datums[tankPart_datums_keys[index_of_plane3]]
# Select the second face to be partitioned
partition_face_pt3 = (32000, 0, 6100)
partition_face3 = tankPart.faces.findAt((partition_face_pt3,))
tankPart.PartitionFaceByDatumPlane(faces=partition_face3,
                                   datumPlane=tank_datum_plane3)

# Fourth partition
tankPart.DatumPlaneByOffset(plane=beam_datum_plane3, flip=SIDE1, offset=2440)
tankPart_datums_keys = tankPart.datums.keys()
tankPart_datums_keys.sort()
index_of_plane4 = (len(tankPart_datums_keys)-1)
tank_datum_plane4 = tankPart.datums[tankPart_datums_keys[index_of_plane4]]
# Select the second face to be partitioned
partition_face_pt4 = (32000, 0, 8540)
partition_face4 = tankPart.faces.findAt((partition_face_pt4,))
tankPart.PartitionFaceByDatumPlane(faces=partition_face4,
                                   datumPlane=tank_datum_plane4)

# Create a section to assign to the beam
tankSection1 = tankModel.HomogeneousShellSection(name='Shell Section1',
                                                material='ASTM A36 USin',
                                                thicknessType=UNIFORM,
                                                thickness=23.44)
tankSection2 = tankModel.HomogeneousShellSection(name='Shell Section2',
                                                material='ASTM A36 USin',
                                                thicknessType=UNIFORM,
                                                thickness=17.75)
tankSection3 = tankModel.HomogeneousShellSection(name='Shell Section3',
                                                material='ASTM A36 USin',
                                                thicknessType=UNIFORM,
                                                thickness=13.16)
tankSection4 = tankModel.HomogeneousShellSection(name='Shell Section4',
                                                material='ASTM A36 USin',
                                                thicknessType=UNIFORM,
                                                thickness=9.53)
tankSection5 = tankModel.HomogeneousShellSection(name='Shell Section5',
                                                material='ASTM A36 USin',
                                                thicknessType=UNIFORM,
                                                thickness=9.53)

# Assign the shell to this section
tank_face_point1 = (32000, 0, 1220)
tank_face1 = tankPart.faces.findAt((tank_face_point1,))
tank_region1 = (tank_face1,)
tankPart.SectionAssignment(region=tank_region1,  sectionName='Shell Section1',
                           offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='')
tank_face_point2 = (32000, 0, 3660)
tank_face2 = tankPart.faces.findAt((tank_face_point2,))
tank_region2 = (tank_face2,)
tankPart.SectionAssignment(region=tank_region2,  sectionName='Shell Section2',
                           offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='')
tank_face_point3 = (32000, 0, 6100)
tank_face3 = tankPart.faces.findAt((tank_face_point3,))
tank_region3 = (tank_face3,)
tankPart.SectionAssignment(region=tank_region3,  sectionName='Shell Section3',
                           offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='')
tank_face_point4 = (32000, 0, 8540)
tank_face4 = tankPart.faces.findAt((tank_face_point4,))
tank_region4 = (tank_face4,)
tankPart.SectionAssignment(region=tank_region4,  sectionName='Shell Section4',
                           offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='')
tank_face_point5 = (32000, 0, 10980)
tank_face5 = tankPart.faces.findAt((tank_face_point5,))
tank_region5 = (tank_face5,)
tankPart.SectionAssignment(region=tank_region5,  sectionName='Shell Section5',
                           offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='')
# -----------------------------------------------------------------
# Create the assembly

import assembly

# Create the part instance
tankAssembly = tankModel.rootAssembly
tankInstance = tankAssembly.Instance(name='Shell Instance', part=tankPart,
                                     dependent=ON)

# -------------------------------------------------------------------
# Create the step

import step

# Create a static general step
tankModel.StaticStep(name='Apply Load', previous='Initial',
                     description='Load is applied during this step',
                     nlgeom=ON)

# --------------------------------------------------------------------
# Create the field output request

# Change the name of field output request 'F-Output-1' to 'Selected Field Outputs'
tankModel.fieldOutputRequests.changeKey(fromName='F-Output-1',
                                        toName='Selected Field Outputs')

# Since F-Output-1 is applied at the 'Apply Load' step by default, 'Selected Field Outputs' will be too
# We only need to set the required variables
tankModel.fieldOutputRequests['Selected Field Outputs'].setValues(variables=('S', 'E', 'PEMAG', 'U', 'RF', 'CF'))

# ---------------------------------------------------------------------------
# Create the history output request
# Create a new history output request called 'Default History Outputs' and assign both the step and the variables

tankModel.HistoryOutputRequest(name='Default History Outputs',
                               createStepName='Apply Load', variables=PRESELECT)

# Now delete the original history output request 'H-Output-1'
del tankModel.historyOutputRequests['H-Output-1']


# -----------------------------------------------------------------------------------
# Apply pin boundary condition to one end

pinned_edge = tankInstance.edges.findAt(((32000, 0, 0), ))
pinned_edge_region = regionToolset.Region(edges=pinned_edge)

tankModel.DisplacementBC(name='PinnedEdge', createStepName='Initial',
                         region=pinned_edge_region, u1=SET, u2=SET, u3=SET,
                         ur1=UNSET, ur2=UNSET, ur3=UNSET,
                         amplitude=UNSET, distributionType=UNIFORM,
                         fieldName='', localCsys=None)


# -----------------------------------------------------------------------------
# Apply plastic moment
moment_edge = tankInstance.edges.findAt(((-32000, 0, 0), ))
moment_edge_region = regionToolset.Region(side1Edges=moment_edge)
tankModel.ShellEdgeLoad(name='Plastic moment', createStepName='Apply Load',
region=moment_edge_region, magnitude=1, traction=MOMENT)
# Apply internal pressure to shell

shell_face_point1 = (32000, 0, 10980)
shell_face1 = tankInstance.faces.findAt((shell_face_point1,))
shell_face_point2 = (32000, 0, 8540)
shell_face2 = tankInstance.faces.findAt((shell_face_point2,))
shell_face_point3 = (32000, 0, 6100)
shell_face3 = tankInstance.faces.findAt((shell_face_point3,))
shell_face_point4 = (32000, 0, 3660)
shell_face4 = tankInstance.faces.findAt((shell_face_point4,))
shell_face_point5 = (32000, 0, 1220)
shell_face5 = tankInstance.faces.findAt((shell_face_point5,))
shell_face_region1 = regionToolset.Region(side2Faces=shell_face1)
shell_face_region2 = regionToolset.Region(side2Faces=shell_face2)
shell_face_region3 = regionToolset.Region(side2Faces=shell_face3)
shell_face_region4 = regionToolset.Region(side2Faces=shell_face4)
shell_face_region5 = regionToolset.Region(side2Faces=shell_face5)
# Here we apply uniform pressure
tankModel.Pressure(name='Hydrostatic Applied Pressure1', createStepName='Apply Load',
                   region=shell_face_region1, distributionType=HYDROSTATIC, magnitude=0.09,
                   hZero=12200, hReference=0, amplitude=UNSET)
tankModel.Pressure(name='Hydrostatic Applied Pressure2', createStepName='Apply Load',
                   region=shell_face_region2, distributionType=HYDROSTATIC, magnitude=0.09,
                   hZero=12200, hReference=0, amplitude=UNSET)
tankModel.Pressure(name='Hydrostatic Applied Pressure3', createStepName='Apply Load',
                   region=shell_face_region3, distributionType=HYDROSTATIC, magnitude=0.09,
                   hZero=12200, hReference=0, amplitude=UNSET)
tankModel.Pressure(name='Hydrostatic Applied Pressure4', createStepName='Apply Load',
                   region=shell_face_region4, distributionType=HYDROSTATIC, magnitude=0.09,
                   hZero=12200, hReference=0, amplitude=UNSET)
tankModel.Pressure(name='Hydrostatic Applied Pressure5', createStepName='Apply Load',
                   region=shell_face_region5, distributionType=HYDROSTATIC, magnitude=0.09,
                   hZero=12200, hReference=0, amplitude=UNSET)
# ------------------------------------------------------------------------------------
# Create the mesh

import mesh

# Set element type
elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=STANDARD)

tankPart.setElementType(regions=shell_face_region1, elemTypes=(elemType1,))
tankPart.setElementType(regions=shell_face_region2, elemTypes=(elemType1,))
tankPart.setElementType(regions=shell_face_region3, elemTypes=(elemType1,))
tankPart.setElementType(regions=shell_face_region4, elemTypes=(elemType1,))
tankPart.setElementType(regions=shell_face_region5, elemTypes=(elemType1,))
# Seed edges by number

mesh_edges_horizontal = tankPart.edges.findAt(((32000, 0, 0), ),
                                              ((32000, 0, 2440), ),
                                              ((32000, 0, 4880), ),
                                              ((32000, 0, 7320), ),
                                              ((32000, 0, 9760), ),
                                              ((32000, 0, 12200), ),)
tankPart.seedEdgeByNumber(edges=mesh_edges_horizontal, number=1000)
tankPart.generateMesh()

# ------------------------------------------------------------------------------------
# Create and run the job

import job

# Create the job
mdb.Job(name='UniformShellJob', model='Uniform Tank', type=ANALYSIS,
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE,
        description='Job simulates a loaded tank',
        parallelizationMethodExplicit=DOMAIN, multiprocessingMode=DEFAULT,
        numDomains=1, userSubroutine='', numCpus=1, memory=50,
        memoryUnits=PERCENTAGE, scratch='', echoPrint=OFF, modelPrint=OFF,
        contactPrint=OFF, historyPrint=OFF)

# Run the job
mdb.jobs['UniformShellJob'].submit(consistencyChecking=OFF)

# Do not return control till job is finished running
mdb.jobs['UniformShellJob'].waitForCompletion()

# End of run job
# -----------------------------------------------------------------------------------
# Post processing

import visualization

tank_viewport = session.Viewport(name='Tank Results Viewport')
shell_Odb_Path = 'UniformShellJob.odb'
an_odb_object = session.openOdb(name=shell_Odb_Path)
tank_viewport.setValues(displayedObject=an_odb_object)
tank_viewport.odbDisplay.display.setValues(plotState=(DEFORMED,))

