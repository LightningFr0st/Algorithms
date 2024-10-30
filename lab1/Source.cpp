#include <iostream>
#include <vector>
#include <SFML/Graphics.hpp>
#include <SFML/Graphics/CircleShape.hpp>

#define sqr(x) (x) * (x)
using namespace std;

typedef pair<int, int> position;
sf::RenderWindow window;


struct node {
	position pos;
	double distance = 100000;
	int core = -1;
};

int n = 100000, k = 6;
vector<node> nodes;
vector<position> cores;

double dist(position pos1, position pos2) {
	return sqrt(sqr(pos1.first - pos2.first) + sqr(pos1.second - pos2.second));
}

void draw() {
	window.clear(sf::Color::Black);
	for (int i = 0; i < n; i++) {
		sf::CircleShape circle;
		circle.setRadius(1);
		circle.setFillColor(sf::Color::Color(50 + 20 * nodes[i].core, 100 + 20 * nodes[i].core, 150 + 20 * nodes[i].core));
		circle.setPosition(nodes[i].pos.first, nodes[i].pos.second);
		window.draw(circle);
	}
	for (int i = 0; i < k; i++) {
		sf::CircleShape circle;
		circle.setRadius(4);
		circle.setFillColor(sf::Color::Red);
		circle.setPosition(cores[i].first, cores[i].second);
		window.draw(circle);
	}
	window.display();
}

bool ischanged = true;
bool start = false;

void update() {
	vector<pair<position, int>> avg(k);

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < k; j++) {
			double cur = dist(nodes[i].pos, cores[j]);
			if (nodes[i].distance > cur) {
				nodes[i].distance = cur;
				nodes[i].core = j;
			}
		}
	}
	for (int i = 0; i < n; i++) {
		avg[nodes[i].core].first.first += nodes[i].pos.first;
		avg[nodes[i].core].first.second += nodes[i].pos.second;
		avg[nodes[i].core].second++;
	}
	ischanged = false;
	for (int i = 0; i < k; i++) {
		position temp = { avg[i].first.first / avg[i].second,  avg[i].first.second / avg[i].second };
		if (temp != cores[i]) {
			cores[i] = temp;
			ischanged = true;
		}
	}
}

int main() {
	srand(time(NULL));
	cout << "Clusters: "; cin >> k;
	cout << "Nodes: "; cin >> n;
	nodes.resize(n);
	cores.resize(k);
	for (int i = 0; i < n; i++) {
		nodes[i].pos.first = rand() % 1001;
		nodes[i].pos.second = rand() % 1001;
	}
	for (int i = 0; i < k; i++) {
		cores[i].first = rand() % 1001;
		cores[i].second = rand() % 1001;
	}

	window.create(sf::VideoMode(1000, 1000), "Clustering", sf::Style::None);
	window.setFramerateLimit(60);
	draw();
	while (window.isOpen()) {
		sf::Event event;
		while (window.pollEvent(event)) {
			if ((event.type == sf::Event::KeyPressed) && (event.key.code == sf::Keyboard::Escape)) {
				window.close();
			}
			else if ((event.type == sf::Event::MouseButtonPressed) && (event.mouseButton.button == sf::Mouse::Left)) {
				start = true;
			}
		}
		if (ischanged && start) {
			update();
			draw();
		}
		sf::sleep(sf::milliseconds(500));
	}
}

/*
6
100000
*/