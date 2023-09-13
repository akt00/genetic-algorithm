from typing import Optional
from xml.dom.minidom import getDOMImplementation
import numpy as np

from ga import genome
from ga.genome import URDFLink
import motor
from type import Point


class Creature:
    def __init__(self, gene_count: int = 3):
        self.spec = genome.get_gene_spec(gene_spec=None)
        self.dna = genome.get_random_genome(gene_count=gene_count, gene_length=len(self.spec))
        self.flat_links: Optional[list[URDFLink]] = None
        self.exp_links: Optional[list[URDFLink]] = None
        self.motors: Optional[list[motor.Motor]] = None
        self.start_position: Optional[Point] = None
        self.last_position: Optional[Point] = None

    def get_flat_links(self) -> list[URDFLink]:
        """
        :return:
        """
        if self.flat_links is None:
            g_dicts = genome.get_genome_dicts(self.dna, self.spec)
            self.flat_links = genome.genome_to_links(g_dicts)
        return self.flat_links

    def get_expanded_links(self) -> list[URDFLink]:
        """
        :return:
        """
        self.get_flat_links()
        if self.exp_links is None:
            exp_links = [self.flat_links[0]]
            genome.expand_link(self.flat_links[0], self.flat_links[0].name, self.flat_links, exp_links)
            self.exp_links = exp_links
        return self.exp_links

    def to_xml(self) -> str:
        """
        :return:
        """
        self.get_expanded_links()
        dom = getDOMImplementation()
        adom = dom.createDocument(None, 'start', None)
        root_tag = adom.createElement('robot')
        for link in self.exp_links:
            root_tag.appendChild(link.to_link_element(adom))
        iterator = iter(self.exp_links)
        next(iterator)
        while link := next(iterator):
            root_tag.appendChild(link.to_joint_element(adom))
        root_tag.setAttribute('name', 'Creature')
        return '<?xml version="1.0"?>' + root_tag.toprettyxml()

    def get_motors(self) -> list[motor.Motor]:
        """
        :return:
        """
        self.get_expanded_links()
        if self.motors is None:
            motors = []
            for i in range(1, len(self.exp_links)):
                link = self.exp_links[i]
                mtr = motor.Motor(link.control_waveform, link.control_amp, link.control_freq)
                motors.append(mtr)
            self.motors = motors
        return self.motors

    def update_position(self, pos: Point):
        """
        :param pos:
        :return:
        """
        if self.start_position is None:
            self.start_position = pos
        else:
            self.last_position = pos

    def get_distance_travelled(self) -> float:
        """
        :return:
        """
        dist = 0
        if self.start_position and self.last_position:
            p1 = np.asarray(self.start_position)
            p2 = np.asarray(self.last_position)
            dist = np.linalg.norm(p1 - p2)
        return dist

    def update_dna(self, dna) -> None:
        """
        :param dna:
        :return:
        """
        self.dna = dna
        self.flat_links = None
        self.exp_links = None
        self.motors = None
        self.start_position = None
        self.last_position = None
