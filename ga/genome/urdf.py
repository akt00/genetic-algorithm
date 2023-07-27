from .type import *


class URDFLink:
    def __init__(self, name: str, parent_name: str, recur: int,
                 link_length: float = 0.1,
                 link_radius: float = 0.1,
                 link_mass: float = 0.1,
                 joint_type: float = 0.1,
                 joint_parent: float = 0.1,
                 joint_axis_xyz: float = 0.1,
                 joint_origin_rpy_1: float = 0.1,
                 joint_origin_rpy_2: float = 0.1,
                 joint_origin_rpy_3: float = 0.1,
                 joint_origin_xyz_1: float = 0.1,
                 joint_origin_xyz_2: float = 0.1,
                 joint_origin_xyz_3: float = 0.1,
                 control_waveform: float = 0.1,
                 control_amp: float = 0.1,
                 control_freq: float = 0.1):
        self.name = name
        self.parent_name = parent_name
        self.recur = recur
        self.link_length = link_length
        self.link_radius = link_radius
        self.link_mass = link_mass
        self.joint_type = joint_type
        self.joint_parent = joint_parent
        self.joint_axis_xyz = joint_axis_xyz
        self.joint_origin_rpy_1 = joint_origin_rpy_1
        self.joint_origin_rpy_2 = joint_origin_rpy_2
        self.joint_origin_rpy_3 = joint_origin_rpy_3
        self.joint_origin_xyz_1 = joint_origin_xyz_1
        self.joint_origin_xyz_2 = joint_origin_xyz_2
        self.joint_origin_xyz_3 = joint_origin_xyz_3
        self.control_waveform = control_waveform
        self.control_amp = control_amp
        self.control_freq = control_freq

        self.sibling_index = 1

    def to_link_element(self, adom: xmlDocument) -> xmlElement:
        """
        <link name="base_link">
            <visual>
                <geometry>
                    <cylinder length="0.6" radius="0.25"/>
                </geometry>
            </visual>
            <collision>
                <geometry>
                    <cylinder length="0.6" radius="0.25"/>
                </geometry>
            </collision>
            <inertial>
                <mass value="0.25"/>
                <inertia ixx="0.0003" iyy="0.0003 izz="0.003" ixy="0" ixz="0" iyz="0"/>
            <inertia>
        </link>
        :param adom: xml minidom document
        :return: the link tag of xml minidom element
        """
        # <link>
        link_tag: xmlElement = adom.createElement('link')
        link_tag.setAttribute('name', self.name)

        # <visual>
        cyl_tag: xmlElement = adom.createElement('cylinder')
        cyl_tag.setAttribute('length', str(self.link_length))
        cyl_tag.setAttribute('radius', str(self.link_radius))
        geom_tag: xmlElement = adom.createElement('geometry')
        geom_tag.appendChild(cyl_tag)
        vis_tag: xmlElement = adom.createElement('visual')
        vis_tag.appendChild(geom_tag)

        # <collision>
        coll_tag: xmlElement = adom.createElement('collision')
        coll_geom_tag: xmlElement = adom.createElement('geometry')
        coll_cyl_tag: xmlElement = adom.createElement('cylinder')
        coll_cyl_tag.setAttribute('length', str(self.link_length))
        coll_cyl_tag.setAttribute('radius', str(self.link_radius))
        coll_geom_tag.appendChild(coll_cyl_tag)
        coll_tag.appendChild(coll_geom_tag)

        # <inertial>
        inertial_tag = adom.createElement('inertial')
        mass_tag = adom.createElement('mass')
        mass = np.pi * (self.link_radius * self.link_radius) * self.link_length
        mass_tag.setAttribute("value", str(mass))
        inertia_tag = adom.createElement("inertia")
        inertia_tag.setAttribute("ixx", "0.03")
        inertia_tag.setAttribute("iyy", "0.03")
        inertia_tag.setAttribute("izz", "0.03")
        inertia_tag.setAttribute("ixy", "0")
        inertia_tag.setAttribute("ixz", "0")
        inertia_tag.setAttribute("iyx", "0")
        inertial_tag.appendChild(mass_tag)
        inertial_tag.appendChild(inertia_tag)

        link_tag.appendChild(vis_tag)
        link_tag.appendChild(coll_tag)
        link_tag.appendChild(inertial_tag)

        return link_tag

    def to_joint_element(self, adom: xmlDocument) -> xmlElement:
        """
        <joint name="base_to_sub2" type="revolute">
            <parent link="base_link"/>
            <child link="sub_link2"/>
            <axis xyz="1 0 0"/>
            <limit effort="10" upper"0" lower="10" velocity="1"/>
            <origin rpy="0 0 0" xyz="0 0.5 0"/>
        </joint>
        :param adom: xml minidom document object
        :return: xml minidom element of joint tag
        """
        # <joint>
        joint_tag: xmlElement = adom.createElement('joint')
        joint_tag.setAttribute('name', self.name + '_to_' + self.parent_name)
        joint_tag.setAttribute('type', 'revolute')
        # <parent>
        parent_tag: xmlElement = adom.createElement('parent')
        parent_tag.setAttribute('link', self.parent_name)
        # <child>
        child_tag: xmlElement = adom.createElement('child')
        child_tag.setAttribute('link', self.name)
        # <axis>
        axis_tag: xmlElement = adom.createElement('axis')
        if self.joint_axis_xyz <= .33:
            axis_tag.setAttribute('xyz', '1 0 0')
        elif .33 < self.joint_axis_xyz <= .66:
            axis_tag.setAttribute('xyz', '0 1 0')
        else:
            axis_tag.setAttribute('xyz', '0 0 1')
        # <limit>
        limit_tag: xmlElement = adom.createElement('limit')
        limit_tag.setAttribute('effort', '1')
        limit_tag.setAttribute('lower', '-3.1415')
        limit_tag.setAttribute('upper', '3.1415')
        limit_tag.setAttribute('velocity', '1')
        # <origin>
        orig_tag: xmlElement = adom.createElement('origin')
        rpy = str(self.joint_origin_rpy_1 * self.sibling_index) + ' ' + str(self.joint_origin_rpy_2) + ' ' + \
            str(self.joint_origin_rpy_3)
        xyz = str(self.joint_origin_xyz_1) + ' ' + str(self.joint_origin_xyz_2) + ' ' + str(self.joint_origin_xyz_3)
        orig_tag.setAttribute('rpy', rpy)
        orig_tag.setAttribute('xyz', xyz)

        joint_tag.appendChild(parent_tag)
        joint_tag.appendChild(child_tag)
        joint_tag.appendChild(axis_tag)
        joint_tag.appendChild(limit_tag)
        joint_tag.appendChild(orig_tag)

        return joint_tag

    def __repr__(self):
        repr_str = f'name: {self.name}\n\
                    parent_name: {self.parent_name}\n\
                    recur: {self.recur}\n\
                    '
        return repr_str
