import os
import pytest
from xml.dom.minidom import getDOMImplementation
import numpy as np

from ga import genome


@pytest.fixture(scope='module')
def setup_gene_seed():
    # print('setting up GeneSeeds...')
    return genome.get_random_gene()


@pytest.fixture(scope='module')
def setup_dna():
    # print('setting up dna...')
    return genome.get_random_genome()


@pytest.fixture
def cleanup():
    yield
    path = './genome_temp.csv'
    if os.path.exists(path):
        os.remove(path)


def test_get_random_gene(setup_gene_seed):
    gs = setup_gene_seed
    assert isinstance(gs, np.ndarray)
    assert gs.shape == (17,)


def test_get_random_genome(setup_dna):
    ret = setup_dna
    assert isinstance(ret, list)
    assert len(ret) == 3
    assert isinstance(ret[0], np.ndarray)
    assert ret[0].shape == (17,)


def test_gene_spec_default():
    gene_spec = genome.get_gene_spec()
    assert gene_spec is not None
    default = genome.DEFAULT_GENE_SPEC
    for idx, (k1, k2) in enumerate(zip(default, gene_spec)):
        assert default[k1]['scale'] == gene_spec[k2]['scale']
        assert gene_spec[k2]['index'] == idx


def test_get_gene_dict(setup_gene_seed):
    seeds = setup_gene_seed
    spec = genome.get_gene_spec()
    gdict = genome.get_gene_dict(seeds, spec)
    # print(gdict)
    for key in spec.keys():
        assert isinstance(gdict[key], float)


def test_get_genome_dicts(setup_dna):
    seed = setup_dna
    spec = genome.get_gene_spec()
    gl = genome.get_genome_dicts(seed, spec)
    assert len(gl) == len(seed)


def test_expand_links():
    links = [
        genome.URDFLink(name="A", parent_name="None", recur=1),
        genome.URDFLink(name="B", parent_name="A", recur=1),
        genome.URDFLink(name="C", parent_name="B", recur=2),
        genome.URDFLink(name="D", parent_name="C", recur=1),
    ]
    exp_links = [root := links[0]]
    genome.expand_link(root, root.name, links, exp_links)
    print()
    for link in exp_links:
        print(f'{link.parent_name} -> {link.name}')
    assert len(exp_links) == 6


def test_genome_to_links(setup_dna):
    dna = setup_dna
    spec = genome.get_gene_spec()
    gl = genome.get_genome_dicts(dna, spec)
    links = genome.genome_to_links(gl)
    # print(repr(links[0]), len(links))
    assert isinstance(links, list)
    assert len(links) == 3
    assert isinstance(links[0], genome.URDFLink)


def test_crossover(setup_dna):
    for _ in range(1000):
        g1 = setup_dna
        g2 = genome.get_random_genome(gene_count=4)
        g3 = genome.crossover(g1, g2)
        assert isinstance(g3, list)
        assert len(g3) == 4
        assert isinstance(g3[0], np.ndarray)
        assert g3[0].shape == (17,)


def test_point_mutate_max_mutate(setup_dna):
    dna = setup_dna
    new_genome = genome.point_mutate(dna, rate=1, amount=1)
    for gene in new_genome:
        for i in gene:
            assert i == 0 or round(i, 2) == round(0.999, 2)


def test_point_mutate_no_mutation(setup_dna):
    dna = setup_dna
    new_dna = genome.point_mutate(dna, rate=0, amount=0.1)
    assert len(dna) == len(new_dna)
    for g1, g2 in zip(dna, new_dna):
        assert np.array_equal(g1, g2)


def test_shrink_mutate_shrink(setup_dna):
    dna = setup_dna
    new_dna = genome.shrink_mutate(dna, rate=1)
    assert len(dna) == len(new_dna) + 1


def test_shrink_mutate_no_shrink(setup_dna):
    dna = setup_dna
    new_dna = genome.shrink_mutate(dna, rate=0)
    assert len(dna) == len(new_dna)


def test_shrink_mutate_smallest_dna(setup_dna):
    dna = genome.get_random_genome(gene_count=1)
    new_dna = genome.shrink_mutate(dna, rate=1)
    assert len(dna) == len(new_dna)


def test_grow_mutate_grow(setup_dna):
    dna = setup_dna
    new_dna = genome.grow_mutate(dna, rate=1)
    assert len(dna) == len(new_dna) - 1


def test_grow_mutate_no_grow(setup_dna):
    dna = setup_dna
    new_dna = genome.grow_mutate(dna, rate=0)
    assert len(dna) == len(new_dna)


def test_to_csv(setup_dna):
    dna = setup_dna
    genome.to_csv(dna, './genome_temp.csv')
    assert True


def test_from_csv(setup_dna, cleanup):
    original = setup_dna
    dna = genome.from_csv('./genome_temp.csv')
    assert len(original) == len(dna)
    for g1, g2 in zip(original, dna):
        assert np.array_equal(g1, g2)


def test_urdf(setup_dna):
    dna = setup_dna
    spec = genome.get_gene_spec()
    gl = genome.get_genome_dicts(dna, spec)
    links = genome.genome_to_links(gl)

    dom = getDOMImplementation()
    adom = dom.createDocument(None, 'start', None)
    f1 = links[0]
    print()
    print(f1.to_link_element(adom).toprettyxml())
    print(f1.to_joint_element(adom).toprettyxml())
    assert True
