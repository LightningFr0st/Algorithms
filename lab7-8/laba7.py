import nltk
import matplotlib.pyplot as plt

grammar = nltk.CFG.fromstring("""
    S -> NP VP
    NP -> Det N | Det N PP | Det N VP
    VP -> V NP | VP PP
    PP -> P NP
    Det -> 'a' | 'an' | 'the'
    N -> 'nebula' | 'planet' | 'star' | 'telescope'
    V -> 'observe' | 'passing' | 'eclipses'
    P -> 'on' | 'under' | 'in'
""")


parser = nltk.ChartParser(grammar)
sentence = "the telescope observe the planet eclipses the star"

object_images = {
    'nebula': plt.imread('./lab7img/nebula.jpg'),
    'planet': plt.imread('./lab7img/planet.jpg'),
    'star': plt.imread('./lab7img/star.jpg'),
    'telescope': plt.imread('./lab7img/telescope.jpg')
}
flag = True

for tree in parser.parse(sentence.split()):

    tree.pretty_print()
    plt.figure(figsize=(10, 5))
    obj = []
    for subtree in tree.subtrees(lambda t: t.label() == 'N'):
        object_name = subtree.leaves()[0]
        if flag:
            # plt.subplot(1, 2, 1)
            obj.append(object_name)
            # plt.imshow(object_images[object_name])
            # plt.title(object_name)
            # plt.axis('off')
            # plt.show()

    if flag:
        plt.title('Objects')
        plt.axis('off')
        plt.subplot(2, 2, 1)
        plt.axis('off')
        plt.imshow(object_images[obj[0]])

        plt.subplot(2, 2, 2)
        plt.imshow(object_images[obj[1]])
        plt.axis('off')
        plt.subplot(2, 2, 3)
        plt.imshow(object_images[obj[2]])
        plt.axis('off')

        plt.show()
        flag = False