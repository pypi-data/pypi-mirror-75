import sys
import typing
import mathutils
import bpy.context
import mathutils.bvhtree


class EXP_PyObjectPlus:
    ''' EXP_PyObjectPlus base class of most other types in the Game Engine.
    '''

    invalid: bool = None
    ''' Test if the object has been freed by the game engine and is no longer valid. Normally this is not a problem but when storing game engine data in the GameLogic module, KX_Scenes or other KX_GameObjects its possible to hold a reference to invalid data. Calling an attribute or method on an invalid object will raise a SystemError. The invalid attribute allows testing for this case without exception handling.

    :type: bool
    '''


class BL_ArmatureBone(EXP_PyObjectPlus):
    ''' Proxy to Blender bone structure. All fields are read-only and comply to RNA names. All space attribute correspond to the rest pose.
    '''

    name: str = None
    ''' bone name.

    :type: str
    '''

    connected: bool = None
    ''' true when the bone head is struck to the parent's tail.

    :type: bool
    '''

    hinge: bool = None
    ''' true when bone doesn't inherit rotation or scale from parent bone.

    :type: bool
    '''

    inherit_scale: bool = None
    ''' true when bone inherits scaling from parent bone.

    :type: bool
    '''

    bbone_segments = None
    ''' number of B-bone segments.'''

    roll: float = None
    ''' bone rotation around head-tail axis.

    :type: float
    '''

    head = None
    ''' location of head end of the bone in parent bone space.'''

    tail = None
    ''' location of head end of the bone in parent bone space.'''

    length: float = None
    ''' bone length.

    :type: float
    '''

    arm_head = None
    ''' location of head end of the bone in armature space.'''

    arm_tail = None
    ''' location of tail end of the bone in armature space.'''

    arm_mat = None
    ''' matrix of the bone head in armature space.'''

    bone_mat = None
    ''' rotation matrix of the bone in parent bone space.'''

    parent: 'BL_ArmatureBone' = None
    ''' parent bone, or None for root bone.

    :type: 'BL_ArmatureBone'
    '''

    children: typing.List['BL_ArmatureBone'] = None
    ''' list of bone's children.

    :type: typing.List['BL_ArmatureBone']
    '''


class BL_ArmatureChannel(EXP_PyObjectPlus):
    ''' Proxy to armature pose channel. Allows to read and set armature pose. The attributes are identical to RNA attributes, but mostly in read-only mode.
    '''

    name: str = None
    ''' channel name (=bone name), read-only.

    :type: str
    '''

    bone: 'BL_ArmatureBone' = None
    ''' return the bone object corresponding to this pose channel, read-only.

    :type: 'BL_ArmatureBone'
    '''

    parent: 'BL_ArmatureChannel' = None
    ''' return the parent channel object, None if root channel, read-only.

    :type: 'BL_ArmatureChannel'
    '''

    has_ik: bool = None
    ''' true if the bone is part of an active IK chain, read-only. This flag is not set when an IK constraint is defined but not enabled (miss target information for example).

    :type: bool
    '''

    ik_dof_x: bool = None
    ''' true if the bone is free to rotation in the X axis, read-only.

    :type: bool
    '''

    ik_dof_y: bool = None
    ''' true if the bone is free to rotation in the Y axis, read-only.

    :type: bool
    '''

    ik_dof_z: bool = None
    ''' true if the bone is free to rotation in the Z axis, read-only.

    :type: bool
    '''

    ik_limit_x: bool = None
    ''' true if a limit is imposed on X rotation, read-only.

    :type: bool
    '''

    ik_limit_y: bool = None
    ''' true if a limit is imposed on Y rotation, read-only.

    :type: bool
    '''

    ik_limit_z: bool = None
    ''' true if a limit is imposed on Z rotation, read-only.

    :type: bool
    '''

    ik_rot_control: bool = None
    ''' true if channel rotation should applied as IK constraint, read-only.

    :type: bool
    '''

    ik_lin_control: bool = None
    ''' true if channel size should applied as IK constraint, read-only.

    :type: bool
    '''

    location = None
    ''' displacement of the bone head in armature local space, read-write.'''

    scale = None
    ''' scale of the bone relative to its parent, read-write.'''

    rotation_quaternion = None
    ''' rotation of the bone relative to its parent expressed as a quaternion, read-write.'''

    rotation_euler = None
    ''' rotation of the bone relative to its parent expressed as a set of euler angles, read-write.'''

    rotation_mode = None
    ''' Method of updating the bone rotation, read-write.'''

    channel_matrix = None
    ''' pose matrix in bone space (deformation of the bone due to action, constraint, etc), Read-only. This field is updated after the graphic render, it represents the current pose.'''

    pose_matrix = None
    ''' pose matrix in armature space, read-only, This field is updated after the graphic render, it represents the current pose.'''

    pose_head = None
    ''' position of bone head in armature space, read-only.'''

    pose_tail = None
    ''' position of bone tail in armature space, read-only.'''

    ik_min_x: float = None
    ''' minimum value of X rotation in degree (<= 0) when X rotation is limited (see ik_limit_x), read-only.

    :type: float
    '''

    ik_max_x: float = None
    ''' maximum value of X rotation in degree (>= 0) when X rotation is limited (see ik_limit_x), read-only.

    :type: float
    '''

    ik_min_y: float = None
    ''' minimum value of Y rotation in degree (<= 0) when Y rotation is limited (see ik_limit_y), read-only.

    :type: float
    '''

    ik_max_y: float = None
    ''' maximum value of Y rotation in degree (>= 0) when Y rotation is limited (see ik_limit_y), read-only.

    :type: float
    '''

    ik_min_z: float = None
    ''' minimum value of Z rotation in degree (<= 0) when Z rotation is limited (see ik_limit_z), read-only.

    :type: float
    '''

    ik_max_z: float = None
    ''' maximum value of Z rotation in degree (>= 0) when Z rotation is limited (see ik_limit_z), read-only.

    :type: float
    '''

    ik_stiffness_x: float = None
    ''' bone rotation stiffness in X axis, read-only.

    :type: float
    '''

    ik_stiffness_y: float = None
    ''' bone rotation stiffness in Y axis, read-only.

    :type: float
    '''

    ik_stiffness_z: float = None
    ''' bone rotation stiffness in Z axis, read-only.

    :type: float
    '''

    ik_stretch: float = None
    ''' ratio of scale change that is allowed, 0=bone can't change size, read-only.

    :type: float
    '''

    ik_rot_weight: float = None
    ''' weight of rotation constraint when ik_rot_control is set, read-write.

    :type: float
    '''

    ik_lin_weight: float = None
    ''' weight of size constraint when ik_lin_control is set, read-write.

    :type: float
    '''

    joint_rotation = None
    ''' Control bone rotation in term of joint angle (for robotic applications), read-write. When writing to this attribute, you pass a [x, y, z] vector and an appropriate set of euler angles or quaternion is calculated according to the rotation_mode. When you read this attribute, the current pose matrix is converted into a [x, y, z] vector representing the joint angles. The value and the meaning of the x, y, z depends on the ik_dof_x/ik_dof_y/ik_dof_z attributes: * 1DoF joint X, Y or Z: the corresponding x, y, or z value is used an a joint angle in radiant * 2DoF joint X+Y or Z+Y: treated as 2 successive 1DoF joints: first X or Z, then Y. The x or z value is used as a joint angle in radiant along the X or Z axis, followed by a rotation along the new Y axis of y radiants. * 2DoF joint X+Z: treated as a 2DoF joint with rotation axis on the X/Z plane. The x and z values are used as the coordinates of the rotation vector in the X/Z plane. * 3DoF joint X+Y+Z: treated as a revolute joint. The [x, y, z] vector represents the equivalent rotation vector to bring the joint from the rest pose to the new pose.'''


class BL_ArmatureConstraint(EXP_PyObjectPlus):
    ''' Proxy to Armature Constraint. Allows to change constraint on the fly. Obtained through BL_ArmatureObject .constraints.
    '''

    type = None
    ''' Type of constraint, (read-only). Use one of :ref: these constants<armatureconstraint-constants-type> .'''

    name: str = None
    ''' Name of constraint constructed as <bone_name>:<constraint_name>. constraints list. This name is also the key subscript on BL_ArmatureObject .

    :type: str
    '''

    enforce: float = None
    ''' fraction of constraint effect that is enforced. Between 0 and 1.

    :type: float
    '''

    headtail = None
    ''' Position of target between head and tail of the target bone: 0=head, 1=tail.'''

    lin_error: float = None
    ''' runtime linear error (in Blender units) on constraint at the current frame. This is a runtime value updated on each frame by the IK solver. Only available on IK constraint and iTaSC solver.

    :type: float
    '''

    rot_error = None
    ''' Runtime rotation error (in radiant) on constraint at the current frame. This is a runtime value updated on each frame by the IK solver. Only available on IK constraint and iTaSC solver. It is only set if the constraint has a rotation part, for example, a CopyPose+Rotation IK constraint.'''

    target: 'KX_GameObject' = None
    ''' Primary target object for the constraint. The position of this object in the GE will be used as target for the constraint.

    :type: 'KX_GameObject'
    '''

    subtarget: 'KX_GameObject' = None
    ''' Secondary target object for the constraint. The position of this object in the GE will be used as secondary target for the constraint. Currently this is only used for pole target on IK constraint.

    :type: 'KX_GameObject'
    '''

    active: bool = None
    ''' True if the constraint is active.

    :type: bool
    '''

    ik_weight: float = None
    ''' Weight of the IK constraint between 0 and 1. Only defined for IK constraint.

    :type: float
    '''

    ik_type = None
    ''' Type of IK constraint, (read-only). Use one of :ref: these constants<armatureconstraint-constants-ik-type> .'''

    ik_flag = None
    ''' Combination of IK constraint option flags, read-only. Use one of :ref: these constants<armatureconstraint-constants-ik-flag> .'''

    ik_dist: float = None
    ''' Distance the constraint is trying to maintain with target, only used when ik_type=CONSTRAINT_IK_DISTANCE.

    :type: float
    '''

    ik_mode = None
    ''' Use one of :ref: these constants<armatureconstraint-constants-ik-mode> . Additional mode for IK constraint. Currently only used for Distance constraint:'''


class BL_Shader(EXP_PyObjectPlus):
    ''' BL_Shader is a class used to compile and use custom shaders scripts. It supports vertex, fragment and geometry shader scripts. The shader is compiled with a generated header for the three shaders scripts. This header set the #version directive, so the user must not define his own #version .
    '''

    enabled: bool = None
    ''' Set shader enabled to use.

    :type: bool
    '''

    objectCallbacks: list = None
    ''' The list of python callbacks executed when the shader is used to render an object. All the functions can expect as argument the object currently rendered.

    :type: list
    '''

    bindCallbacks: list = None
    ''' The list of python callbacks executed when the shader is begin used to render.

    :type: list
    '''

    def setUniformfv(self, name: str, fList):
        ''' Set a uniform with a list of float values

        :param name: the uniform name
        :type name: str
        :param fList: a list (2, 3 or 4 elements) of float values
        :type fList: 
        '''
        pass

    def delSource(self):
        ''' Clear the shader. Use this method before the source is changed with :data: setSource .

        '''
        pass

    def getFragmentProg(self) -> str:
        ''' Returns the fragment program.

        :rtype: str
        :return: The fragment program.
        '''
        pass

    def getVertexProg(self) -> str:
        ''' Get the vertex program.

        :rtype: str
        :return: The vertex program.
        '''
        pass

    def isValid(self) -> bool:
        ''' Check if the shader is valid.

        :rtype: bool
        :return: True if the shader is valid
        '''
        pass

    def setAttrib(self, enum):
        ''' Set attribute location. (The parameter is ignored a.t.m. and the value of "tangent" is always used.)

        :param enum: attribute location value
        :type enum: 
        '''
        pass

    def setSampler(self, name: str, index):
        ''' Set uniform texture sample index.

        :param name: Uniform name
        :type name: str
        :param index: Texture sample index.
        :type index: 
        '''
        pass

    def setSource(self, vertexProgram: str, fragmentProgram: str, apply: bool):
        ''' Set the vertex and fragment programs

        :param vertexProgram: Vertex program
        :type vertexProgram: str
        :param fragmentProgram: Fragment program
        :type fragmentProgram: str
        :param apply: Enable the shader.
        :type apply: bool
        '''
        pass

    def setSourceList(self, sources: dict, apply: bool):
        ''' Set the vertex, fragment and geometry shader programs.

        :param sources: geometry represent shader programs of the same name. :data: geometry is an optional program. This dictionary can be similar to: .. code-block:: python sources = { "vertex" : vertexProgram, "fragment" : fragmentProgram, "geometry" : geometryProgram }
        :type sources: dict
        :param apply: Enable the shader.
        :type apply: bool
        '''
        pass

    def setUniform1f(self, name: str, fx: float):
        ''' Set a uniform with 1 float value.

        :param name: the uniform name
        :type name: str
        :param fx: Uniform value
        :type fx: float
        '''
        pass

    def setUniform1i(self, name: str, ix):
        ''' Set a uniform with an integer value.

        :param name: the uniform name
        :type name: str
        :param ix: the uniform value
        :type ix: 
        '''
        pass

    def setUniform2f(self, name: str, fx: float, fy: float):
        ''' Set a uniform with 2 float values

        :param name: the uniform name
        :type name: str
        :param fx: first float value
        :type fx: float
        :param fy: second float value
        :type fy: float
        '''
        pass

    def setUniform2i(self, name: str, ix, iy):
        ''' Set a uniform with 2 integer values

        :param name: the uniform name
        :type name: str
        :param ix: first integer value
        :type ix: 
        :param iy: second integer value
        :type iy: 
        '''
        pass

    def setUniform3f(self, name: str, fx: float, fy: float, fz: float):
        ''' Set a uniform with 3 float values.

        :param name: the uniform name
        :type name: str
        :param fx: first float value
        :type fx: float
        :param fy: second float value
        :type fy: float
        :param fz: third float value
        :type fz: float
        '''
        pass

    def setUniform3i(self, name: str, ix, iy, iz):
        ''' Set a uniform with 3 integer values

        :param name: the uniform name
        :type name: str
        :param ix: first integer value
        :type ix: 
        :param iy: second integer value
        :type iy: 
        :param iz: third integer value
        :type iz: 
        '''
        pass

    def setUniform4f(self, name: str, fx: float, fy: float, fz: float,
                     fw: float):
        ''' Set a uniform with 4 float values.

        :param name: the uniform name
        :type name: str
        :param fx: first float value
        :type fx: float
        :param fy: second float value
        :type fy: float
        :param fz: third float value
        :type fz: float
        :param fw: fourth float value
        :type fw: float
        '''
        pass

    def setUniform4i(self, name: str, ix, iy, iz, iw):
        ''' Set a uniform with 4 integer values

        :param name: the uniform name
        :type name: str
        :param ix: first integer value
        :type ix: 
        :param iy: second integer value
        :type iy: 
        :param iz: third integer value
        :type iz: 
        :param iw: fourth integer value
        :type iw: 
        '''
        pass

    def setUniformDef(self, name: str, type):
        ''' Define a new uniform

        :param name: the uniform name
        :type name: str
        :param type: these constants <shader-defined-uniform>
        :type type: 
        '''
        pass

    def setUniformMatrix3(self, name: str, mat, transpose: bool):
        ''' Set a uniform with a 3x3 matrix value

        :param name: the uniform name
        :type name: str
        :param mat: A 3x3 matrix [[f, f, f], [f, f, f], [f, f, f]]
        :type mat: 
        :param transpose: set to True to transpose the matrix
        :type transpose: bool
        '''
        pass

    def setUniformMatrix4(self, name: str, mat, transpose: bool):
        ''' Set a uniform with a 4x4 matrix value

        :param name: the uniform name
        :type name: str
        :param mat: A 4x4 matrix [[f, f, f, f], [f, f, f, f], [f, f, f, f], [f, f, f, f]]
        :type mat: 
        :param transpose: set to True to transpose the matrix
        :type transpose: bool
        '''
        pass

    def setUniformiv(self, name: str, iList):
        ''' Set a uniform with a list of integer values

        :param name: the uniform name
        :type name: str
        :param iList: a list (2, 3 or 4 elements) of integer values
        :type iList: 
        '''
        pass

    def setUniformEyef(self, name: str):
        ''' Set a uniform with a float value that reflects the eye being render in stereo mode: 0.0 for the left eye, 0.5 for the right eye. In non stereo mode, the value of the uniform is fixed to 0.0. The typical use of this uniform is in stereo mode to sample stereo textures containing the left and right eye images in a top-bottom order.

        :param name: the uniform name
        :type name: str
        '''
        pass

    def validate(self):
        ''' Validate the shader object.

        '''
        pass


class EXP_Value(EXP_PyObjectPlus):
    ''' This class is a basis for other classes.
    '''

    name: str = None
    ''' The name of this EXP_Value derived object (read-only).

    :type: str
    '''


class KX_2DFilterManager(EXP_PyObjectPlus):
    ''' 2D filter manager used to add, remove and find filters in a scene.
    '''

    def addFilter(self, index, type, fragmentProgram: str) -> 'KX_2DFilter':
        ''' Add a filter to the pass index :data: index , type :data: type and fragment program if custom filter.

        :param index: The filter pass index.
        :type index: 
        :param type: * :data: bge.logic.RAS_2DFILTER_BLUR * :data: bge.logic.RAS_2DFILTER_DILATION * :data: bge.logic.RAS_2DFILTER_EROSION * :data: bge.logic.RAS_2DFILTER_SHARPEN * :data: bge.logic.RAS_2DFILTER_LAPLACIAN * :data: bge.logic.RAS_2DFILTER_PREWITT * :data: bge.logic.RAS_2DFILTER_SOBEL * :data: bge.logic.RAS_2DFILTER_GRAYSCALE * :data: bge.logic.RAS_2DFILTER_SEPIA * :data: bge.logic.RAS_2DFILTER_CUSTOMFILTER
        :type type: 
        :param fragmentProgram: The filter shader fragment program. Used only if :data: type is :data: bge.logic.RAS_2DFILTER_CUSTOMFILTER , if empty or not specified the filter is created without shader, waiting call to :data: BL_Shader.setSourceList . (optional)
        :type fragmentProgram: str
        :rtype: 'KX_2DFilter'
        :return: The 2D Filter.
        '''
        pass

    def removeFilter(self, index):
        ''' Remove filter to the pass index :data: index .

        :param index: The filter pass index.
        :type index: 
        '''
        pass

    def getFilter(self, index) -> 'KX_2DFilter':
        ''' Return filter to the pass index :data: index .

        :param index: The filter pass index.
        :type index: 
        :rtype: 'KX_2DFilter'
        :return: The filter in the specified pass index or None.
        '''
        pass


class KX_BlenderMaterial(EXP_PyObjectPlus):
    ''' This is the interface to materials in the game engine. Materials define the render state to be applied to mesh objects. The example below shows a simple GLSL shader setup allowing to dynamically mix two texture channels in a material. All materials of the object executing this script should have two textures using separate UV maps in the two first texture channels. The code works for both Multitexture and GLSL rendering modes.
    '''

    shader: 'BL_Shader' = None
    ''' The material's shader.

    :type: 'BL_Shader'
    '''

    blending = None
    ''' Ints used for pixel blending, (src, dst), matching the setBlending method.'''

    alpha: float = None
    ''' The material's alpha transparency.

    :type: float
    '''

    hardness = None
    ''' How hard (sharp) the material's specular reflection is.'''

    emit: float = None
    ''' Amount of light to emit.

    :type: float
    '''

    ambient: float = None
    ''' Amount of ambient light on the material.

    :type: float
    '''

    specularAlpha: float = None
    ''' Alpha transparency for specular areas.

    :type: float
    '''

    specularIntensity: float = None
    ''' How intense (bright) the material's specular reflection is.

    :type: float
    '''

    diffuseIntensity: float = None
    ''' The material's amount of diffuse reflection.

    :type: float
    '''

    specularColor: 'mathutils.Color' = None
    ''' The material's specular color.

    :type: 'mathutils.Color'
    '''

    diffuseColor: 'mathutils.Color' = None
    ''' The material's diffuse color.

    :type: 'mathutils.Color'
    '''

    textures: typing.List['BL_Texture'] = None
    ''' List of all material's textures.

    :type: typing.List['BL_Texture']
    '''

    def getShader(self) -> 'BL_Shader':
        ''' Returns the material's shader.

        :rtype: 'BL_Shader'
        :return: the material's shader
        '''
        pass

    def getTextureBindcode(self, textureslot):
        ''' Returns the material's texture OpenGL bind code/id/number/name.

        :param textureslot: Specifies the texture slot number
        :type textureslot: 
        :return: the material's texture OpenGL bind code/id/number/name
        '''
        pass

    def setBlending(self, src: int, dest: int):
        ''' Set the pixel color arithmetic functions.

        :param src: Specifies how the red, green, blue, and alpha source blending factors are computed, one of... * :data: ~bgl.GL_ZERO * :data: ~bgl.GL_ONE * :data: ~bgl.GL_SRC_COLOR * :data: ~bgl.GL_ONE_MINUS_SRC_COLOR * :data: ~bgl.GL_DST_COLOR * :data: ~bgl.GL_ONE_MINUS_DST_COLOR * :data: ~bgl.GL_SRC_ALPHA * :data: ~bgl.GL_ONE_MINUS_SRC_ALPHA * :data: ~bgl.GL_DST_ALPHA * :data: ~bgl.GL_ONE_MINUS_DST_ALPHA * :data: ~bgl.GL_SRC_ALPHA_SATURATE
        :type src: int
        :param dest: Specifies how the red, green, blue, and alpha destination blending factors are computed, one of... * :data: ~bgl.GL_ZERO * :data: ~bgl.GL_ONE * :data: ~bgl.GL_SRC_COLOR * :data: ~bgl.GL_ONE_MINUS_SRC_COLOR * :data: ~bgl.GL_DST_COLOR * :data: ~bgl.GL_ONE_MINUS_DST_COLOR * :data: ~bgl.GL_SRC_ALPHA * :data: ~bgl.GL_ONE_MINUS_SRC_ALPHA * :data: ~bgl.GL_DST_ALPHA * :data: ~bgl.GL_ONE_MINUS_DST_ALPHA * :data: ~bgl.GL_SRC_ALPHA_SATURATE
        :type dest: int
        '''
        pass


class KX_BoundingBox(EXP_PyObjectPlus):
    ''' A bounding volume box of a game object. Used to get and alterate the volume box or AABB.
    '''

    min: 'mathutils.Vector' = None
    ''' The minimal point in x, y and z axis of the bounding box.

    :type: 'mathutils.Vector'
    '''

    max: 'mathutils.Vector' = None
    ''' The maximal point in x, y and z axis of the bounding box.

    :type: 'mathutils.Vector'
    '''

    center: 'mathutils.Vector' = None
    ''' The center of the bounding box. (read only)

    :type: 'mathutils.Vector'
    '''

    radius: float = None
    ''' The radius of the bounding box. (read only)

    :type: float
    '''

    autoUpdate: bool = None
    ''' Allow to update the bounding box if the mesh is modified.

    :type: bool
    '''


class KX_CharacterWrapper(EXP_PyObjectPlus):
    ''' A wrapper to expose character physics options.
    '''

    onGround: bool = None
    ''' Whether or not the character is on the ground. (read-only)

    :type: bool
    '''

    gravity: float = None
    ''' The gravity value used for the character.

    :type: float
    '''

    fallSpeed: float = None
    ''' The character falling speed.

    :type: float
    '''

    maxJumps: int = None
    ''' The maximum number of jumps a character can perform before having to touch the ground. By default this is set to 1. 2 allows for a double jump, etc.

    :type: int
    '''

    jumpCount: int = None
    ''' The current jump count. This can be used to have different logic for a single jump versus a double jump. For example, a different animation for the second jump.

    :type: int
    '''

    jumpSpeed: float = None
    ''' The character jumping speed.

    :type: float
    '''

    maxSlope: float = None
    ''' The maximum slope which the character can climb.

    :type: float
    '''

    walkDirection = None
    ''' The speed and direction the character is traveling in using world coordinates. This should be used instead of applyMovement() to properly move the character.'''

    def jump(self):
        ''' The character jumps based on it's jump speed.

        '''
        pass

    def setVelocity(self,
                    velocity: 'mathutils.Vector',
                    time: float,
                    local: bool = False):
        ''' Sets the character's linear velocity for a given period. This method sets character's velocity through it's center of mass during a period.

        :param velocity: Linear velocity vector.
        :type velocity: 'mathutils.Vector'
        :param time: Period while applying linear velocity.
        :type time: float
        :param local: * False: you get the "global" velocity ie: relative to world orientation. * True: you get the "local" velocity ie: relative to object orientation.
        :type local: bool
        '''
        pass

    def reset(self):
        ''' Resets the character velocity and walk direction.

        '''
        pass


class KX_ConstraintWrapper(EXP_PyObjectPlus):
    ''' KX_ConstraintWrapper
    '''

    constraint_id = None
    ''' Returns the contraint ID (read only)'''

    constraint_type = None
    ''' Returns the contraint type (read only) - ~bge.constraints.POINTTOPOINT_CONSTRAINT - ~bge.constraints.LINEHINGE_CONSTRAINT - ~bge.constraints.ANGULAR_CONSTRAINT - ~bge.constraints.CONETWIST_CONSTRAINT - ~bge.constraints.VEHICLE_CONSTRAINT - ~bge.constraints.GENERIC_6DOF_CONSTRAINT'''

    breakingThreshold: float = None
    ''' The impulse threshold breaking the constraint, if the constraint is broken :data: enabled is set to False .

    :type: float
    '''

    enabled: bool = None
    ''' The status of the constraint. Set to True to restore a constraint after breaking.

    :type: bool
    '''

    def getConstraintId(self, val):
        ''' Returns the contraint ID

        :return: the constraint ID
        '''
        pass

    def setParam(self, axis, value0: float, value1: float):
        ''' Set the contraint limits For PHY_LINEHINGE_CONSTRAINT = 2 or PHY_ANGULAR_CONSTRAINT = 3: axis = 3 is a constraint limit, with low/high limit value * 3: X axis angle

        :param axis: 
        :type axis: 
        :param value0: Set the minimum limit of the axis Set the minimum limit of the axis Set the minimum limit of the axis Set the linear velocity of the axis Set the stiffness of the spring
        :type value0: float
        :param value1: Set the maximum limit of the axis Set the maximum limit of the axis Set the maximum limit of the axis Set the maximum force limit of the axis Tendency of the spring to return to it's original position
        :type value1: float
        :param value0: Set the minimum limit of the axis Set the minimum limit of the axis Set the minimum limit of the axis Set the linear velocity of the axis Set the stiffness of the spring
        :type value0: float
        :param value1: Set the maximum limit of the axis Set the maximum limit of the axis Set the maximum limit of the axis Set the maximum force limit of the axis Tendency of the spring to return to it's original position
        :type value1: float
        :param value0: Set the minimum limit of the axis Set the minimum limit of the axis Set the minimum limit of the axis Set the linear velocity of the axis Set the stiffness of the spring
        :type value0: float
        :param value1: Set the maximum limit of the axis Set the maximum limit of the axis Set the maximum limit of the axis Set the maximum force limit of the axis Tendency of the spring to return to it's original position
        :type value1: float
        :param value0: Set the minimum limit of the axis Set the minimum limit of the axis Set the minimum limit of the axis Set the linear velocity of the axis Set the stiffness of the spring
        :type value0: float
        :param value1: Set the maximum limit of the axis Set the maximum limit of the axis Set the maximum limit of the axis Set the maximum force limit of the axis Tendency of the spring to return to it's original position
        :type value1: float
        :param value0: Set the minimum limit of the axis Set the minimum limit of the axis Set the minimum limit of the axis Set the linear velocity of the axis Set the stiffness of the spring
        :type value0: float
        :param value1: Set the maximum limit of the axis Set the maximum limit of the axis Set the maximum limit of the axis Set the maximum force limit of the axis Tendency of the spring to return to it's original position
        :type value1: float
        '''
        pass

    def getParam(self, axis) -> float:
        ''' Get the contraint position or euler angle of a generic 6DOF constraint

        :param axis: 
        :type axis: 
        :rtype: float
        :return: position
        '''
        pass


class KX_LibLoadStatus(EXP_PyObjectPlus):
    ''' An object providing information about a LibLoad() operation.
    '''

    onFinish = None
    ''' A callback that gets called when the lib load is done.'''

    finished: bool = None
    ''' The current status of the lib load.

    :type: bool
    '''

    progress: float = None
    ''' The current progress of the lib load as a normalized value from 0.0 to 1.0.

    :type: float
    '''

    libraryName: str = None
    ''' The name of the library being loaded (the first argument to LibLoad).

    :type: str
    '''

    timeTaken: float = None
    ''' The amount of time, in seconds, the lib load took (0 until the operation is complete).

    :type: float
    '''


class KX_LodLevel(EXP_PyObjectPlus):
    ''' A single lod level for a game object lod manager.
    '''

    mesh = None
    ''' The mesh used for this lod level. (read only)'''

    level = None
    ''' The number of the lod level. (read only)'''

    distance: float = None
    ''' Distance to begin using this level of detail. (read only)

    :type: float
    '''

    hysteresis: float = None
    ''' Minimum distance factor change required to transition to the previous level of detail in percent. (read only)

    :type: float
    '''

    useMesh: bool = None
    ''' Return True if the lod level uses a different mesh than the original object mesh. (read only)

    :type: bool
    '''

    useMaterial: bool = None
    ''' Return True if the lod level uses a different material than the original object mesh material. (read only)

    :type: bool
    '''

    useHysteresis: bool = None
    ''' Return true if the lod level uses hysteresis override. (read only)

    :type: bool
    '''


class KX_LodManager(EXP_PyObjectPlus):
    ''' This class contains a list of all levels of detail used by a game object.
    '''

    levels: typing.List['KX_LodLevel'] = None
    ''' Return the list of all levels of detail of the lod manager.

    :type: typing.List['KX_LodLevel']
    '''

    distanceFactor: float = None
    ''' Method to multiply the distance to the camera.

    :type: float
    '''


class KX_Scene(EXP_PyObjectPlus):
    ''' An active scene that gives access to objects, cameras, lights and scene attributes. The activity culling stuff is supposed to disable logic bricks when their owner gets too far from the active camera. It was taken from some code lurking at the back of KX_Scene - who knows what it does! @bug: All attributes are read only at the moment.
    '''

    name: str = None
    ''' The scene's name, (read-only).

    :type: str
    '''

    objects: typing.Union['KX_GameObject', 'EXP_ListValue'] = None
    ''' A list of objects in the scene, (read-only).

    :type: typing.Union['KX_GameObject', 'EXP_ListValue']
    '''

    objectsInactive: typing.Union['KX_GameObject', 'EXP_ListValue'] = None
    ''' A list of objects on background layers (used for the addObject actuator), (read-only).

    :type: typing.Union['KX_GameObject', 'EXP_ListValue']
    '''

    lights: typing.Union['KX_LightObject', 'EXP_ListValue'] = None
    ''' A list of lights in the scene, (read-only).

    :type: typing.Union['KX_LightObject', 'EXP_ListValue']
    '''

    cameras: typing.Union['EXP_ListValue', 'KX_Camera'] = None
    ''' A list of cameras in the scene, (read-only).

    :type: typing.Union['EXP_ListValue', 'KX_Camera']
    '''

    texts: typing.Union['EXP_ListValue', 'KX_FontObject'] = None
    ''' A list of texts in the scene, (read-only).

    :type: typing.Union['EXP_ListValue', 'KX_FontObject']
    '''

    active_camera: 'KX_Camera' = None
    ''' The current active camera.

    :type: 'KX_Camera'
    '''

    overrideCullingCamera: 'KX_Camera' = None
    ''' The override camera used for scene culling, if set to None the culling is proceeded with the camera used to render.

    :type: 'KX_Camera'
    '''

    world: 'KX_WorldInfo' = None
    ''' The current active world, (read-only).

    :type: 'KX_WorldInfo'
    '''

    filterManager: 'KX_2DFilterManager' = None
    ''' The scene's 2D filter manager, (read-only).

    :type: 'KX_2DFilterManager'
    '''

    suspended: bool = None
    ''' True if the scene is suspended, (read-only).

    :type: bool
    '''

    activityCulling: bool = None
    ''' True if the scene allow object activity culling.

    :type: bool
    '''

    dbvt_culling: bool = None
    ''' True when Dynamic Bounding box Volume Tree is set (read-only).

    :type: bool
    '''

    pre_draw: list = None
    ''' A list of callables to be run before the render step. The callbacks can take as argument the rendered camera.

    :type: list
    '''

    post_draw: list = None
    ''' A list of callables to be run after the render step.

    :type: list
    '''

    pre_draw_setup: list = None
    ''' A list of callables to be run before the drawing setup (i.e., before the model view and projection matrices are computed). The callbacks can take as argument the rendered camera, the camera could be temporary in case of stereo rendering.

    :type: list
    '''

    onRemove: list = None
    ''' A list of callables to run when the scene is destroyed. .. code-block:: python @scene.onRemove.append def callback(scene): print('exiting %s...' % scene.name)

    :type: list
    '''

    gravity = None
    ''' The scene gravity using the world x, y and z axis.'''

    def addObject(self,
                  object: typing.Union[str, 'KX_GameObject'],
                  reference: typing.Union[str, 'KX_GameObject'],
                  time: float = 0.0) -> 'KX_GameObject':
        ''' Adds an object to the scene like the Add Object Actuator would.

        :param object: The (name of the) object to add.
        :type object: typing.Union[str, 'KX_GameObject']
        :param reference: The (name of the) object which position, orientation, and scale to copy (optional), if the object to add is a light and there is not reference the light's layer will be the same that the active layer in the blender scene.
        :type reference: typing.Union[str, 'KX_GameObject']
        :param time: The lifetime of the added object, in frames (assumes one frame is 1/50 second). A time of 0.0 means the object will last forever (optional).
        :type time: float
        :rtype: 'KX_GameObject'
        :return: The newly added object.
        '''
        pass

    def end(self):
        ''' Removes the scene from the game.

        '''
        pass

    def restart(self):
        ''' Restarts the scene.

        '''
        pass

    def replace(self, scene: str) -> bool:
        ''' Replaces this scene with another one.

        :param scene: The name of the scene to replace this scene with.
        :type scene: str
        :rtype: bool
        :return: True if the scene exists and was scheduled for addition, False otherwise.
        '''
        pass

    def suspend(self):
        ''' Suspends this scene.

        '''
        pass

    def resume(self):
        ''' Resume this scene.

        '''
        pass

    def get(self, key, default=None):
        ''' Return the value matching key, or the default value if its not found.

        '''
        pass

    def drawObstacleSimulation(self):
        ''' Draw debug visualization of obstacle simulation.

        '''
        pass


class KX_VehicleWrapper(EXP_PyObjectPlus):
    ''' KX_VehicleWrapper TODO - description
    '''

    rayMask = None
    ''' Set ray cast mask.'''

    def addWheel(self, wheel: 'KX_GameObject', attachPos, downDir, axleDir,
                 suspensionRestLength: float, wheelRadius: float,
                 hasSteering: bool):
        ''' Add a wheel to the vehicle

        :param wheel: The object to use as a wheel.
        :type wheel: 'KX_GameObject'
        :param attachPos: The position to attach the wheel, relative to the chassis object center.
        :type attachPos: 
        :param downDir: The direction vector pointing down to where the vehicle should collide with the floor.
        :type downDir: 
        :param axleDir: The axis the wheel rotates around, relative to the chassis.
        :type axleDir: 
        :param suspensionRestLength: The length of the suspension when no forces are being applied.
        :type suspensionRestLength: float
        :param wheelRadius: The radius of the wheel (half the diameter).
        :type wheelRadius: float
        :param hasSteering: True if the wheel should turn with steering, typically used in front wheels.
        :type hasSteering: bool
        '''
        pass

    def applyBraking(self, force: float, wheelIndex):
        ''' Apply a braking force to the specified wheel

        :param force: the brake force
        :type force: float
        :param wheelIndex: index of the wheel where the force needs to be applied
        :type wheelIndex: 
        '''
        pass

    def applyEngineForce(self, force: float, wheelIndex):
        ''' Apply an engine force to the specified wheel

        :param force: the engine force
        :type force: float
        :param wheelIndex: index of the wheel where the force needs to be applied
        :type wheelIndex: 
        '''
        pass

    def getConstraintId(self):
        ''' Get the constraint ID

        :return: the constraint id
        '''
        pass

    def getConstraintType(self):
        ''' Returns the constraint type.

        :return: constraint type
        '''
        pass

    def getNumWheels(self):
        ''' Returns the number of wheels.

        :return: the number of wheels for this vehicle
        '''
        pass

    def getWheelOrientationQuaternion(self, wheelIndex):
        ''' Returns the wheel orientation as a quaternion.

        :param wheelIndex: the wheel index
        :type wheelIndex: 
        :return: TODO Description
        '''
        pass

    def getWheelPosition(self, wheelIndex):
        ''' Returns the position of the specified wheel

        :param wheelIndex: the wheel index
        :type wheelIndex: 
        :return: position vector
        '''
        pass

    def getWheelRotation(self, wheelIndex) -> float:
        ''' Returns the rotation of the specified wheel

        :param wheelIndex: the wheel index
        :type wheelIndex: 
        :rtype: float
        :return: the wheel rotation
        '''
        pass

    def setRollInfluence(self, rollInfluece: float, wheelIndex):
        ''' Set the specified wheel's roll influence. The higher the roll influence the more the vehicle will tend to roll over in corners.

        :param rollInfluece: the wheel roll influence
        :type rollInfluece: float
        :param wheelIndex: the wheel index
        :type wheelIndex: 
        '''
        pass

    def setSteeringValue(self, steering: float, wheelIndex):
        ''' Set the specified wheel's steering

        :param steering: the wheel steering
        :type steering: float
        :param wheelIndex: the wheel index
        :type wheelIndex: 
        '''
        pass

    def setSuspensionCompression(self, compression: float, wheelIndex):
        ''' Set the specified wheel's compression

        :param compression: the wheel compression
        :type compression: float
        :param wheelIndex: the wheel index
        :type wheelIndex: 
        '''
        pass

    def setSuspensionDamping(self, damping: float, wheelIndex):
        ''' Set the specified wheel's damping

        :param damping: the wheel damping
        :type damping: float
        :param wheelIndex: the wheel index
        :type wheelIndex: 
        '''
        pass

    def setSuspensionStiffness(self, stiffness: float, wheelIndex):
        ''' Set the specified wheel's stiffness

        :param stiffness: the wheel stiffness
        :type stiffness: float
        :param wheelIndex: the wheel index
        :type wheelIndex: 
        '''
        pass

    def setTyreFriction(self, friction: float, wheelIndex):
        ''' Set the specified wheel's tyre friction

        :param friction: the tyre friction
        :type friction: float
        :param wheelIndex: the wheel index
        :type wheelIndex: 
        '''
        pass


class KX_WorldInfo(EXP_PyObjectPlus):
    ''' A world object.
    '''

    KX_MIST_QUADRATIC = None
    ''' Type of quadratic attenuation used to fade mist.'''

    KX_MIST_LINEAR = None
    ''' Type of linear attenuation used to fade mist.'''

    KX_MIST_INV_QUADRATIC = None
    ''' Type of inverse quadratic attenuation used to fade mist.'''

    mistEnable: bool = None
    ''' Return the state of the mist.

    :type: bool
    '''

    mistStart: float = None
    ''' The mist start point.

    :type: float
    '''

    mistDistance: float = None
    ''' The mist distance fom the start point to reach 100% mist.

    :type: float
    '''

    mistIntensity: float = None
    ''' The mist intensity.

    :type: float
    '''

    mistType = None
    ''' The type of mist - must be KX_MIST_QUADRATIC, KX_MIST_LINEAR or KX_MIST_INV_QUADRATIC'''

    mistColor: 'mathutils.Color' = None
    ''' The color of the mist. Black = [0.0, 0.0, 0.0], White = [1.0, 1.0, 1.0]. Mist and background color sould always set to the same color.

    :type: 'mathutils.Color'
    '''

    horizonColor: 'mathutils.Vector' = None
    ''' The horizon color. Black = [0.0, 0.0, 0.0, 1.0], White = [1.0, 1.0, 1.0, 1.0]. Mist and horizon color should always be set to the same color.

    :type: 'mathutils.Vector'
    '''

    zenithColor: 'mathutils.Vector' = None
    ''' The zenith color. Black = [0.0, 0.0, 0.0, 1.0], White = [1.0, 1.0, 1.0, 1.0].

    :type: 'mathutils.Vector'
    '''

    ambientColor: 'mathutils.Color' = None
    ''' The color of the ambient light. Black = [0.0, 0.0, 0.0], White = [1.0, 1.0, 1.0].

    :type: 'mathutils.Color'
    '''

    exposure: float = None
    ''' Amount of exponential color correction for light.

    :type: float
    '''

    range: float = None
    ''' The color range that will be mapped to 0 - 1.

    :type: float
    '''

    envLightEnergy: float = None
    ''' The environment light energy.

    :type: float
    '''

    envLightEnabled: bool = None
    ''' Returns True if Environment Lighting is enabled. Else returns False

    :type: bool
    '''

    envLightColor: int = None
    ''' White: returns 0 SkyColor: returns 1 SkyTexture: returns 2

    :type: int
    '''


class SCA_InputEvent(EXP_PyObjectPlus):
    ''' Events for a keyboard or mouse input.
    '''

    status: list = None
    ''' A list of existing status of the input from the last frame. Can contain :data: bge.logic.KX_INPUT_NONE and :data: bge.logic.KX_INPUT_ACTIVE . The list always contains one value. The first value of the list is the last value of the list in the last frame. (read-only)

    :type: list
    '''

    queue: list = None
    ''' A list of existing events of the input from the last frame. Can contain :data: bge.logic.KX_INPUT_JUST_ACTIVATED and :data: bge.logic.KX_INPUT_JUST_RELEASED . The list can be empty. (read-only)

    :type: list
    '''

    values: list = None
    ''' A list of existing value of the input from the last frame. For keyboard it contains 1 or 0 and for mouse the coordinate of the mouse or the movement of the wheel mouse. The list contains always one value, the size of the list is the same than :data: queue + 1 only for keyboard inputs. The first value of the list is the last value of the list in the last frame. (read-only) Example to get the non-normalized mouse coordinates:

    :type: list
    '''

    inactive: bool = None
    ''' True if the input was inactive from the last frame.

    :type: bool
    '''

    active: bool = None
    ''' True if the input was active from the last frame.

    :type: bool
    '''

    activated: bool = None
    ''' True if the input was activated from the last frame.

    :type: bool
    '''

    released: bool = None
    ''' True if the input was released from the last frame.

    :type: bool
    '''

    type = None
    ''' The type of the input. One of :ref: these constants<keyboard-keys>'''


class SCA_PythonJoystick(EXP_PyObjectPlus):
    ''' A Python interface to a joystick.
    '''

    name: str = None
    ''' The name assigned to the joystick by the operating system. (read-only)

    :type: str
    '''

    activeButtons: list = None
    ''' A list of active button values. (read-only)

    :type: list
    '''

    axisValues: list = None
    ''' The state of the joysticks axis as a list of values :data: numAxis long. (read-only). Each specifying the value of an axis between -1.0 and 1.0 depending on how far the axis is pushed, 0 for nothing. The first 2 values are used by most joysticks and gamepads for directional control. 3rd and 4th values are only on some joysticks and can be used for arbitary controls. * left:[-1.0, 0.0, ...] * right:[1.0, 0.0, ...] * up:[0.0, -1.0, ...] * down:[0.0, 1.0, ...]

    :type: list
    '''

    numAxis = None
    ''' The number of axes for the joystick at this index. (read-only).'''

    numButtons = None
    ''' The number of buttons for the joystick at this index. (read-only).'''


class SCA_PythonKeyboard(EXP_PyObjectPlus):
    ''' The current keyboard.
    '''

    inputs: 'SCA_InputEvent' = None
    ''' A dictionary containing the input of each keyboard key. (read-only).

    :type: 'SCA_InputEvent'
    '''

    events = None
    ''' A dictionary containing the status of each keyboard event or key. (read-only).'''

    activeInputs: 'SCA_InputEvent' = None
    ''' A dictionary containing the input of only the active keyboard keys. (read-only).

    :type: 'SCA_InputEvent'
    '''

    active_events = None
    ''' A dictionary containing the status of only the active keyboard events or keys. (read-only).'''

    text: str = None
    ''' The typed unicode text from the last frame.

    :type: str
    '''

    def getClipboard(self):
        ''' Gets the clipboard text.

        '''
        pass

    def setClipboard(self, text: str):
        ''' Sets the clipboard text.

        :param text: New clipboard text
        :type text: str
        '''
        pass


class SCA_PythonMouse(EXP_PyObjectPlus):
    ''' The current mouse.
    '''

    inputs: 'SCA_InputEvent' = None
    ''' A dictionary containing the input of each mouse event. (read-only).

    :type: 'SCA_InputEvent'
    '''

    events = None
    ''' a dictionary containing the status of each mouse event. (read-only).'''

    activeInputs: 'SCA_InputEvent' = None
    ''' A dictionary containing the input of only the active mouse events. (read-only).

    :type: 'SCA_InputEvent'
    '''

    active_events = None
    ''' a dictionary containing the status of only the active mouse events. (read-only).'''

    position: tuple = None
    ''' The normalized x and y position of the mouse cursor.

    :type: tuple
    '''

    visible: bool = None
    ''' The visibility of the mouse cursor.

    :type: bool
    '''


class KX_2DFilter(BL_Shader):
    ''' 2D filter shader object. Can be alterated with BL_Shader 's functions.
    '''

    mipmap: bool = None
    ''' Request mipmap generation of the render bgl_RenderedTexture texture. Accessing mipmapping level is similar to:

    :type: bool
    '''

    offScreen: 'KX_2DFilterOffScreen' = None
    ''' The custom off screen the filter render to (read-only).

    :type: 'KX_2DFilterOffScreen'
    '''

    def setTexture(self, index, bindCode, samplerName: str = ""):
        ''' Set specified texture bind code :data: bindCode in specified slot :data: index . Any call to :data: setTexture should be followed by a call to :data: BL_Shader.setSampler with the same :data: index if :data: sampleName is not specified.

        :param index: The texture slot.
        :type index: 
        :param bindCode: The texture bind code/Id.
        :type bindCode: 
        :param samplerName: samplerName is passed in the function. (optional)
        :type samplerName: str
        '''
        pass

    def setCubeMap(self, index, bindCode, samplerName: str = ""):
        ''' Set specified cube map texture bind code :data: bindCode in specified slot :data: index . Any call to :data: setCubeMap should be followed by a call to :data: BL_Shader.setSampler with the same :data: index if :data: sampleName is not specified.

        :param index: The texture slot.
        :type index: 
        :param bindCode: The cube map texture bind code/Id.
        :type bindCode: 
        :param samplerName: samplerName is passed in the function. (optional)
        :type samplerName: str
        '''
        pass

    def addOffScreen(self,
                     slots,
                     depth: bool = False,
                     width=-1,
                     height=-1,
                     hdr='bge.render.HDR_NONE',
                     mipmap: bool = False):
        ''' Register a custom off screen to render the filter to.

        :param slots: The number of color texture attached to the off screen, between 0 and 8 excluded.
        :type slots: 
        :param depth: True of the off screen use a depth texture (optional).
        :type depth: bool
        :param width: The off screen width, -1 if it can be resized dynamically when the viewport dimensions changed (optional).
        :type width: 
        :param height: The off screen height, -1 if it can be resized dynamically when the viewport dimensions changed (optional).
        :type height: 
        :param hdr: The image quality HDR of the color textures (optional).
        :type hdr: 
        :param mipmap: True if the color texture generate mipmap at the end of the filter rendering (optional).
        :type mipmap: bool
        '''
        pass

    def removeOffScreen(self):
        ''' Unregister the custom off screen the filter render to.

        '''
        pass


class BL_Texture(EXP_Value):
    ''' A texture object that contains attributes of a material texture.
    '''

    diffuseIntensity: float = None
    ''' Amount texture affects diffuse reflectivity.

    :type: float
    '''

    diffuseFactor: float = None
    ''' Amount texture affects diffuse color.

    :type: float
    '''

    alpha: float = None
    ''' Amount texture affects alpha.

    :type: float
    '''

    specularIntensity: float = None
    ''' Amount texture affects specular reflectivity.

    :type: float
    '''

    specularFactor: float = None
    ''' Amount texture affects specular color.

    :type: float
    '''

    hardness: float = None
    ''' Amount texture affects hardness.

    :type: float
    '''

    emit: float = None
    ''' Amount texture affects emission.

    :type: float
    '''

    mirror: float = None
    ''' Amount texture affects mirror color.

    :type: float
    '''

    normal: float = None
    ''' Amount texture affects normal values.

    :type: float
    '''

    parallaxBump: float = None
    ''' Height of parallax occlusion mapping.

    :type: float
    '''

    parallaxStep: float = None
    ''' Number of steps to achieve parallax effect.

    :type: float
    '''

    lodBias: float = None
    ''' Amount bias on mipmapping.

    :type: float
    '''

    bindCode = None
    ''' Texture bind code/Id/number.'''

    renderer: typing.Union['KX_PlanarMap', 'KX_CubeMap'] = None
    ''' Texture renderer of this texture.

    :type: typing.Union['KX_PlanarMap', 'KX_CubeMap']
    '''

    ior: float = None
    ''' Index Of Refraction used to compute refraction.

    :type: float
    '''

    refractionRatio: float = None
    ''' Amount refraction mixed with reflection.

    :type: float
    '''

    uvOffset: 'mathutils.Vector' = None
    ''' Offset applied to texture UV coordinates (mainly translation on U and V axis).

    :type: 'mathutils.Vector'
    '''

    uvSize: 'mathutils.Vector' = None
    ''' Scale applied to texture UV coordinates.

    :type: 'mathutils.Vector'
    '''

    uvRotation: float = None
    ''' Rotation applied to texture UV coordinates.

    :type: float
    '''


class EXP_PropValue(EXP_Value):
    ''' This class has no python functions
    '''

    pass


class KX_2DFilterOffScreen(EXP_Value):
    ''' 2D filter custom off screen.
    '''

    width = None
    ''' The off screen width, -1 if the off screen can be resized dynamically (read-only).'''

    height = None
    ''' The off screen height, -1 if the off screen can be resized dynamically (read-only).'''

    colorBindCodes: list = None
    ''' The bind code of the color textures attached to the off screen (read-only).

    :type: list
    '''

    depthBindCode = None
    ''' The bind code of the depth texture attached to the off screen (read-only).'''


class KX_BatchGroup(EXP_Value):
    ''' The batch group is class containing a mesh resulting of the merging of meshes used by objects. The meshes are merged with the transformation of the objects using it. An instance of this class is not owned by one object but shared between objects. In consideration an instance of KX_BatchGroup have to instanced with as argument a list of at least one object containing the meshes to merge. This can be done in a way similar to:
    '''

    objects: typing.Union['KX_GameObject', 'EXP_ListValue'] = None
    ''' The list of the objects merged. (read only)

    :type: typing.Union['KX_GameObject', 'EXP_ListValue']
    '''

    referenceObject = None
    ''' The object used for object rendering settings (layer, color...).'''

    def merge(self, objects):
        ''' Merge meshes using the transformation of the objects using them.

        :param object: 
        :type object: typing.Union['KX_GameObject', 'EXP_ListValue']
        :param objects: 
        :type objects: 
        '''
        pass

    def split(self, objects):
        ''' Split the meshes of the objects using them and restore their original meshes.

        :param object: 
        :type object: typing.Union['KX_GameObject', 'EXP_ListValue']
        :param objects: 
        :type objects: 
        '''
        pass

    def destruct(self):
        ''' Destruct the batch group and restore all the objects to their original meshes.

        '''
        pass


class KX_CollisionContactPoint(EXP_Value):
    ''' A collision contact point passed to the collision callbacks.
    '''

    localPointA: 'mathutils.Vector' = None
    ''' The contact point in the owner object space.

    :type: 'mathutils.Vector'
    '''

    localPointB: 'mathutils.Vector' = None
    ''' The contact point in the collider object space.

    :type: 'mathutils.Vector'
    '''

    worldPoint: 'mathutils.Vector' = None
    ''' The contact point in world space.

    :type: 'mathutils.Vector'
    '''

    normal: 'mathutils.Vector' = None
    ''' The contact normal in owner object space.

    :type: 'mathutils.Vector'
    '''

    combinedFriction: float = None
    ''' The combined friction of the owner and collider object.

    :type: float
    '''

    combinedRollingFriction: float = None
    ''' The combined rolling friction of the owner and collider object.

    :type: float
    '''

    combinedRestitution: float = None
    ''' The combined restitution of the owner and collider object.

    :type: float
    '''

    appliedImpulse: float = None
    ''' The applied impulse to the owner object.

    :type: float
    '''


class KX_Mesh(EXP_Value):
    ''' A mesh object. You can only change the vertex properties of a mesh object, not the mesh topology. To use mesh objects effectively, you should know a bit about how the game engine handles them. #. Mesh Objects are converted from Blender at scene load. #. The Converter groups polygons by Material. This means they can be sent to the renderer efficiently. A material holds: #. The texture. #. The Blender material. #. The Tile properties #. The face properties - (From the "Texture Face" panel) #. Transparency & z sorting #. Light layer #. Polygon shape (triangle/quad) #. Game Object #. Vertices will be split by face if necessary. Vertices can only be shared between faces if: #. They are at the same position #. UV coordinates are the same #. Their normals are the same (both polygons are "Set Smooth") #. They are the same color, for example: a cube has 24 vertices: 6 faces with 4 vertices per face. The correct method of iterating over every KX_VertexProxy in a game object
    '''

    materials: typing.List['KX_BlenderMaterial'] = None
    ''' 

    :type: typing.List['KX_BlenderMaterial']
    '''

    numPolygons = None
    ''' '''

    numMaterials = None
    ''' '''

    polygons: typing.List['KX_PolyProxy'] = None
    ''' Returns the list of polygons of this mesh.

    :type: typing.List['KX_PolyProxy']
    '''

    def getMaterialName(self, matid) -> str:
        ''' Gets the name of the specified material.

        :param matid: the specified material.
        :type matid: 
        :rtype: str
        :return: the attached material name.
        '''
        pass

    def getTextureName(self, matid) -> str:
        ''' Gets the name of the specified material's texture.

        :param matid: the specified material
        :type matid: 
        :rtype: str
        :return: the attached material's texture name.
        '''
        pass

    def getVertexArrayLength(self, matid):
        ''' Gets the length of the vertex array associated with the specified material. There is one vertex array for each material.

        :param matid: the specified material
        :type matid: 
        :return: the number of verticies in the vertex array.
        '''
        pass

    def getVertex(self, matid, index) -> 'KX_VertexProxy':
        ''' Gets the specified vertex from the mesh object.

        :param matid: the specified material
        :type matid: 
        :param index: the index into the vertex array.
        :type index: 
        :rtype: 'KX_VertexProxy'
        :return: a vertex object.
        '''
        pass

    def getPolygon(self, index) -> 'KX_PolyProxy':
        ''' Gets the specified polygon from the mesh.

        :param index: polygon number
        :type index: 
        :rtype: 'KX_PolyProxy'
        :return: a polygon object.
        '''
        pass

    def transform(self, matid, matrix):
        ''' Transforms the vertices of a mesh.

        :param matid: material index, -1 transforms all.
        :type matid: 
        :param matrix: transformation matrix.
        :type matrix: 
        '''
        pass

    def transformUV(self, matid, matrix, uv_index=-1, uv_index_from=-1):
        ''' Transforms the vertices UV's of a mesh.

        :param matid: material index, -1 transforms all.
        :type matid: 
        :param matrix: transformation matrix.
        :type matrix: 
        :param uv_index: optional uv index, -1 for all, otherwise 0 or 1.
        :type uv_index: 
        :param uv_index_from: optional uv index to copy from, -1 to transform the current uv.
        :type uv_index_from: 
        '''
        pass

    def replaceMaterial(self, matid, material: 'KX_BlenderMaterial'):
        ''' Replace the material in slot :data: matid by the material :data: material .

        :param matid: The material index.
        :type matid: 
        :param material: The material replacement.
        :type material: 'KX_BlenderMaterial'
        '''
        pass

    def copy(self) -> 'KX_Mesh':
        ''' Return a duplicated mesh.

        :rtype: 'KX_Mesh'
        :return: a duplicated mesh of the current used.
        '''
        pass

    def constructBvh(
            self,
            transform: 'mathutils.Matrix' = 'mathutils.Matrix.Identity(4)',
            epsilon: float = 0) -> 'mathutils.bvhtree.BVHTree':
        ''' Return a BVH tree based on mesh geometry. Indices of tree elements match polygons indices.

        :param transform: The transform 4x4 matrix applied to vertices.
        :type transform: 'mathutils.Matrix'
        :param epsilon: The tree distance epsilon.
        :type epsilon: float
        :rtype: 'mathutils.bvhtree.BVHTree'
        :return: A BVH tree based on mesh geometry.
        '''
        pass


class KX_PythonComponent(EXP_Value):
    ''' Python component can be compared to python logic bricks with parameters. The python component is a script loaded in the UI, this script defined a component class by inheriting from KX_PythonComponent . This class must contain a dictionary of properties: :attr: args and two default functions: :meth: start and :meth: update . The script must have .py extension. The component properties are loaded from the :attr: args attribute from the UI at loading time. When the game start the function :meth: start is called with as arguments a dictionary of the properties' name and value. The :meth: update function is called every frames during the logic stage before running logics bricks, the goal of this function is to handle and process everything. The following component example moves and rotates the object when pressing the keys W, A, S and D. Since the components are loaded for the first time outside the bge, then :attr: bge is a fake module that contains only the class KX_PythonComponent to avoid importing all the bge modules. This behavior is safer but creates some issues at loading when the user want to use functions or attributes from the bge modules other than the KX_PythonComponent class. The way is to not call these functions at loading outside the bge. To detect it, the bge module contains the attribute :attr: __component__ when it's imported outside the bge. The following component example add a "Cube" object at initialization and move it along x for each update. It shows that the user can use functions from scene and load the component outside the bge by setting global attributes in a condition at the beginning of the script. The property types supported are float, integer, boolean, string, set (for enumeration) and Vector 2D, 3D and 4D. The following example show all of these property types.
    '''

    object: 'KX_GameObject' = None
    ''' The object owner of the component.

    :type: 'KX_GameObject'
    '''

    args: dict = None
    ''' Dictionary of the component properties, the keys are string and the value can be: float, integer, Vector(2D/3D/4D), set, string.

    :type: dict
    '''

    def start(self, args: dict):
        ''' Initialize the component.

        :param args: The dictionary of the properties' name and value.
        :type args: dict
        '''
        pass

    def update(self):
        ''' Process the logic of the component.

        '''
        pass


class KX_TextureRenderer(EXP_Value):
    ''' Python API for object doing a render stored in a texture.
    '''

    autoUpdate: bool = None
    ''' Choose to update automatically each frame the texture renderer or not.

    :type: bool
    '''

    viewpointObject: 'KX_GameObject' = None
    ''' The object where the texture renderer will render the scene.

    :type: 'KX_GameObject'
    '''

    enabled: bool = None
    ''' Enable the texture renderer to render the scene.

    :type: bool
    '''

    ignoreLayers = None
    ''' The layers to ignore when rendering.'''

    clipStart: float = None
    ''' The projection view matrix near plane, used for culling.

    :type: float
    '''

    clipEnd: float = None
    ''' The projection view matrix far plane, used for culling.

    :type: float
    '''

    lodDistanceFactor: float = None
    ''' The factor to multiply distance to camera to adjust levels of detail. A float < 1.0f will make the distance to camera used to compute levels of detail decrease.

    :type: float
    '''

    def update(self):
        ''' Request to update this texture renderer during the rendering stage. This function is effective only when :data: autoUpdate is disabled.

        '''
        pass


class SCA_ILogicBrick(EXP_Value):
    ''' Base class for all logic bricks.
    '''

    executePriority: int = None
    ''' This determines the order controllers are evaluated, and actuators are activated (lower priority is executed first).

    :type: int
    '''

    owner: 'KX_GameObject' = None
    ''' The game object this logic brick is attached to (read-only).

    :type: 'KX_GameObject'
    '''

    name: str = None
    ''' The name of this logic brick (read-only).

    :type: str
    '''


class SCA_IObject(EXP_Value):
    ''' This class has no python functions
    '''

    pass


class EXP_ListValue(EXP_PropValue):
    ''' This is a list like object used in the game engine internally that behaves similar to a python list in most ways. As well as the normal index lookup ( val= clist[i] ), EXP_ListValue supports string lookups ( val= scene.objects["Cube"] ) Other operations such as len(clist) , list(clist) , clist[0:10] are also supported.
    '''

    def append(self, val):
        ''' Add an item to the list (like pythons append)

        '''
        pass

    def count(self, val):
        ''' Count the number of instances of a value in the list.

        :return: number of instances
        '''
        pass

    def index(self, val):
        ''' Return the index of a value in the list.

        :return: The index of the value in the list.
        '''
        pass

    def reverse(self):
        ''' Reverse the order of the list.

        '''
        pass

    def get(self, key, default=None):
        ''' Return the value matching key, or the default value if its not found.

        '''
        pass

    def filter(self, name, prop):
        ''' Return a list of items with name matching name regex and with a property matching prop regex. If name is empty every items are checked, if prop is empty no property check is proceeded.

        '''
        pass

    def from_id(self, id):
        ''' This is a funtion especially for the game engine to return a value with a spesific id. Since object names are not always unique, the id of an object can be used to get an object from the EXP_ValueList. Example: Where myObID is an int or long from the id function. This has the advantage that you can store the id in places you could not store a gameObject.

        '''
        pass


class KX_CubeMap(KX_TextureRenderer):
    ''' Python API for realtime cube map textures.
    '''

    pass


class KX_PlanarMap(KX_TextureRenderer):
    ''' Python API for realtime planar map textures.
    '''

    normal: 'mathutils.Vector' = None
    ''' Plane normal used to compute the reflection or refraction orientation of the render camera.

    :type: 'mathutils.Vector'
    '''


class SCA_IActuator(SCA_ILogicBrick):
    ''' Base class for all actuator logic bricks.
    '''

    pass


class SCA_IController(SCA_ILogicBrick):
    ''' Base class for all controller logic bricks.
    '''

    state: int = None
    ''' The controllers state bitmask. This can be used with the GameObject's state to test if the controller is active.

    :type: int
    '''

    sensors: list = None
    ''' A list of sensors linked to this controller.

    :type: list
    '''

    actuators: list = None
    ''' A list of actuators linked to this controller.

    :type: list
    '''

    useHighPriority = None
    ''' When set the controller executes always before all other controllers that dont have this set.'''


class SCA_ISensor(SCA_ILogicBrick):
    ''' Base class for all sensor logic bricks.
    '''

    usePosPulseMode: bool = None
    ''' Flag to turn positive pulse mode on and off.

    :type: bool
    '''

    useNegPulseMode: bool = None
    ''' Flag to turn negative pulse mode on and off.

    :type: bool
    '''

    frequency = None
    ''' The frequency for pulse mode sensors. (Deprecated: use SCA_ISensor.skippedTicks)'''

    skippedTicks = None
    ''' Number of logic ticks skipped between 2 active pulses'''

    level: bool = None
    ''' level Option whether to detect level or edge transition when entering a state. It makes a difference only in case of logic state transition (state actuator). A level detector will immediately generate a pulse, negative or positive depending on the sensor condition, as soon as the state is activated. A edge detector will wait for a state change before generating a pulse. note: mutually exclusive with :data: tap , enabling will disable :data: tap .

    :type: bool
    '''

    tap: bool = None
    ''' When enabled only sensors that are just activated will send a positive event, after this they will be detected as negative by the controllers. This will make a key thats held act as if its only tapped for an instant. note: mutually exclusive with :data: level , enabling will disable :data: level .

    :type: bool
    '''

    invert: bool = None
    ''' Flag to set if this sensor activates on positive or negative events.

    :type: bool
    '''

    triggered: bool = None
    ''' True if this sensor brick is in a positive state. (read-only).

    :type: bool
    '''

    positive: bool = None
    ''' True if this sensor brick is in a positive state. (read-only).

    :type: bool
    '''

    pos_ticks: int = None
    ''' The number of ticks since the last positive pulse (read-only).

    :type: int
    '''

    neg_ticks: int = None
    ''' The number of ticks since the last negative pulse (read-only).

    :type: int
    '''

    status: int = None
    ''' The status of the sensor (read-only): can be one of :ref: these constants<sensor-status> .

    :type: int
    '''

    def reset(self):
        ''' Reset sensor internal state, effect depends on the type of sensor and settings. The sensor is put in its initial state as if it was just activated.

        '''
        pass


class KX_GameObject(SCA_IObject):
    ''' All game objects are derived from this class. Properties assigned to game objects are accessible as attributes of this class. KX_GameObject can be subclassed to extend functionality. For example: When subclassing objects other than empties and meshes, the specific type should be used - e.g. inherit from BL_ArmatureObject when the object to mutate is an armature.
    '''

    name: str = None
    ''' The object's name.

    :type: str
    '''

    mass: float = None
    ''' The object's mass

    :type: float
    '''

    isSuspendDynamics: bool = None
    ''' The object's dynamic state (read-only).

    :type: bool
    '''

    linearDamping: float = None
    ''' The object's linear damping, also known as translational damping. Can be set simultaneously with angular damping using the :py:meth: setDamping method.

    :type: float
    '''

    angularDamping: float = None
    ''' The object's angular damping, also known as rotationation damping. Can be set simultaneously with linear damping using the :py:meth: setDamping method.

    :type: float
    '''

    linVelocityMin: float = None
    ''' Enforces the object keeps moving at a minimum velocity.

    :type: float
    '''

    linVelocityMax: float = None
    ''' Clamp the maximum linear velocity to prevent objects moving beyond a set speed.

    :type: float
    '''

    angularVelocityMin: float = None
    ''' Enforces the object keeps rotating at a minimum velocity. A value of 0.0 disables this.

    :type: float
    '''

    angularVelocityMax: float = None
    ''' Clamp the maximum angular velocity to prevent objects rotating beyond a set speed. A value of 0.0 disables clamping; it does not stop rotation.

    :type: float
    '''

    localInertia = None
    ''' the object's inertia vector in local coordinates. Read only.'''

    parent: 'KX_GameObject' = None
    ''' The object's parent object. (read-only).

    :type: 'KX_GameObject'
    '''

    groupMembers: typing.Union['KX_GameObject', 'EXP_ListValue'] = None
    ''' Returns the list of group members if the object is a group object (dupli group instance), otherwise None is returned.

    :type: typing.Union['KX_GameObject', 'EXP_ListValue']
    '''

    groupObject: 'KX_GameObject' = None
    ''' Returns the group object (dupli group instance) that the object belongs to or None if the object is not part of a group.

    :type: 'KX_GameObject'
    '''

    collisionGroup = None
    ''' The object's collision group.'''

    collisionMask = None
    ''' The object's collision mask.'''

    collisionCallbacks: list = None
    ''' A list of functions to be called when a collision occurs. Callbacks should either accept one argument (object) , or four arguments (object, point, normal, points) . For simplicity, per colliding object the first collision point is reported in second and third argument.

    :type: list
    '''

    scene: 'KX_Scene' = None
    ''' The object's scene. (read-only).

    :type: 'KX_Scene'
    '''

    visible: bool = None
    ''' visibility flag.

    :type: bool
    '''

    layer = None
    ''' The layer mask used for shadow and real-time cube map render.'''

    cullingBox: 'KX_BoundingBox' = None
    ''' The object's bounding volume box used for culling.

    :type: 'KX_BoundingBox'
    '''

    culled: bool = None
    ''' Returns True if the object is culled, else False.

    :type: bool
    '''

    color: 'mathutils.Vector' = None
    ''' The object color of the object. [r, g, b, a]

    :type: 'mathutils.Vector'
    '''

    occlusion: bool = None
    ''' occlusion capability flag.

    :type: bool
    '''

    physicsCulling: bool = None
    ''' True if the object suspends its physics depending on its nearest distance to any camera.

    :type: bool
    '''

    logicCulling: bool = None
    ''' True if the object suspends its logic and animation depending on its nearest distance to any camera.

    :type: bool
    '''

    physicsCullingRadius: float = None
    ''' Suspend object's physics if this radius is smaller than its nearest distance to any camera and :data: physicsCulling set to True .

    :type: float
    '''

    logicCullingRadius: float = None
    ''' Suspend object's logic and animation if this radius is smaller than its nearest distance to any camera and :data: logicCulling set to True .

    :type: float
    '''

    position: 'mathutils.Vector' = None
    ''' The object's position. [x, y, z] On write: local position, on read: world position

    :type: 'mathutils.Vector'
    '''

    orientation: 'mathutils.Matrix' = None
    ''' The object's orientation. 3x3 Matrix. You can also write a Quaternion or Euler vector. On write: local orientation, on read: world orientation

    :type: 'mathutils.Matrix'
    '''

    scaling: 'mathutils.Vector' = None
    ''' The object's scaling factor. [sx, sy, sz] On write: local scaling, on read: world scaling

    :type: 'mathutils.Vector'
    '''

    localOrientation: 'mathutils.Matrix' = None
    ''' The object's local orientation. 3x3 Matrix. You can also write a Quaternion or Euler vector.

    :type: 'mathutils.Matrix'
    '''

    worldOrientation: 'mathutils.Matrix' = None
    ''' The object's world orientation. 3x3 Matrix.

    :type: 'mathutils.Matrix'
    '''

    localScale: 'mathutils.Vector' = None
    ''' The object's local scaling factor. [sx, sy, sz]

    :type: 'mathutils.Vector'
    '''

    worldScale: 'mathutils.Vector' = None
    ''' The object's world scaling factor. [sx, sy, sz]

    :type: 'mathutils.Vector'
    '''

    localPosition: 'mathutils.Vector' = None
    ''' The object's local position. [x, y, z]

    :type: 'mathutils.Vector'
    '''

    worldPosition: 'mathutils.Vector' = None
    ''' The object's world position. [x, y, z]

    :type: 'mathutils.Vector'
    '''

    localTransform: 'mathutils.Matrix' = None
    ''' The object's local space transform matrix. 4x4 Matrix.

    :type: 'mathutils.Matrix'
    '''

    worldTransform: 'mathutils.Matrix' = None
    ''' The object's world space transform matrix. 4x4 Matrix.

    :type: 'mathutils.Matrix'
    '''

    localLinearVelocity: 'mathutils.Vector' = None
    ''' The object's local linear velocity. [x, y, z]

    :type: 'mathutils.Vector'
    '''

    worldLinearVelocity: 'mathutils.Vector' = None
    ''' The object's world linear velocity. [x, y, z]

    :type: 'mathutils.Vector'
    '''

    localAngularVelocity: 'mathutils.Vector' = None
    ''' The object's local angular velocity. [x, y, z]

    :type: 'mathutils.Vector'
    '''

    worldAngularVelocity: 'mathutils.Vector' = None
    ''' The object's world angular velocity. [x, y, z]

    :type: 'mathutils.Vector'
    '''

    gravity: 'mathutils.Vector' = None
    ''' The object's gravity. [x, y, z]

    :type: 'mathutils.Vector'
    '''

    timeOffset: float = None
    ''' adjust the slowparent delay at runtime.

    :type: float
    '''

    state: int = None
    ''' the game object's state bitmask, using the first 30 bits, one bit must always be set.

    :type: int
    '''

    meshes: typing.List['KX_Mesh'] = None
    ''' a list meshes for this object.

    :type: typing.List['KX_Mesh']
    '''

    batchGroup: 'KX_BatchGroup' = None
    ''' The object batch group containing the batched mesh.

    :type: 'KX_BatchGroup'
    '''

    sensors: list = None
    ''' a sequence of SCA_ISensor objects with string/index lookups and iterator support.

    :type: list
    '''

    controllers: typing.List['SCA_ISensor'] = None
    ''' a sequence of SCA_IController objects with string/index lookups and iterator support.

    :type: typing.List['SCA_ISensor']
    '''

    actuators: list = None
    ''' a list of SCA_IActuator with string/index lookups and iterator support.

    :type: list
    '''

    attrDict: dict = None
    ''' get the objects internal python attribute dictionary for direct (faster) access.

    :type: dict
    '''

    components: typing.Union['KX_PythonComponent', 'EXP_ListValue'] = None
    ''' All python components.

    :type: typing.Union['KX_PythonComponent', 'EXP_ListValue']
    '''

    children: typing.Union['KX_GameObject', 'EXP_ListValue'] = None
    ''' direct children of this object, (read-only).

    :type: typing.Union['KX_GameObject', 'EXP_ListValue']
    '''

    childrenRecursive: typing.Union['KX_GameObject', 'EXP_ListValue'] = None
    ''' all children of this object including children's children, (read-only).

    :type: typing.Union['KX_GameObject', 'EXP_ListValue']
    '''

    life: float = None
    ''' The number of frames until the object ends, assumes one frame is 1/50 second (read-only).

    :type: float
    '''

    debug: bool = None
    ''' If true, the object's debug properties will be displayed on screen.

    :type: bool
    '''

    debugRecursive: bool = None
    ''' If true, the object's and children's debug properties will be displayed on screen.

    :type: bool
    '''

    currentLodLevel: int = None
    ''' The index of the level of detail (LOD) currently used by this object (read-only).

    :type: int
    '''

    lodManager: 'KX_LodManager' = None
    ''' Return the lod manager of this object. Needed to access to lod manager to set attributes of levels of detail of this object. The lod manager is shared between instance objects and can be changed to use the lod levels of an other object. If the lod manager is set to None the object's mesh backs to the mesh of the previous first lod level.

    :type: 'KX_LodManager'
    '''

    def endObject(self):
        ''' Delete this object, can be used in place of the EndObject Actuator. The actual removal of the object from the scene is delayed.

        '''
        pass

    def replaceMesh(self,
                    mesh: str,
                    useDisplayMesh: bool = True,
                    usePhysicsMesh: bool = False):
        ''' Replace the mesh of this object with a new mesh. This works the same was as the actuator.

        :param mesh: mesh to replace or the meshes name.
        :type mesh: str
        :param useDisplayMesh: when enabled the display mesh will be replaced (optional argument).
        :type useDisplayMesh: bool
        :param usePhysicsMesh: when enabled the physics mesh will be replaced (optional argument).
        :type usePhysicsMesh: bool
        '''
        pass

    def setVisible(self, visible: bool, recursive: bool):
        ''' Sets the game object's visible flag.

        :param visible: the visible state to set.
        :type visible: bool
        :param recursive: optional argument to set all childrens visibility flag too, defaults to False if no value passed.
        :type recursive: bool
        '''
        pass

    def setOcclusion(self, occlusion: bool, recursive: bool):
        ''' Sets the game object's occlusion capability.

        :param occlusion: the state to set the occlusion to.
        :type occlusion: bool
        :param recursive: optional argument to set all childrens occlusion flag too, defaults to False if no value passed.
        :type recursive: bool
        '''
        pass

    def alignAxisToVect(self, vect, axis=2, factor: float = 1.0):
        ''' Aligns any of the game object's axis along the given vector.

        :param vect: a vector to align the axis.
        :type vect: 
        :param axis: The axis you want to align * 0: X axis * 1: Y axis * 2: Z axis
        :type axis: 
        :param factor: Only rotate a feaction of the distance to the target vector (0.0 - 1.0)
        :type factor: float
        '''
        pass

    def getAxisVect(self, vect: 'mathutils.Vector'):
        ''' Returns the axis vector rotates by the object's worldspace orientation. This is the equivalent of multiplying the vector by the orientation matrix.

        :param vect: a vector to align the axis.
        :type vect: 'mathutils.Vector'
        :return: The vector in relation to the objects rotation.
        '''
        pass

    def applyMovement(self, movement: 'mathutils.Vector', local):
        ''' Sets the game object's movement.

        :param movement: movement vector.
        :type movement: 'mathutils.Vector'
        :param local: 
        :type local: 
        :param local: 
        :type local: 
        '''
        pass

    def applyRotation(self, rotation: 'mathutils.Vector', local):
        ''' Sets the game object's rotation.

        :param rotation: rotation vector.
        :type rotation: 'mathutils.Vector'
        :param local: 
        :type local: 
        :param local: 
        :type local: 
        '''
        pass

    def applyForce(self, force: 'mathutils.Vector', local: bool):
        ''' Sets the game object's force. This requires a dynamic object.

        :param force: force vector.
        :type force: 'mathutils.Vector'
        :param local: * False: get the "global" force ie: relative to world orientation. * True: get the "local" force ie: relative to object orientation. Default to False if not passed.
        :type local: bool
        '''
        pass

    def applyTorque(self, torque: 'mathutils.Vector', local: bool):
        ''' Sets the game object's torque. This requires a dynamic object.

        :param torque: torque vector.
        :type torque: 'mathutils.Vector'
        :param local: * False: get the "global" torque ie: relative to world orientation. * True: get the "local" torque ie: relative to object orientation. Default to False if not passed.
        :type local: bool
        '''
        pass

    def getLinearVelocity(self, local: bool):
        ''' Gets the game object's linear velocity. This method returns the game object's velocity through it's center of mass, ie no angular velocity component.

        :param local: * False: get the "global" velocity ie: relative to world orientation. * True: get the "local" velocity ie: relative to object orientation. Default to False if not passed.
        :type local: bool
        :return: the object's linear velocity.
        '''
        pass

    def setLinearVelocity(self, velocity: 'mathutils.Vector', local: bool):
        ''' Sets the game object's linear velocity. This method sets game object's velocity through it's center of mass, ie no angular velocity component. This requires a dynamic object.

        :param velocity: linear velocity vector.
        :type velocity: 'mathutils.Vector'
        :param local: * False: get the "global" velocity ie: relative to world orientation. * True: get the "local" velocity ie: relative to object orientation. Default to False if not passed.
        :type local: bool
        '''
        pass

    def getAngularVelocity(self, local: bool):
        ''' Gets the game object's angular velocity.

        :param local: * False: get the "global" velocity ie: relative to world orientation. * True: get the "local" velocity ie: relative to object orientation. Default to False if not passed.
        :type local: bool
        :return: the object's angular velocity.
        '''
        pass

    def setAngularVelocity(self, velocity: bool, local):
        ''' Sets the game object's angular velocity. This requires a dynamic object.

        :param velocity: angular velocity vector.
        :type velocity: bool
        :param local: 
        :type local: 
        '''
        pass

    def getVelocity(self, point: 'mathutils.Vector'):
        ''' Gets the game object's velocity at the specified point. Gets the game object's velocity at the specified point, including angular components.

        :param point: optional point to return the velocity for, in local coordinates, defaults to (0, 0, 0) if no value passed.
        :type point: 'mathutils.Vector'
        :return: the velocity at the specified point.
        '''
        pass

    def getReactionForce(self):
        ''' Gets the game object's reaction force. The reaction force is the force applied to this object over the last simulation timestep. This also includes impulses, eg from collisions.

        :return: the reaction force of this object.
        '''
        pass

    def applyImpulse(self, point: 'bpy.context.world',
                     impulse: 'mathutils.Vector', local: bool):
        ''' Applies an impulse to the game object. This will apply the specified impulse to the game object at the specified point. If point != position, applyImpulse will also change the object's angular momentum. Otherwise, only linear momentum will change.

        :param point: the point to apply the impulse to (in world or local coordinates)
        :type point: 'bpy.context.world'
        :param impulse: impulse vector.
        :type impulse: 'mathutils.Vector'
        :param local: * False: get the "global" impulse ie: relative to world coordinates with world orientation. * True: get the "local" impulse ie: relative to local coordinates with object orientation. Default to False if not passed.
        :type local: bool
        '''
        pass

    def setDamping(self, linear_damping: float, angular_damping: float):
        ''' Sets both the :py:attr: linearDamping and :py:attr: angularDamping simultaneously. This is more efficient than setting both properties individually.

        :param linear_damping: Linear ("translational") damping factor.
        :type linear_damping: float
        :param angular_damping: Angular ("rotational") damping factor.
        :type angular_damping: float
        '''
        pass

    def suspendPhysics(self, freeConstraints: bool):
        ''' Suspends physics for this object.

        :param freeConstraints: When set to True physics constraints used by the object are deleted. Else when False (the default) constraints are restored when restoring physics.
        :type freeConstraints: bool
        '''
        pass

    def restorePhysics(self):
        ''' Resumes physics for this object. Also reinstates collisions.

        '''
        pass

    def suspendDynamics(self, ghost: bool):
        ''' Suspends dynamics physics for this object.

        :param ghost: When set to True , collisions with the object will be ignored, similar to the "ghost" checkbox in Blender. When False (the default), the object becomes static but still collide with other objects.
        :type ghost: bool
        '''
        pass

    def restoreDynamics(self):
        ''' Resumes dynamics physics for this object. Also reinstates collisions; the object will no longer be a ghost.

        '''
        pass

    def enableRigidBody(self):
        ''' Enables rigid body physics for this object. Rigid body physics allows the object to roll on collisions.

        '''
        pass

    def disableRigidBody(self):
        ''' Disables rigid body physics for this object.

        '''
        pass

    def setParent(self,
                  parent: 'KX_GameObject',
                  compound: bool = True,
                  ghost: bool = True):
        ''' Sets this object's parent. Control the shape status with the optional compound and ghost parameters: In that case you can control if it should be ghost or not:

        :param parent: new parent object.
        :type parent: 'KX_GameObject'
        :param compound: whether the shape should be added to the parent compound shape. * True: the object shape should be added to the parent compound shape. * False: the object should keep its individual shape.
        :type compound: bool
        :param ghost: whether the object should be ghost while parented. * True: if the object should be made ghost while parented. * False: if the object should be solid while parented.
        :type ghost: bool
        '''
        pass

    def removeParent(self):
        ''' Removes this objects parent.

        '''
        pass

    def getPhysicsId(self):
        ''' Returns the user data object associated with this game object's physics controller.

        '''
        pass

    def getPropertyNames(self) -> list:
        ''' Gets a list of all property names.

        :rtype: list
        :return: All property names for this object.
        '''
        pass

    def getDistanceTo(self, other: typing.List['KX_GameObject']) -> float:
        ''' 

        :param other: KX_GameObject to measure the distance to.
        :type other: typing.List['KX_GameObject']
        :rtype: float
        :return: distance to another object or point.
        '''
        pass

    def getVectTo(self, other: typing.List['KX_GameObject']) -> float:
        ''' Returns the vector and the distance to another object or point. The vector is normalized unless the distance is 0, in which a zero length vector is returned.

        :param other: KX_GameObject to get the vector and distance to.
        :type other: typing.List['KX_GameObject']
        :rtype: float
        :return: (distance, globalVector(3), localVector(3))
        '''
        pass

    def rayCastTo(self,
                  other: 'KX_GameObject',
                  dist: float = 0,
                  prop: str = "") -> 'KX_GameObject':
        ''' Look towards another point/object and find first object hit within dist that matches prop. The ray is always casted from the center of the object, ignoring the object itself. The ray is casted towards the center of another object or an explicit [x, y, z] point. Use rayCast() if you need to retrieve the hit point

        :param other: [x, y, z] or object towards which the ray is casted
        :type other: 'KX_GameObject'
        :param dist: max distance to look (can be negative => look behind); 0 or omitted => detect up to other
        :type dist: float
        :param prop: property name that object must have; can be omitted => detect any object
        :type prop: str
        :rtype: 'KX_GameObject'
        :return: the first object hit or None if no object or object does not match prop
        '''
        pass

    def rayCast(self,
                objto: 'KX_GameObject',
                objfrom: 'KX_GameObject' = None,
                dist: float = 0,
                prop: str = "",
                face=False,
                xray=False,
                poly=0,
                mask=0xFFFF) -> typing.Union['KX_PolyProxy', 'KX_GameObject']:
        ''' Look from a point/object to another point/object and find first object hit within dist that matches prop. if poly is 0, returns a 3-tuple with object reference, hit point and hit normal or (None, None, None) if no hit. if poly is 1, returns a 4-tuple with in addition a KX_PolyProxy as 4th element. if poly is 2, returns a 5-tuple with in addition a 2D vector with the UV mapping of the hit point as 5th element. The face parameter determines the orientation of the normal. * 0 => hit normal is always oriented towards the ray origin (as if you casted the ray from outside) * 1 => hit normal is the real face normal (only for mesh object, otherwise face has no effect) The ray has X-Ray capability if xray parameter is 1, otherwise the first object hit (other than self object) stops the ray. The prop and xray parameters interact as follow. * prop off, xray off: return closest hit or no hit if there is no object on the full extend of the ray. * prop off, xray on : idem. * prop on, xray off: return closest hit if it matches prop, no hit otherwise. * prop on, xray on : return closest hit matching prop or no hit if there is no object matching prop on the full extend of the ray. The KX_PolyProxy 4th element of the return tuple when poly=1 allows to retrieve information on the polygon hit by the ray. If there is no hit or the hit object is not a static mesh, None is returned as 4th element. The ray ignores collision-free objects and faces that dont have the collision flag enabled, you can however use ghost objects.

        :param objto: [x, y, z] or object to which the ray is casted
        :type objto: 'KX_GameObject'
        :param objfrom: [x, y, z] or object from which the ray is casted; None or omitted => use self object center
        :type objfrom: 'KX_GameObject'
        :param dist: max distance to look (can be negative => look behind); 0 or omitted => detect up to to
        :type dist: float
        :param prop: property name that object must have; can be omitted or "" => detect any object
        :type prop: str
        :param face: 1=>return face normal; 0 or omitted => normal is oriented towards origin
        :type face: 
        :param xray: 1=>skip objects that don't match prop; 0 or omitted => stop on first object
        :type xray: 
        :param poly: 0, 1 or 2 to return a 3-, 4- or 5-tuple with information on the face hit. * 0 or omitted: return value is a 3-tuple (object, hitpoint, hitnormal) or (None, None, None) if no hit * 1: return value is a 4-tuple and the 4th element is a KX_PolyProxy or None if no hit or the object doesn't use a mesh collision shape. * 2: return value is a 5-tuple and the 5th element is a 2-tuple (u, v) with the UV mapping of the hit point or None if no hit, or the object doesn't use a mesh collision shape, or doesn't have a UV mapping.
        :type poly: 
        :param mask: The collision mask (16 layers mapped to a 16-bit integer) is combined with each object's collision group, to hit only a subset of the objects in the scene. Only those objects for which collisionGroup & mask is true can be hit.
        :type mask: 
        :rtype: typing.Union['KX_PolyProxy', 'KX_GameObject']
        :return: (object, hitpoint, hitnormal) or (object, hitpoint, hitnormal, polygon) or (object, hitpoint, hitnormal, polygon, hituv). * object, hitpoint and hitnormal are None if no hit. * polygon is valid only if the object is valid and is a static object, a dynamic object using mesh collision shape or a soft body object, otherwise it is None * hituv is valid only if polygon is valid and the object has a UV mapping, otherwise it is None
        '''
        pass

    def collide(self, obj: typing.Union[str, 'KX_GameObject']
                ) -> 'KX_CollisionContactPoint':
        ''' Test if this object collides object :data: obj .

        :param obj: the object to test collision with
        :type obj: typing.Union[str, 'KX_GameObject']
        :rtype: 'KX_CollisionContactPoint'
        :return: (collide, points) * collide, True if this object collides object :data: obj * points, contact point data of the collision or None
        '''
        pass

    def setCollisionMargin(self, margin: float):
        ''' Set the objects collision margin.

        :param margin: the collision margin distance in blender units.
        :type margin: float
        '''
        pass

    def sendMessage(self, subject: str, body: str = "", to: str = ""):
        ''' Sends a message.

        :param subject: The subject of the message
        :type subject: str
        :param body: The body of the message (optional)
        :type body: str
        :param to: The name of the object to send the message to (optional)
        :type to: str
        '''
        pass

    def reinstancePhysicsMesh(self,
                              gameObject: typing.Union[str, 'KX_GameObject'],
                              meshObject: str, dupli: bool) -> bool:
        ''' Updates the physics system with the changed mesh. If no arguments are given the physics mesh will be re-created from the first mesh assigned to the game object.

        :param gameObject: optional argument, set the physics shape from this gameObjets mesh.
        :type gameObject: typing.Union[str, 'KX_GameObject']
        :param meshObject: optional argument, set the physics shape from this mesh.
        :type meshObject: str
        :param dupli: optional argument, duplicate the physics shape.
        :type dupli: bool
        :rtype: bool
        :return: True if reinstance succeeded, False if it failed.
        '''
        pass

    def replacePhysicsShape(
            self, gameObject: typing.Union[str, 'KX_GameObject']) -> bool:
        ''' Replace the current physics shape.

        :param gameObject: set the physics shape from this gameObjets.
        :type gameObject: typing.Union[str, 'KX_GameObject']
        :rtype: bool
        :return: True if replace succeeded, False if it failed.
        '''
        pass

    def get(self, key: str, default):
        ''' Return the value matching key, or the default value if its not found.

        :param key: the matching key
        :type key: str
        :param default: 
        :type default: 
        '''
        pass

    def playAction(self,
                   name: str,
                   start_frame,
                   end_frame,
                   layer=0,
                   priority=0,
                   blendin: float = 0,
                   play_mode='KX_ACTION_MODE_PLAY',
                   layer_weight: float = 0.0,
                   ipo_flags: int = 0,
                   speed: float = 1.0,
                   blend_mode='KX_ACTION_BLEND_BLEND'):
        ''' Plays an action.

        :param name: the name of the action
        :type name: str
        :param start: the start frame of the action
        :type start: float
        :param end: the end frame of the action
        :type end: float
        :param layer: the layer the action will play in (actions in different layers are added/blended together)
        :type layer: 
        :param priority: only play this action if there isn't an action currently playing in this layer with a higher (lower number) priority
        :type priority: 
        :param blendin: the amount of blending between this animation and the previous one on this layer
        :type blendin: float
        :param play_mode: the play mode
        :type play_mode: 
        :param layer_weight: how much of the previous layer to use for blending
        :type layer_weight: float
        :param ipo_flags: flags for the old IPO behaviors (force, etc)
        :type ipo_flags: int
        :param speed: the playback speed of the action as a factor (1.0 = normal speed, 2.0 = 2x speed, etc)
        :type speed: float
        :param blend_mode: how to blend this layer with previous layers
        :type blend_mode: 
        '''
        pass

    def stopAction(self, layer):
        ''' Stop playing the action on the given layer.

        :param layer: The layer to stop playing, defaults to 0 if no value passed.
        :type layer: 
        '''
        pass

    def getActionFrame(self, layer) -> float:
        ''' Gets the current frame of the action playing in the supplied layer.

        :param layer: The layer that you want to get the frame from, defaults to 0 if no value passed.
        :type layer: 
        :rtype: float
        :return: The current frame of the action
        '''
        pass

    def getActionName(self, layer) -> str:
        ''' Gets the name of the current action playing in the supplied layer.

        :param layer: The layer that you want to get the action name from, defaults to 0 if no value passed.
        :type layer: 
        :rtype: str
        :return: The name of the current action
        '''
        pass

    def setActionFrame(self, frame: float, layer):
        ''' Set the current frame of the action playing in the supplied layer.

        :param layer: The layer where you want to set the frame, default to 0 if no value passed.
        :type layer: 
        :param frame: The frame to set the action to
        :type frame: float
        '''
        pass

    def isPlayingAction(self, layer) -> bool:
        ''' Checks to see if there is an action playing in the given layer.

        :param layer: The layer to check for a playing action, defaults to 0 if no value passed.
        :type layer: 
        :rtype: bool
        :return: Whether or not the action is playing
        '''
        pass

    def addDebugProperty(self, name: str, debug: bool):
        ''' Adds a single debug property to the debug list.

        :param name: name of the property that added to the debug list.
        :type name: str
        :param debug: the debug state, default to True is no value passed.
        :type debug: bool
        '''
        pass


class KX_PolyProxy(SCA_IObject):
    ''' A polygon holds the index of the vertex forming the poylgon. Note: The polygon attributes are read-only, you need to retrieve the vertex proxy if you want to change the vertex settings.
    '''

    material_name: str = None
    ''' The name of polygon material, empty if no material.

    :type: str
    '''

    material: 'KX_BlenderMaterial' = None
    ''' The material of the polygon.

    :type: 'KX_BlenderMaterial'
    '''

    texture_name: str = None
    ''' The texture name of the polygon.

    :type: str
    '''

    material_id = None
    ''' The material index of the polygon, use this to retrieve vertex proxy from mesh proxy.'''

    v1 = None
    ''' vertex index of the first vertex of the polygon, use this to retrieve vertex proxy from mesh proxy.'''

    v2 = None
    ''' vertex index of the second vertex of the polygon, use this to retrieve vertex proxy from mesh proxy.'''

    v3 = None
    ''' vertex index of the third vertex of the polygon, use this to retrieve vertex proxy from mesh proxy.'''

    v4 = None
    ''' '''

    visible = None
    ''' visible state of the polygon: 1=visible, 0=invisible.'''

    collide = None
    ''' collide state of the polygon: 1=receives collision, 0=collision free.'''

    vertices: typing.List['KX_VertexProxy'] = None
    ''' Returns the list of vertices of this polygon.

    :type: typing.List['KX_VertexProxy']
    '''

    def getMaterialName(self) -> str:
        ''' Returns the polygon material name with MA prefix

        :rtype: str
        :return: material name
        '''
        pass

    def getMaterial(self) -> 'KX_BlenderMaterial':
        ''' 

        :rtype: 'KX_BlenderMaterial'
        :return: The polygon material
        '''
        pass

    def getTextureName(self) -> str:
        ''' 

        :rtype: str
        :return: The texture name
        '''
        pass

    def getMaterialIndex(self):
        ''' Returns the material bucket index of the polygon. This index and the ones returned by getVertexIndex() are needed to retrieve the vertex proxy from MeshProxy .

        :return: the material index in the mesh
        '''
        pass

    def getNumVertex(self):
        ''' Returns the number of vertex of the polygon.

        :return: number of vertex.
        '''
        pass

    def isVisible(self) -> bool:
        ''' Returns whether the polygon is visible or not

        :rtype: bool
        :return: 0=invisible, 1=visible
        '''
        pass

    def isCollider(self):
        ''' Returns whether the polygon is receives collision or not

        :return: 0=collision free, 1=receives collision
        '''
        pass

    def getVertexIndex(self, vertex):
        ''' Returns the mesh vertex index of a polygon vertex This index and the one returned by getMaterialIndex() are needed to retrieve the vertex proxy from MeshProxy .

        :param vertex: 
        :type vertex: 
        :param vertex: 
        :type vertex: 
        :return: mesh vertex index
        '''
        pass

    def getMesh(self):
        ''' Returns a mesh proxy

        :return: mesh proxy
        '''
        pass


class KX_VertexProxy(SCA_IObject):
    ''' A vertex holds position, UV, color and normal information. Note: The physics simulation is NOT currently updated - physics will not respond to changes in the vertex position.
    '''

    XYZ = None
    ''' The position of the vertex.'''

    UV = None
    ''' The texture coordinates of the vertex.'''

    uvs: list = None
    ''' The texture coordinates list of the vertex.

    :type: list
    '''

    normal = None
    ''' The normal of the vertex.'''

    color = None
    ''' The color of the vertex. Black = [0.0, 0.0, 0.0, 1.0], White = [1.0, 1.0, 1.0, 1.0]'''

    colors: list = None
    ''' The color list of the vertex.

    :type: list
    '''

    x: float = None
    ''' The x coordinate of the vertex.

    :type: float
    '''

    y: float = None
    ''' The y coordinate of the vertex.

    :type: float
    '''

    z: float = None
    ''' The z coordinate of the vertex.

    :type: float
    '''

    u: float = None
    ''' The u texture coordinate of the vertex.

    :type: float
    '''

    v: float = None
    ''' The v texture coordinate of the vertex.

    :type: float
    '''

    u2: float = None
    ''' The second u texture coordinate of the vertex.

    :type: float
    '''

    v2: float = None
    ''' The second v texture coordinate of the vertex.

    :type: float
    '''

    r: float = None
    ''' The red component of the vertex color. 0.0 <= r <= 1.0.

    :type: float
    '''

    g: float = None
    ''' The green component of the vertex color. 0.0 <= g <= 1.0.

    :type: float
    '''

    b: float = None
    ''' The blue component of the vertex color. 0.0 <= b <= 1.0.

    :type: float
    '''

    a: float = None
    ''' The alpha component of the vertex color. 0.0 <= a <= 1.0.

    :type: float
    '''

    def getXYZ(self):
        ''' Gets the position of this vertex.

        :return: this vertexes position in local coordinates.
        '''
        pass

    def setXYZ(self, pos):
        ''' Sets the position of this vertex.

        :param pos: 
        :type pos: 
        '''
        pass

    def getUV(self):
        ''' Gets the UV (texture) coordinates of this vertex.

        :return: this vertexes UV (texture) coordinates.
        '''
        pass

    def setUV(self, uv):
        ''' Sets the UV (texture) coordinates of this vertex.

        '''
        pass

    def getUV2(self):
        ''' Gets the 2nd UV (texture) coordinates of this vertex.

        :return: this vertexes UV (texture) coordinates.
        '''
        pass

    def setUV2(self, uv, unit):
        ''' Sets the 2nd UV (texture) coordinates of this vertex.

        :param unit: 
        :type unit: 
        :param unit: 
        :type unit: 
        '''
        pass

    def getRGBA(self):
        ''' Gets the color of this vertex. The color is represented as four bytes packed into an integer value. The color is packed as RGBA. Since Python offers no way to get each byte without shifting, you must use the struct module to access color in an machine independent way. Because of this, it is suggested you use the r, g, b and a attributes or the color attribute instead.

        :return: packed color. 4 byte integer with one byte per color channel in RGBA format.
        '''
        pass

    def setRGBA(self, col: list):
        ''' Sets the color of this vertex. See getRGBA() for the format of col, and its relevant problems. Use the r, g, b and a attributes or the color attribute instead. setRGBA() also accepts a four component list as argument col. The list represents the color as [r, g, b, a] with black = [0.0, 0.0, 0.0, 1.0] and white = [1.0, 1.0, 1.0, 1.0]

        :param col: the new color of this vertex in packed RGBA format.
        :type col: list
        '''
        pass

    def getNormal(self):
        ''' Gets the normal vector of this vertex.

        :return: normalized normal vector.
        '''
        pass

    def setNormal(self, normal):
        ''' Sets the normal vector of this vertex.

        :param normal: 
        :type normal: 
        '''
        pass


class BL_ActionActuator(SCA_IActuator):
    ''' Action Actuators apply an action to an actor.
    '''

    action: str = None
    ''' The name of the action to set as the current action.

    :type: str
    '''

    frameStart: float = None
    ''' Specifies the starting frame of the animation.

    :type: float
    '''

    frameEnd: float = None
    ''' Specifies the ending frame of the animation.

    :type: float
    '''

    blendIn: float = None
    ''' Specifies the number of frames of animation to generate when making transitions between actions.

    :type: float
    '''

    priority = None
    ''' Sets the priority of this actuator. Actuators will lower priority numbers will override actuators with higher numbers.'''

    frame: float = None
    ''' Sets the current frame for the animation.

    :type: float
    '''

    propName: str = None
    ''' Sets the property to be used in FromProp playback mode.

    :type: str
    '''

    mode = None
    ''' The operation mode of the actuator. Can be one of :ref: these constants<action-actuator> .'''

    useContinue: bool = None
    ''' The actions continue option, True or False. When True, the action will always play from where last left off, otherwise negative events to this actuator will reset it to its start frame.

    :type: bool
    '''

    framePropName: str = None
    ''' The name of the property that is set to the current frame number.

    :type: str
    '''


class BL_ArmatureActuator(SCA_IActuator):
    ''' Armature Actuators change constraint condition on armatures.
    '''

    type = None
    ''' The type of action that the actuator executes when it is active. Can be one of :ref: these constants <armatureactuator-constants-type>'''

    constraint: 'BL_ArmatureConstraint' = None
    ''' The constraint object this actuator is controlling.

    :type: 'BL_ArmatureConstraint'
    '''

    target: 'KX_GameObject' = None
    ''' The object that this actuator will set as primary target to the constraint it controls.

    :type: 'KX_GameObject'
    '''

    subtarget: 'KX_GameObject' = None
    ''' The object that this actuator will set as secondary target to the constraint it controls.

    :type: 'KX_GameObject'
    '''

    weight = None
    ''' The weight this actuator will set on the constraint it controls.'''

    influence = None
    ''' The influence this actuator will set on the constraint it controls.'''


class KX_CameraActuator(SCA_IActuator):
    ''' Applies changes to a camera.
    '''

    damping: float = None
    ''' strength of of the camera following movement.

    :type: float
    '''

    axis: int = None
    ''' The camera axis (0, 1, 2) for positive XYZ , (3, 4, 5) for negative XYZ .

    :type: int
    '''

    min: float = None
    ''' minimum distance to the target object maintained by the actuator.

    :type: float
    '''

    max: float = None
    ''' maximum distance to stay from the target object.

    :type: float
    '''

    height: float = None
    ''' height to stay above the target object.

    :type: float
    '''

    object: 'KX_GameObject' = None
    ''' the object this actuator tracks.

    :type: 'KX_GameObject'
    '''


class KX_ConstraintActuator(SCA_IActuator):
    ''' A constraint actuator limits the position, rotation, distance or orientation of an object.
    '''

    damp = None
    ''' Time constant of the constraint expressed in frame (not use by Force field constraint).'''

    rotDamp = None
    ''' Time constant for the rotation expressed in frame (only for the distance constraint), 0 = use damp for rotation as well.'''

    direction: 'mathutils.Vector' = None
    ''' The reference direction in world coordinate for the orientation constraint.

    :type: 'mathutils.Vector'
    '''

    option = None
    ''' Binary combination of :ref: these constants <constraint-actuator-option>'''

    time = None
    ''' activation time of the actuator. The actuator disables itself after this many frame. If set to 0, the actuator is not limited in time.'''

    propName: str = None
    ''' the name of the property or material for the ray detection of the distance constraint.

    :type: str
    '''

    min: float = None
    ''' The lower bound of the constraint. For the rotation and orientation constraint, it represents radiant.

    :type: float
    '''

    distance: float = None
    ''' the target distance of the distance constraint.

    :type: float
    '''

    max: float = None
    ''' the upper bound of the constraint. For rotation and orientation constraints, it represents radiant.

    :type: float
    '''

    rayLength: float = None
    ''' the length of the ray of the distance constraint.

    :type: float
    '''

    limit = None
    ''' type of constraint. Use one of the :ref: these constants <constraint-actuator-limit>'''


class KX_GameActuator(SCA_IActuator):
    ''' The game actuator loads a new .blend file, restarts the current .blend file or quits the game.
    '''

    fileName: str = None
    ''' the new .blend file to load.

    :type: str
    '''

    mode = None
    ''' The mode of this actuator. Can be on of :ref: these constants <game-actuator>'''


class KX_MouseActuator(SCA_IActuator):
    ''' The mouse actuator gives control over the visibility of the mouse cursor and rotates the parent object according to mouse movement.
    '''

    visible: bool = None
    ''' The visibility of the mouse cursor.

    :type: bool
    '''

    use_axis_x: bool = None
    ''' Mouse movement along the x axis effects object rotation.

    :type: bool
    '''

    use_axis_y: bool = None
    ''' Mouse movement along the y axis effects object rotation.

    :type: bool
    '''

    threshold: 'mathutils.Vector' = None
    ''' Amount of movement from the mouse required before rotation is triggered. The values in the list should be between 0.0 and 0.5.

    :type: 'mathutils.Vector'
    '''

    reset_x: bool = None
    ''' Mouse is locked to the center of the screen on the x axis.

    :type: bool
    '''

    reset_y: bool = None
    ''' Mouse is locked to the center of the screen on the y axis.

    :type: bool
    '''

    object_axis: list = None
    ''' The object's 3D axis to rotate with the mouse movement. ([x, y]) * KX_ACT_MOUSE_OBJECT_AXIS_X * KX_ACT_MOUSE_OBJECT_AXIS_Y * KX_ACT_MOUSE_OBJECT_AXIS_Z

    :type: list
    '''

    local_x: bool = None
    ''' Rotation caused by mouse movement along the x axis is local.

    :type: bool
    '''

    local_y: bool = None
    ''' Rotation caused by mouse movement along the y axis is local.

    :type: bool
    '''

    sensitivity: 'mathutils.Vector' = None
    ''' The amount of rotation caused by mouse movement along the x and y axis. Negative values invert the rotation.

    :type: 'mathutils.Vector'
    '''

    limit_x: 'mathutils.Vector' = None
    ''' The minimum and maximum angle of rotation caused by mouse movement along the x axis in degrees. limit_x[0] is minimum, limit_x[1] is maximum.

    :type: 'mathutils.Vector'
    '''

    limit_y: 'mathutils.Vector' = None
    ''' The minimum and maximum angle of rotation caused by mouse movement along the y axis in degrees. limit_y[0] is minimum, limit_y[1] is maximum.

    :type: 'mathutils.Vector'
    '''

    angle: 'mathutils.Vector' = None
    ''' The current rotational offset caused by the mouse actuator in degrees.

    :type: 'mathutils.Vector'
    '''

    def reset(self):
        ''' Undoes the rotation caused by the mouse actuator.

        '''
        pass


class KX_NetworkMessageActuator(SCA_IActuator):
    ''' Message Actuator
    '''

    propName: str = None
    ''' Messages will only be sent to objects with the given property name.

    :type: str
    '''

    subject: str = None
    ''' The subject field of the message.

    :type: str
    '''

    body: str = None
    ''' The body of the message.

    :type: str
    '''

    usePropBody: bool = None
    ''' Send a property instead of a regular body message.

    :type: bool
    '''


class KX_ObjectActuator(SCA_IActuator):
    ''' The object actuator ("Motion Actuator") applies force, torque, displacement, angular displacement, velocity, or angular velocity to an object. Servo control allows to regulate force to achieve a certain speed target.
    '''

    force = None
    ''' The force applied by the actuator.'''

    useLocalForce: bool = None
    ''' A flag specifying if the force is local.

    :type: bool
    '''

    torque = None
    ''' The torque applied by the actuator.'''

    useLocalTorque: bool = None
    ''' A flag specifying if the torque is local.

    :type: bool
    '''

    dLoc = None
    ''' The displacement vector applied by the actuator.'''

    useLocalDLoc: bool = None
    ''' A flag specifying if the dLoc is local.

    :type: bool
    '''

    dRot = None
    ''' The angular displacement vector applied by the actuator'''

    useLocalDRot: bool = None
    ''' A flag specifying if the dRot is local.

    :type: bool
    '''

    linV = None
    ''' The linear velocity applied by the actuator.'''

    useLocalLinV: bool = None
    ''' A flag specifying if the linear velocity is local.

    :type: bool
    '''

    angV = None
    ''' The angular velocity applied by the actuator.'''

    useLocalAngV: bool = None
    ''' A flag specifying if the angular velocity is local.

    :type: bool
    '''

    damping = None
    ''' The damping parameter of the servo controller.'''

    forceLimitX: typing.List[float] = None
    ''' The min/max force limit along the X axis and activates or deactivates the limits in the servo controller.

    :type: typing.List[float]
    '''

    forceLimitY: typing.List[float] = None
    ''' The min/max force limit along the Y axis and activates or deactivates the limits in the servo controller.

    :type: typing.List[float]
    '''

    forceLimitZ: typing.List[float] = None
    ''' The min/max force limit along the Z axis and activates or deactivates the limits in the servo controller.

    :type: typing.List[float]
    '''

    pid: list = None
    ''' The PID coefficients of the servo controller.

    :type: list
    '''

    reference: 'KX_GameObject' = None
    ''' The object that is used as reference to compute the velocity for the servo controller.

    :type: 'KX_GameObject'
    '''


class KX_ParentActuator(SCA_IActuator):
    ''' The parent actuator can set or remove an objects parent object.
    '''

    object: 'KX_GameObject' = None
    ''' the object this actuator sets the parent too.

    :type: 'KX_GameObject'
    '''

    mode = None
    ''' The mode of this actuator.'''

    compound: bool = None
    ''' Whether the object shape should be added to the parent compound shape when parenting. Effective only if the parent is already a compound shape.

    :type: bool
    '''

    ghost: bool = None
    ''' Whether the object should be made ghost when parenting Effective only if the shape is not added to the parent compound shape.

    :type: bool
    '''


class KX_SCA_AddObjectActuator(SCA_IActuator):
    ''' Edit Object Actuator (in Add Object Mode)
    '''

    object: 'KX_GameObject' = None
    ''' the object this actuator adds.

    :type: 'KX_GameObject'
    '''

    objectLastCreated: 'KX_GameObject' = None
    ''' the last added object from this actuator (read-only).

    :type: 'KX_GameObject'
    '''

    time: float = None
    ''' the lifetime of added objects, in frames. Set to 0 to disable automatic deletion.

    :type: float
    '''

    linearVelocity: list = None
    ''' the initial linear velocity of added objects.

    :type: list
    '''

    angularVelocity: list = None
    ''' the initial angular velocity of added objects.

    :type: list
    '''

    def instantAddObject(self):
        ''' adds the object without needing to calling SCA_PythonController.activate()

        '''
        pass


class KX_SCA_DynamicActuator(SCA_IActuator):
    ''' Dynamic Actuator.
    '''

    mode = None
    ''' the type of operation of the actuator, 0-4 * KX_DYN_RESTORE_DYNAMICS(0) * KX_DYN_DISABLE_DYNAMICS(1) * KX_DYN_ENABLE_RIGID_BODY(2) * KX_DYN_DISABLE_RIGID_BODY(3) * KX_DYN_SET_MASS(4)'''

    mass: float = None
    ''' the mass value for the KX_DYN_SET_MASS operation.

    :type: float
    '''


class KX_SCA_EndObjectActuator(SCA_IActuator):
    ''' Edit Object Actuator (in End Object mode) This actuator has no python methods.
    '''

    pass


class KX_SCA_ReplaceMeshActuator(SCA_IActuator):
    ''' Edit Object actuator, in Replace Mesh mode.
    '''

    mesh: typing.Set['bpy.context.mesh'] = None
    ''' MeshProxy or the name of the mesh that will replace the current one. Set to None to disable actuator.

    :type: typing.Set['bpy.context.mesh']
    '''

    useDisplayMesh: bool = None
    ''' when true the displayed mesh is replaced.

    :type: bool
    '''

    usePhysicsMesh: bool = None
    ''' when true the physics mesh is replaced.

    :type: bool
    '''

    def instantReplaceMesh(self):
        ''' Immediately replace mesh without delay.

        '''
        pass


class KX_SceneActuator(SCA_IActuator):
    ''' Scene Actuator logic brick.
    '''

    scene: str = None
    ''' the name of the scene to change to/overlay/underlay/remove/suspend/resume.

    :type: str
    '''

    camera: typing.Union[str, 'KX_Camera'] = None
    ''' the camera to change to.

    :type: typing.Union[str, 'KX_Camera']
    '''

    useRestart: bool = None
    ''' Set flag to True to restart the sene.

    :type: bool
    '''

    mode = None
    ''' The mode of the actuator.'''


class KX_SoundActuator(SCA_IActuator):
    ''' Sound Actuator. The :data: startSound , :data: pauseSound and :data: stopSound do not require the actuator to be activated - they act instantly provided that the actuator has been activated once at least.
    '''

    volume: float = None
    ''' The volume (gain) of the sound.

    :type: float
    '''

    time: float = None
    ''' The current position in the audio stream (in seconds).

    :type: float
    '''

    pitch: float = None
    ''' The pitch of the sound.

    :type: float
    '''

    mode = None
    ''' The operation mode of the actuator. Can be one of :ref: these constants<logic-sound-actuator>'''

    sound = None
    ''' The sound the actuator should play.'''

    is3D: bool = None
    ''' Whether or not the actuator should be using 3D sound. (read-only)

    :type: bool
    '''

    volume_maximum: float = None
    ''' The maximum gain of the sound, no matter how near it is.

    :type: float
    '''

    volume_minimum: float = None
    ''' The minimum gain of the sound, no matter how far it is away.

    :type: float
    '''

    distance_reference: float = None
    ''' The distance where the sound has a gain of 1.0.

    :type: float
    '''

    distance_maximum: float = None
    ''' The maximum distance at which you can hear the sound.

    :type: float
    '''

    attenuation: float = None
    ''' The influence factor on volume depending on distance.

    :type: float
    '''

    cone_angle_inner: float = None
    ''' The angle of the inner cone.

    :type: float
    '''

    cone_angle_outer: float = None
    ''' The angle of the outer cone.

    :type: float
    '''

    cone_volume_outer: float = None
    ''' The gain outside the outer cone (the gain in the outer cone will be interpolated between this value and the normal gain in the inner cone).

    :type: float
    '''

    def startSound(self):
        ''' Starts the sound.

        '''
        pass

    def pauseSound(self):
        ''' Pauses the sound.

        '''
        pass

    def stopSound(self):
        ''' Stops the sound.

        '''
        pass


class KX_StateActuator(SCA_IActuator):
    ''' State actuator changes the state mask of parent object.
    '''

    operation = None
    ''' Type of bit operation to be applied on object state mask. You can use one of :ref: these constants <state-actuator-operation>'''

    mask = None
    ''' Value that defines the bits that will be modified by the operation. The bits that are 1 in the mask will be updated in the object state. The bits that are 0 are will be left unmodified expect for the Copy operation which copies the mask to the object state.'''


class KX_SteeringActuator(SCA_IActuator):
    ''' Steering Actuator for navigation.
    '''

    behavior = None
    ''' The steering behavior to use.'''

    velocity: float = None
    ''' Velocity magnitude

    :type: float
    '''

    acceleration: float = None
    ''' Max acceleration

    :type: float
    '''

    turnspeed: float = None
    ''' Max turn speed

    :type: float
    '''

    distance: float = None
    ''' Relax distance

    :type: float
    '''

    target: 'KX_GameObject' = None
    ''' Target object

    :type: 'KX_GameObject'
    '''

    navmesh: 'KX_GameObject' = None
    ''' Navigation mesh

    :type: 'KX_GameObject'
    '''

    selfterminated: bool = None
    ''' Terminate when target is reached

    :type: bool
    '''

    enableVisualization: bool = None
    ''' Enable debug visualization

    :type: bool
    '''

    pathUpdatePeriod: int = None
    ''' Path update period

    :type: int
    '''

    path: typing.List['mathutils.Vector'] = None
    ''' Path point list.

    :type: typing.List['mathutils.Vector']
    '''


class KX_TrackToActuator(SCA_IActuator):
    ''' Edit Object actuator in Track To mode.
    '''

    object: 'KX_GameObject' = None
    ''' the object this actuator tracks.

    :type: 'KX_GameObject'
    '''

    time = None
    ''' the time in frames with which to delay the tracking motion.'''

    use3D: bool = None
    ''' the tracking motion to use 3D.

    :type: bool
    '''

    upAxis = None
    ''' The axis that points upward. * KX_TRACK_UPAXIS_POS_X * KX_TRACK_UPAXIS_POS_Y * KX_TRACK_UPAXIS_POS_Z'''

    trackAxis = None
    ''' The axis that points to the target object. * KX_TRACK_TRAXIS_POS_X * KX_TRACK_TRAXIS_POS_Y * KX_TRACK_TRAXIS_POS_Z * KX_TRACK_TRAXIS_NEG_X * KX_TRACK_TRAXIS_NEG_Y * KX_TRACK_TRAXIS_NEG_Z'''


class KX_VisibilityActuator(SCA_IActuator):
    ''' Visibility Actuator.
    '''

    visibility: bool = None
    ''' whether the actuator makes its parent object visible or invisible.

    :type: bool
    '''

    useOcclusion: bool = None
    ''' whether the actuator makes its parent object an occluder or not.

    :type: bool
    '''

    useRecursion: bool = None
    ''' whether the visibility/occlusion should be propagated to all children of the object.

    :type: bool
    '''


class SCA_2DFilterActuator(SCA_IActuator):
    ''' Create, enable and disable 2D filters. The following properties don't have an immediate effect. You must active the actuator to get the result. The actuator is not persistent: it automatically stops itself after setting up the filter but the filter remains active. To stop a filter you must activate the actuator with 'type' set to :data: ~bge.logic.RAS_2DFILTER_DISABLED or :data: ~bge.logic.RAS_2DFILTER_NOFILTER .
    '''

    shaderText: str = None
    ''' shader source code for custom shader.

    :type: str
    '''

    disableMotionBlur = None
    ''' action on motion blur: 0=enable, 1=disable.'''

    mode = None
    ''' Type of 2D filter, use one of :ref: these constants <Two-D-FilterActuator-mode> .'''

    passNumber = None
    ''' order number of filter in the stack of 2D filters. Filters are executed in increasing order of passNb. Only be one filter can be defined per passNb.'''

    value: float = None
    ''' argument for motion blur filter.

    :type: float
    '''


class SCA_PropertyActuator(SCA_IActuator):
    ''' Property Actuator
    '''

    propName: str = None
    ''' the property on which to operate.

    :type: str
    '''

    value: str = None
    ''' the value with which the actuator operates.

    :type: str
    '''

    mode = None
    ''' TODO - add constants to game logic dict!.'''


class SCA_RandomActuator(SCA_IActuator):
    ''' Random Actuator
    '''

    seed = None
    ''' Seed of the random number generator. Equal seeds produce equal series. If the seed is 0, the generator will produce the same value on every call.'''

    para1: float = None
    ''' the first parameter of the active distribution. Refer to the documentation of the generator types for the meaning of this value.

    :type: float
    '''

    para2: float = None
    ''' the second parameter of the active distribution. Refer to the documentation of the generator types for the meaning of this value.

    :type: float
    '''

    distribution = None
    ''' Distribution type. (read-only). Can be one of :ref: these constants <logic-random-distributions>'''

    propName: str = None
    ''' the name of the property to set with the random value. If the generator and property types do not match, the assignment is ignored.

    :type: str
    '''

    def setBoolConst(self, value: bool):
        ''' Sets this generator to produce a constant boolean value.

        :param value: The value to return.
        :type value: bool
        '''
        pass

    def setBoolUniform(self):
        ''' Sets this generator to produce a uniform boolean distribution. The generator will generate True or False with 50% chance.

        '''
        pass

    def setBoolBernouilli(self, value: float):
        ''' Sets this generator to produce a Bernouilli distribution.

        :param value: Specifies the proportion of False values to produce. * 0.0: Always generate True * 1.0: Always generate False
        :type value: float
        '''
        pass

    def setIntConst(self, value):
        ''' Sets this generator to always produce the given value.

        :param value: the value this generator produces.
        :type value: 
        '''
        pass

    def setIntUniform(self, lower_bound, upper_bound):
        ''' Sets this generator to produce a random value between the given lower and upper bounds (inclusive).

        :param lower_bound: 
        :type lower_bound: 
        :param upper_bound: 
        :type upper_bound: 
        '''
        pass

    def setIntPoisson(self, value: float):
        ''' Generate a Poisson-distributed number. This performs a series of Bernouilli tests with parameter value. It returns the number of tries needed to achieve succes.

        :param value: 
        :type value: float
        '''
        pass

    def setFloatConst(self, value: float):
        ''' Always generate the given value.

        :param value: 
        :type value: float
        '''
        pass

    def setFloatUniform(self, lower_bound: float, upper_bound: float):
        ''' Generates a random float between lower_bound and upper_bound with a uniform distribution.

        :param lower_bound: 
        :type lower_bound: float
        :param upper_bound: 
        :type upper_bound: float
        '''
        pass

    def setFloatNormal(self, mean: float, standard_deviation: float):
        ''' Generates a random float from the given normal distribution.

        :param mean: The mean (average) value of the generated numbers
        :type mean: float
        :param standard_deviation: The standard deviation of the generated numbers.
        :type standard_deviation: float
        '''
        pass

    def setFloatNegativeExponential(self, half_life: float):
        ''' Generate negative-exponentially distributed numbers. The half-life 'time' is characterized by half_life.

        :param half_life: 
        :type half_life: float
        '''
        pass


class SCA_VibrationActuator(SCA_IActuator):
    ''' Vibration Actuator.
    '''

    joyindex = None
    ''' Joystick index.'''

    strengthLeft: float = None
    ''' Strength of the Low frequency joystick's motor (placed at left position usually).

    :type: float
    '''

    strengthRight: float = None
    ''' Strength of the High frequency joystick's motor (placed at right position usually).

    :type: float
    '''

    duration = None
    ''' Duration of the vibration in milliseconds.'''

    isVibrating: bool = None
    ''' Check status of joystick vibration

    :type: bool
    '''

    hasVibration: bool = None
    ''' Check if the joystick supports vibration

    :type: bool
    '''

    def startVibration(self):
        ''' Starts the vibration.

        '''
        pass

    def stopVibration(self):
        ''' Stops the vibration.

        '''
        pass


class SCA_ANDController(SCA_IController):
    ''' An AND controller activates only when all linked sensors are activated. There are no special python methods for this controller.
    '''

    pass


class SCA_NANDController(SCA_IController):
    ''' An NAND controller activates when all linked sensors are not active. There are no special python methods for this controller.
    '''

    pass


class SCA_NORController(SCA_IController):
    ''' An NOR controller activates only when all linked sensors are de-activated. There are no special python methods for this controller.
    '''

    pass


class SCA_ORController(SCA_IController):
    ''' An OR controller activates when any connected sensor activates. There are no special python methods for this controller.
    '''

    pass


class SCA_PythonController(SCA_IController):
    ''' A Python controller uses a Python script to activate it's actuators, based on it's sensors.
    '''

    owner: 'KX_GameObject' = None
    ''' The object the controller is attached to.

    :type: 'KX_GameObject'
    '''

    script: str = None
    ''' The value of this variable depends on the execution methid. * When 'Script' execution mode is set this value contains the entire python script as a single string (not the script name as you might expect) which can be modified to run different scripts. * When 'Module' execution mode is set this value will contain a single line string - module name and function "module.func" or "package.modile.func" where the module names are python textblocks or external scripts.

    :type: str
    '''

    mode = None
    ''' the execution mode for this controller (read-only). * Script: 0, Execite the :data: script as a python code. * Module: 1, Execite the :data: script as a module and function.'''

    def activate(self, actuator: str):
        ''' Activates an actuator attached to this controller.

        :param actuator: The actuator to operate on.
        :type actuator: str
        '''
        pass

    def deactivate(self, actuator: str):
        ''' Deactivates an actuator attached to this controller.

        :param actuator: The actuator to operate on.
        :type actuator: str
        '''
        pass


class SCA_XNORController(SCA_IController):
    ''' An XNOR controller activates when all linked sensors are the same (activated or inative). There are no special python methods for this controller.
    '''

    pass


class SCA_XORController(SCA_IController):
    ''' An XOR controller activates when there is the input is mixed, but not when all are on or off. There are no special python methods for this controller.
    '''

    pass


class KX_ArmatureSensor(SCA_ISensor):
    ''' Armature sensor detect conditions on armatures.
    '''

    type = None
    ''' The type of measurement that the sensor make when it is active. Can be one of :ref: these constants <armaturesensor-type>'''

    constraint: 'BL_ArmatureConstraint' = None
    ''' The constraint object this sensor is watching.

    :type: 'BL_ArmatureConstraint'
    '''

    value: float = None
    ''' The threshold used in the comparison with the constraint error The linear error is only updated on CopyPose/Distance IK constraint with iTaSC solver The rotation error is only updated on CopyPose+rotation IK constraint with iTaSC solver The linear error on CopyPose is always >= 0: it is the norm of the distance between the target and the bone The rotation error on CopyPose is always >= 0: it is the norm of the equivalent rotation vector between the bone and the target orientations The linear error on Distance can be positive if the distance between the bone and the target is greater than the desired distance, and negative if the distance is smaller.

    :type: float
    '''


class KX_CollisionSensor(SCA_ISensor):
    ''' Collision sensor detects collisions between objects.
    '''

    propName: str = None
    ''' The property or material to collide with.

    :type: str
    '''

    useMaterial: bool = None
    ''' Determines if the sensor is looking for a property or material. KX_True = Find material; KX_False = Find property.

    :type: bool
    '''

    usePulseCollision: bool = None
    ''' When enabled, changes to the set of colliding objects generate a pulse.

    :type: bool
    '''

    hitObject: 'KX_GameObject' = None
    ''' The last collided object. (read-only).

    :type: 'KX_GameObject'
    '''

    hitObjectList: typing.Union['KX_GameObject', 'EXP_ListValue'] = None
    ''' A list of colliding objects. (read-only).

    :type: typing.Union['KX_GameObject', 'EXP_ListValue']
    '''

    hitMaterial: str = None
    ''' The material of the object in the face hit by the ray. (read-only).

    :type: str
    '''


class KX_NetworkMessageSensor(SCA_ISensor):
    ''' The Message Sensor logic brick. Currently only loopback (local) networks are supported.
    '''

    subject: str = None
    ''' The subject the sensor is looking for.

    :type: str
    '''

    frameMessageCount = None
    ''' The number of messages received since the last frame. (read-only).'''

    subjects: list = None
    ''' The list of message subjects received. (read-only).

    :type: list
    '''

    bodies: list = None
    ''' The list of message bodies received. (read-only).

    :type: list
    '''


class KX_RaySensor(SCA_ISensor):
    ''' A ray sensor detects the first object in a given direction.
    '''

    propName: str = None
    ''' The property the ray is looking for.

    :type: str
    '''

    range: float = None
    ''' The distance of the ray.

    :type: float
    '''

    useMaterial: bool = None
    ''' Whether or not to look for a material (false = property).

    :type: bool
    '''

    useXRay: bool = None
    ''' Whether or not to use XRay.

    :type: bool
    '''

    mask = None
    ''' The collision mask (16 layers mapped to a 16-bit integer) combined with each object's collision group, to hit only a subset of the objects in the scene. Only those objects for which collisionGroup & mask is true can be hit.'''

    hitObject: 'KX_GameObject' = None
    ''' The game object that was hit by the ray. (read-only).

    :type: 'KX_GameObject'
    '''

    hitPosition: 'mathutils.Vector' = None
    ''' The position (in worldcoordinates) where the object was hit by the ray. (read-only).

    :type: 'mathutils.Vector'
    '''

    hitNormal: 'mathutils.Vector' = None
    ''' The normal (in worldcoordinates) of the object at the location where the object was hit by the ray. (read-only).

    :type: 'mathutils.Vector'
    '''

    hitMaterial: str = None
    ''' The material of the object in the face hit by the ray. (read-only).

    :type: str
    '''

    rayDirection: 'mathutils.Vector' = None
    ''' The direction from the ray (in worldcoordinates). (read-only).

    :type: 'mathutils.Vector'
    '''

    axis = None
    ''' The axis the ray is pointing on. * KX_RAY_AXIS_POS_X * KX_RAY_AXIS_POS_Y * KX_RAY_AXIS_POS_Z * KX_RAY_AXIS_NEG_X * KX_RAY_AXIS_NEG_Y * KX_RAY_AXIS_NEG_Z'''


class SCA_ActuatorSensor(SCA_ISensor):
    ''' Actuator sensor detect change in actuator state of the parent object. It generates a positive pulse if the corresponding actuator is activated and a negative pulse if the actuator is deactivated.
    '''

    actuator: str = None
    ''' the name of the actuator that the sensor is monitoring.

    :type: str
    '''


class SCA_AlwaysSensor(SCA_ISensor):
    ''' This sensor is always activated.
    '''

    pass


class SCA_DelaySensor(SCA_ISensor):
    ''' The Delay sensor generates positive and negative triggers at precise time, expressed in number of frames. The delay parameter defines the length of the initial OFF period. A positive trigger is generated at the end of this period. The duration parameter defines the length of the ON period following the OFF period. There is a negative trigger at the end of the ON period. If duration is 0, the sensor stays ON and there is no negative trigger. The sensor runs the OFF-ON cycle once unless the repeat option is set: the OFF-ON cycle repeats indefinately (or the OFF cycle if duration is 0). Use SCA_ISensor.reset at any time to restart sensor.
    '''

    delay = None
    ''' length of the initial OFF period as number of frame, 0 for immediate trigger.'''

    duration = None
    ''' length of the ON period in number of frame after the initial OFF period. If duration is greater than 0, a negative trigger is sent at the end of the ON pulse.'''

    repeat = None
    ''' 1 if the OFF-ON cycle should be repeated indefinately, 0 if it should run once.'''


class SCA_JoystickSensor(SCA_ISensor):
    ''' This sensor detects player joystick events.
    '''

    axisValues: list = None
    ''' The state of the joysticks axis as a list of values :data: numAxis long. (read-only). Each specifying the value of an axis between -32767 and 32767 depending on how far the axis is pushed, 0 for nothing. The first 2 values are used by most joysticks and gamepads for directional control. 3rd and 4th values are only on some joysticks and can be used for arbitary controls. * left:[-32767, 0, ...] * right:[32767, 0, ...] * up:[0, -32767, ...] * down:[0, 32767, ...]

    :type: list
    '''

    axisSingle = None
    ''' like :data: axisValues but returns a single axis value that is set by the sensor. (read-only).'''

    numAxis = None
    ''' The number of axes for the joystick at this index. (read-only).'''

    numButtons = None
    ''' The number of buttons for the joystick at this index. (read-only).'''

    connected: bool = None
    ''' True if a joystick is connected at this joysticks index. (read-only).

    :type: bool
    '''

    index = None
    ''' The joystick index to use (from 0 to 7). The first joystick is always 0.'''

    threshold = None
    ''' Axis threshold. Joystick axis motion below this threshold wont trigger an event. Use values between (0 and 32767), lower values are more sensitive.'''

    button = None
    ''' The button index the sensor reacts to (first button = 0). When the "All Events" toggle is set, this option has no effect.'''

    axis = None
    ''' The axis this sensor reacts to, as a list of two values [axisIndex, axisDirection] * axisIndex: the axis index to use when detecting axis movement, 1=primary directional control, 2=secondary directional control. * axisDirection: 0=right, 1=up, 2=left, 3=down.'''

    def getButtonActiveList(self) -> list:
        ''' 

        :rtype: list
        :return: A list containing the indicies of the currently pressed buttons.
        '''
        pass

    def getButtonStatus(self, buttonIndex) -> bool:
        ''' 

        :param buttonIndex: the button index, 0=first button
        :type buttonIndex: 
        :rtype: bool
        :return: The current pressed state of the specified button.
        '''
        pass


class SCA_KeyboardSensor(SCA_ISensor):
    ''' A keyboard sensor detects player key presses. See module :mod: bge.events for keycode values.
    '''

    key = None
    ''' The key code this sensor is looking for.'''

    hold1 = None
    ''' The key code for the first modifier this sensor is looking for.'''

    hold2 = None
    ''' The key code for the second modifier this sensor is looking for.'''

    toggleProperty: str = None
    ''' The name of the property that indicates whether or not to log keystrokes as a string.

    :type: str
    '''

    targetProperty: str = None
    ''' The name of the property that receives keystrokes in case in case a string is logged.

    :type: str
    '''

    useAllKeys: bool = None
    ''' Flag to determine whether or not to accept all keys.

    :type: bool
    '''

    inputs: 'SCA_InputEvent' = None
    ''' A list of pressed input keys that have either been pressed, or just released, or are active this frame. (read-only).

    :type: 'SCA_InputEvent'
    '''

    events: list = None
    ''' a list of pressed keys that have either been pressed, or just released, or are active this frame. (read-only).

    :type: list
    '''

    def getKeyStatus(self, keycode) -> int:
        ''' Get the status of a key.

        :param keycode: these constants<keyboard-keys>
        :type keycode: 
        :rtype: int
        :return: these constants<input-status>
        '''
        pass


class SCA_MouseSensor(SCA_ISensor):
    ''' Mouse Sensor logic brick.
    '''

    position = None
    ''' current [x, y] coordinates of the mouse, in frame coordinates (pixels).'''

    mode = None
    ''' sensor mode. * KX_MOUSESENSORMODE_LEFTBUTTON(1) * KX_MOUSESENSORMODE_MIDDLEBUTTON(2) * KX_MOUSESENSORMODE_RIGHTBUTTON(3) * KX_MOUSESENSORMODE_WHEELUP(4) * KX_MOUSESENSORMODE_WHEELDOWN(5) * KX_MOUSESENSORMODE_MOVEMENT(6)'''

    def getButtonStatus(self, button: int) -> int:
        ''' Get the mouse button status.

        :param button: these constants<mouse-keys>
        :type button: int
        :rtype: int
        :return: these constants<input-status>
        '''
        pass


class SCA_PropertySensor(SCA_ISensor):
    ''' Activates when the game object property matches.
    '''

    mode = None
    ''' Type of check on the property. Can be one of :ref: these constants <logic-property-sensor>'''

    propName: str = None
    ''' the property the sensor operates.

    :type: str
    '''

    value: str = None
    ''' the value with which the sensor compares to the value of the property.

    :type: str
    '''

    min: str = None
    ''' the minimum value of the range used to evaluate the property when in interval mode.

    :type: str
    '''

    max: str = None
    ''' the maximum value of the range used to evaluate the property when in interval mode.

    :type: str
    '''


class SCA_RandomSensor(SCA_ISensor):
    ''' This sensor activates randomly.
    '''

    lastDraw = None
    ''' The seed of the random number generator.'''

    seed = None
    ''' The seed of the random number generator.'''


class BL_ArmatureObject(KX_GameObject):
    ''' An armature object.
    '''

    constraints: typing.List['BL_ArmatureConstraint'] = None
    ''' The list of armature constraint defined on this armature. Elements of the list can be accessed by index or string. The key format for string access is '<bone_name>:<constraint_name>'.

    :type: typing.List['BL_ArmatureConstraint']
    '''

    channels: typing.List['BL_ArmatureChannel'] = None
    ''' The list of armature channels. Elements of the list can be accessed by index or name the bone.

    :type: typing.List['BL_ArmatureChannel']
    '''

    def update(self):
        ''' Ensures that the armature will be updated on next graphic frame. This action is unecessary if a KX_ArmatureActuator with mode run is active or if an action is playing. Use this function in other cases. It must be called on each frame to ensure that the armature is updated continously.

        '''
        pass

    def draw(self):
        ''' Draw lines that represent armature to view it in real time.

        '''
        pass


class KX_Camera(KX_GameObject):
    ''' A Camera object.
    '''

    INSIDE = None
    ''' See :data: sphereInsideFrustum and :data: boxInsideFrustum'''

    INTERSECT = None
    ''' See :data: sphereInsideFrustum and :data: boxInsideFrustum'''

    OUTSIDE = None
    ''' See :data: sphereInsideFrustum and :data: boxInsideFrustum'''

    lens: float = None
    ''' The camera's lens value.

    :type: float
    '''

    lodDistanceFactor: float = None
    ''' The factor to multiply distance to camera to adjust levels of detail. A float < 1.0f will make the distance to camera used to compute levels of detail decrease.

    :type: float
    '''

    fov: float = None
    ''' The camera's field of view value.

    :type: float
    '''

    ortho_scale: float = None
    ''' The camera's view scale when in orthographic mode.

    :type: float
    '''

    near: float = None
    ''' The camera's near clip distance.

    :type: float
    '''

    far: float = None
    ''' The camera's far clip distance.

    :type: float
    '''

    shift_x: float = None
    ''' The camera's horizontal shift.

    :type: float
    '''

    shift_y: float = None
    ''' The camera's vertical shift.

    :type: float
    '''

    perspective: bool = None
    ''' True if this camera has a perspective transform, False for an orthographic projection.

    :type: bool
    '''

    frustum_culling: bool = None
    ''' True if this camera is frustum culling.

    :type: bool
    '''

    activityCulling: bool = None
    ''' True if this camera is used to compute object distance for object activity culling.

    :type: bool
    '''

    projection_matrix: 'mathutils.Matrix' = None
    ''' This camera's 4x4 projection matrix.

    :type: 'mathutils.Matrix'
    '''

    projectionMatrixLeft: 'mathutils.Matrix' = None
    ''' This camera's 4x4 left eye projection matrix.

    :type: 'mathutils.Matrix'
    '''

    projectionMatrixRight: 'mathutils.Matrix' = None
    ''' This camera's 4x4 right eye projection matrix.

    :type: 'mathutils.Matrix'
    '''

    modelview_matrix: 'mathutils.Matrix' = None
    ''' This camera's 4x4 model view matrix. (read-only).

    :type: 'mathutils.Matrix'
    '''

    camera_to_world: 'mathutils.Matrix' = None
    ''' This camera's camera to world transform. (read-only).

    :type: 'mathutils.Matrix'
    '''

    world_to_camera: 'mathutils.Matrix' = None
    ''' This camera's world to camera transform. (read-only).

    :type: 'mathutils.Matrix'
    '''

    useViewport: bool = None
    ''' True when the camera is used as a viewport, set True to enable a viewport for this camera.

    :type: bool
    '''

    def sphereInsideFrustum(self, centre: list, radius: float):
        ''' Tests the given sphere against the view frustum.

        :param centre: The centre of the sphere (in world coordinates.)
        :type centre: list
        :param radius: the radius of the sphere
        :type radius: float
        :return: ~bge.types.KX_Camera.INTERSECT
        '''
        pass

    def boxInsideFrustum(self, box: list):
        ''' Tests the given box against the view frustum.

        :param box: Eight (8) corner points of the box (in world coordinates.)
        :type box: list
        '''
        pass

    def pointInsideFrustum(self, point: 'mathutils.Vector') -> bool:
        ''' Tests the given point against the view frustum.

        :param point: The point to test (in world coordinates.)
        :type point: 'mathutils.Vector'
        :rtype: bool
        :return: True if the given point is inside this camera's viewing frustum.
        '''
        pass

    def getCameraToWorld(self) -> list:
        ''' Returns the camera-to-world transform.

        :rtype: list
        :return: the camera-to-world transform matrix.
        '''
        pass

    def getWorldToCamera(self) -> list:
        ''' Returns the world-to-camera transform. This returns the inverse matrix of getCameraToWorld().

        :rtype: list
        :return: the world-to-camera transform matrix.
        '''
        pass

    def setOnTop(self):
        ''' Set this cameras viewport ontop of all other viewport.

        '''
        pass

    def setViewport(self, left, bottom, right, top):
        ''' Sets the region of this viewport on the screen in pixels. Use :data: bge.render.getWindowHeight and :data: bge.render.getWindowWidth to calculate values relative to the entire display.

        :param left: left pixel coordinate of this viewport
        :type left: 
        :param bottom: bottom pixel coordinate of this viewport
        :type bottom: 
        :param right: right pixel coordinate of this viewport
        :type right: 
        :param top: top pixel coordinate of this viewport
        :type top: 
        '''
        pass

    def getScreenPosition(
            self,
            object: typing.Union['KX_GameObject', 'mathutils.Vector']) -> list:
        ''' Gets the position of an object projected on screen space.

        :param object: object name or list [x, y, z]
        :type object: typing.Union['KX_GameObject', 'mathutils.Vector']
        :rtype: list
        :return: the object's position in screen coordinates.
        '''
        pass

    def getScreenVect(self, x: float, y: float) -> 'mathutils.Vector':
        ''' Gets the vector from the camera position in the screen coordinate direction.

        :param x: X Axis
        :type x: float
        :param y: Y Axis
        :type y: float
        :rtype: 'mathutils.Vector'
        :return: The vector from screen coordinate.
        '''
        pass

    def getScreenRay(self,
                     x: float,
                     y: float,
                     dist: float = 'inf',
                     property: str = None) -> 'KX_GameObject':
        ''' Look towards a screen coordinate (x, y) and find first object hit within dist that matches prop. The ray is similar to KX_GameObject->rayCastTo.

        :param x: X Axis
        :type x: float
        :param y: Y Axis
        :type y: float
        :param dist: max distance to look (can be negative => look behind); 0 or omitted => detect up to other
        :type dist: float
        :param property: property name that object must have; can be omitted => detect any object
        :type property: str
        :rtype: 'KX_GameObject'
        :return: the first object hit or None if no object or object does not match prop
        '''
        pass


class KX_FontObject(KX_GameObject):
    ''' A Font object.
    '''

    text: str = None
    ''' The text displayed by this Font object.

    :type: str
    '''

    resolution: float = None
    ''' The resolution of the font police.

    :type: float
    '''

    size: float = None
    ''' The size (scale factor) of the font object, scaled from font object origin (affects text resolution).

    :type: float
    '''

    dimensions: 'mathutils.Vector' = None
    ''' The size (width and height) of the current text in Blender Units.

    :type: 'mathutils.Vector'
    '''


class KX_LightObject(KX_GameObject):
    ''' A Light object.
    '''

    SPOT = None
    ''' A spot light source. See attribute :data: type'''

    SUN = None
    ''' A point light source with no attenuation. See attribute :data: type'''

    NORMAL = None
    ''' A point light source. See attribute :data: type'''

    HEMI = None
    ''' A hemi light source. See attribute :data: type'''

    type = None
    ''' The type of light - must be SPOT, SUN or NORMAL'''

    energy: float = None
    ''' The brightness of this light.

    :type: float
    '''

    shadowClipStart: float = None
    ''' The shadowmap clip start, below which objects will not generate shadows.

    :type: float
    '''

    shadowClipEnd: float = None
    ''' The shadowmap clip end, beyond which objects will not generate shadows.

    :type: float
    '''

    shadowFrustumSize: float = None
    ''' Size of the frustum used for creating the shadowmap.

    :type: float
    '''

    shadowBindId: int = None
    ''' The OpenGL shadow texture bind number/id.

    :type: int
    '''

    shadowMapType: int = None
    ''' The shadow shadow map type (0 -> Simple; 1 -> Variance)

    :type: int
    '''

    shadowBias: float = None
    ''' The shadow buffer sampling bias.

    :type: float
    '''

    shadowBleedBias: float = None
    ''' The bias for reducing light-bleed on variance shadow maps.

    :type: float
    '''

    useShadow: bool = None
    ''' Returns True if the light has Shadow option activated, else returns False.

    :type: bool
    '''

    shadowColor: 'mathutils.Color' = None
    ''' The color of this light shadows. Black = (0.0, 0.0, 0.0), White = (1.0, 1.0, 1.0).

    :type: 'mathutils.Color'
    '''

    shadowMatrix = None
    ''' Matrix that converts a vector in camera space to shadow buffer depth space. Computed as: mat4_perspective_to_depth * mat4_lamp_to_perspective * mat4_world_to_lamp * mat4_cam_to_world. mat4_perspective_to_depth is a fixed matrix defined as follow: 0.5 0.0 0.0 0.5 0.0 0.5 0.0 0.5 0.0 0.0 0.5 0.5 0.0 0.0 0.0 1.0'''

    distance: float = None
    ''' The maximum distance this light can illuminate. (SPOT and NORMAL lights only).

    :type: float
    '''

    color: list = None
    ''' The color of this light. Black = [0.0, 0.0, 0.0], White = [1.0, 1.0, 1.0].

    :type: list
    '''

    lin_attenuation: float = None
    ''' The linear component of this light's attenuation. (SPOT and NORMAL lights only).

    :type: float
    '''

    quad_attenuation: float = None
    ''' The quadratic component of this light's attenuation (SPOT and NORMAL lights only).

    :type: float
    '''

    spotsize: float = None
    ''' The cone angle of the spot light, in degrees (SPOT lights only).

    :type: float
    '''

    spotblend: float = None
    ''' Specifies the intensity distribution of the spot light (SPOT lights only).

    :type: float
    '''

    staticShadow = None
    ''' Enables static shadows. By default (staticShadow=False) the shadow cast by the lamp is recalculated every frame. When this is not needed, set staticShadow=True. In that case, call :py:meth: updateShadow to request a shadow update.'''

    def updateShadow(self):
        ''' Set the shadow to be updated next frame if the lamp uses a static shadow, see :data: staticShadow .

        '''
        pass


class KX_NavMeshObject(KX_GameObject):
    ''' Python interface for using and controlling navigation meshes.
    '''

    def findPath(self, start, goal) -> list:
        ''' Finds the path from start to goal points.

        :param start: 
        :type start: 
        :param start: 
        :type start: 
        :param goal: 
        :type goal: 
        :param start: 
        :type start: 
        :rtype: list
        :return: a path as a list of points
        '''
        pass

    def raycast(self, start, goal) -> float:
        ''' Raycast from start to goal points.

        :param start: 
        :type start: 
        :param start: 
        :type start: 
        :param goal: 
        :type goal: 
        :param start: 
        :type start: 
        :rtype: float
        :return: the hit factor
        '''
        pass

    def draw(self, mode):
        ''' Draws a debug mesh for the navigation mesh.

        :param mode: 
        :type mode: 
        :param mode: 
        :type mode: 
        '''
        pass

    def rebuild(self):
        ''' Rebuild the navigation mesh.

        '''
        pass


class KX_NearSensor(KX_CollisionSensor):
    ''' A near sensor is a specialised form of touch sensor.
    '''

    distance: float = None
    ''' The near sensor activates when an object is within this distance.

    :type: float
    '''

    resetDistance: float = None
    ''' The near sensor deactivates when the object exceeds this distance.

    :type: float
    '''


class KX_MouseFocusSensor(SCA_MouseSensor):
    ''' The mouse focus sensor detects when the mouse is over the current game object. The mouse focus sensor works by transforming the mouse coordinates from 2d device space to 3d space then raycasting away from the camera.
    '''

    raySource: list = None
    ''' The worldspace source of the ray (the view position).

    :type: list
    '''

    rayTarget: list = None
    ''' The worldspace target of the ray.

    :type: list
    '''

    rayDirection: list = None
    ''' The :data: rayTarget - raySource normalized.

    :type: list
    '''

    hitObject: 'KX_GameObject' = None
    ''' the last object the mouse was over.

    :type: 'KX_GameObject'
    '''

    hitPosition: list = None
    ''' The worldspace position of the ray intersecton.

    :type: list
    '''

    hitNormal: list = None
    ''' the worldspace normal from the face at point of intersection.

    :type: list
    '''

    hitUV: list = None
    ''' the UV coordinates at the point of intersection. If the object has no UV mapping, it returns [0, 0]. The UV coordinates are not normalized, they can be < 0 or > 1 depending on the UV mapping.

    :type: list
    '''

    usePulseFocus: bool = None
    ''' When enabled, moving the mouse over a different object generates a pulse. (only used when the 'Mouse Over Any' sensor option is set).

    :type: bool
    '''

    useXRay: bool = None
    ''' If enabled it allows the sensor to see through game objects that don't have the selected property or material.

    :type: bool
    '''

    mask = None
    ''' The collision mask (16 layers mapped to a 16-bit integer) combined with each object's collision group, to hit only a subset of the objects in the scene. Only those objects for which collisionGroup & mask is true can be hit.'''

    propName: str = None
    ''' The property or material the sensor is looking for.

    :type: str
    '''

    useMaterial: bool = None
    ''' Determines if the sensor is looking for a property or material. KX_True = Find material; KX_False = Find property.

    :type: bool
    '''


class KX_RadarSensor(KX_NearSensor):
    ''' Radar sensor is a near sensor with a conical sensor object.
    '''

    coneOrigin: 'mathutils.Vector' = None
    ''' The origin of the cone with which to test. The origin is in the middle of the cone. (read-only).

    :type: 'mathutils.Vector'
    '''

    coneTarget: 'mathutils.Vector' = None
    ''' The center of the bottom face of the cone with which to test. (read-only).

    :type: 'mathutils.Vector'
    '''

    distance: float = None
    ''' The height of the cone with which to test.

    :type: float
    '''

    angle: float = None
    ''' The angle of the cone (in degrees) with which to test.

    :type: float
    '''

    axis = None
    ''' The axis on which the radar cone is cast. KX_RADAR_AXIS_POS_X, KX_RADAR_AXIS_POS_Y, KX_RADAR_AXIS_POS_Z, KX_RADAR_AXIS_NEG_X, KX_RADAR_AXIS_NEG_Y, KX_RADAR_AXIS_NEG_Z'''
