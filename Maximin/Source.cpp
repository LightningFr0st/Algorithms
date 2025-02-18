#include <iostream>
#include <vector>
#include <algorithm>
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

int n, k = 1;

vector<node> nodes;
vector<position> cores;

double dist(position pos1, position pos2) {
	return sqrt(sqr(pos1.first - pos2.first) + sqr(pos1.second - pos2.second));
}


bool ending = false;
bool ending2 = false;
int it = 1;

void update() {

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < k; j++) {
			double cur = dist(nodes[i].pos, cores[j]);
			if (nodes[i].distance > cur) {
				nodes[i].distance = cur;
				nodes[i].core = j;
			}
		}
	}
	double maxi = nodes[0].distance;
	int nmx = 0;
	for (int i = 1; i < n; i++) {
		if (maxi < nodes[i].distance) {
			maxi = nodes[i].distance;
			nmx = i;
		}
	}
	//cout << nodes[nmx].pos.first << ' ' << nodes[nmx].pos.second << '\n';
	//cout << cores[nodes[nmx].core].first << ' ' << cores[nodes[nmx].core].second << "\n\n";
	double avaga = 0;
	int count = 0;
	for (int i = 0; i < k; i++) {
		for (int j = i + 1; j < k; j++) {
			avaga += dist(cores[i], cores[j]);
			count++;
		}
	}
	avaga /= count;
	avaga /= 2;
	if (maxi > avaga) {
		cores.push_back(nodes[nmx].pos);
		k++;
		it++;
	}
	else {
		ending = true;
	}
}

sf::Font font;

void draw() {
	window.clear(sf::Color::Black);
	for (int i = 0; i < n; i++) {
		sf::CircleShape circle;
		circle.setRadius(1);
		circle.setFillColor(sf::Color::Color(50 + 20 * nodes[i].core, 100 + 20 * nodes[i].core, 150 + 20 * nodes[i].core));
		circle.setPosition(nodes[i].pos.first + 50, nodes[i].pos.second + 50);
		window.draw(circle);
	}
	for (int i = 0; i < k; i++) {
		sf::CircleShape circle;
		circle.setRadius(4);
		circle.setFillColor(sf::Color::Red);
		circle.setPosition(cores[i].first + 50, cores[i].second + 50);
		window.draw(circle);
	}

	sf::Text text(to_string(it), font, 50);
	window.draw(text);
	window.display();
}

void update2() {
	bool ischanged = true;
	while (ischanged) {
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
}

int main() {
	srand(time(NULL));
	if (!font.loadFromFile("./bit.ttf")) {
		cout << "ERROR\n";
	}
	cout << "Nodes: "; cin >> n;
	nodes.resize(n);
	for (int i = 0; i < n; i++) {
		nodes[i].pos.first = rand() % 1001;
		nodes[i].pos.second = rand() % 1001;
	}
	cores.push_back(nodes[rand() % n].pos);
	int sec = 0;
	{
		double res = 0;
		for (int i = 1; i < n; i++) {
			double temp = dist(cores[0], nodes[i].pos);
			if (res < temp) {
				res = temp;
				sec = i;
			}
		}
	}

	cores.push_back(nodes[sec].pos);
	k++;

	window.create(sf::VideoMode(1100, 1100), "Clustering", sf::Style::None);
	window.setFramerateLimit(60);
	draw();
	while (window.isOpen()) {
		sf::Event event;
		while (window.pollEvent(event)) {
			if (ending2 && (event.type == sf::Event::MouseButtonPressed) && (event.mouseButton.button == sf::Mouse::Left)) {
				window.close();
			}
			else if (!ending && (event.type == sf::Event::MouseButtonPressed) && (event.mouseButton.button == sf::Mouse::Left)) {
				update();
				draw();
			}
			else if (ending && (event.type == sf::Event::MouseButtonPressed) && (event.mouseButton.button == sf::Mouse::Left)) {
				it++;
				update2();
				draw();
				ending2 = true;
			}
		}
	}


}

/*
100000
*/
