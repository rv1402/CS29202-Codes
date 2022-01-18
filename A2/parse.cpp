#include <iostream>
#include <algorithm>
#include <vector>
#include "./pugixml.hpp"
#include <cmath>

using namespace std;

struct Node {
    std::string id;
    // std::string uid;
    std::string name="";
    double lon;
    double lat;

    bool operator==(const Node &node) {
        return((id.compare(node.id) == 0) && (name.compare(node.name) == 0) && (lon == node.lon) && (lat == node.lat));
    }
    bool operator<(const Node &node) const{
        return false;
    }
};

struct Way {
    std::string id;
    // std::string uid;
    std::vector<std::string> node_IDs;
};

//returns distance in kilometre
double haversine(Node &n1, Node &n2) {
    double dist_Lat = (n2.lat - n1.lat) * M_PI / 180.0;
    double dist_Lon = (n2.lon - n1.lon) * M_PI / 180.0;
    double rad_Lat1 = n1.lat * M_PI / 180.0;
    double rad_Lat2 = n2.lat * M_PI / 180.0;

    double a = pow(sin(dist_Lat / 2), 2) + pow(sin(dist_Lon / 2), 2) * cos(rad_Lat1) * cos(rad_Lat2);
    double rad = 6371;
    double c = 2 * asin(sqrt(a));
    return rad * c;
}

void parse(std::vector<Node> &nodes, std::vector<Way> &ways) {
    pugi::xml_document doc;
    pugi::xml_parse_result result = doc.load_file("map.osm");

    //implement error handling here

    for(pugi::xml_node node: doc.child("osm").children("node")) {
        Node obj;
        obj.id = node.attribute("id").as_string();
        // obj.uid = node.attribute("uid").as_string();
        obj.lat = std::stod(node.attribute("lat").as_string());
        obj.lon = std::stod(node.attribute("lon").as_string());
        for(pugi::xml_node tag: node.children("tag")) {
            if(string(tag.first_attribute().value()).compare("name") == 0) {
                obj.name = string(tag.last_attribute().value());
                break;
            }
        }
        nodes.push_back(obj);
    }

    for(pugi::xml_node way: doc.child("osm").children("way")) {
        Way obj;
        obj.id = way.attribute("id").as_string();
        // obj.uid = way.attribute("uid").as_string();
        for(pugi::xml_node nd: way.children("nd")) {
            obj.node_IDs.push_back(string(nd.attribute("ref").value()));
        }
        ways.push_back(obj);
    }

    doc.reset();
    return;
}

void count(std::vector<Node> &nodes, std::vector<Way> &ways) {
    int node_count = nodes.size();
    int way_count = ways.size();
    std::cout << "Number of nodes: " << node_count << ", number of ways: " << way_count << std::endl;
    return;
}

Node search(std::vector<Node> &nodes, int choice) {
    Node empty_node;
    empty_node.id = "";
    empty_node.name = "";
    empty_node.lat = 0.0;
    empty_node.lon = 0.0;

    std::string input;
    if(choice == 1) {
        std::cout << "Enter ID." << std::endl;
        std::cin >> input;
        for(Node node: nodes) {
            if(node.id.compare(input) == 0) {
                return node;
            }
        }
        return empty_node;
    }
    else {
        std::cout << "Enter name." << std::endl;
        std::cin.ignore();
        std::getline(std::cin, input);
        for(Node node: nodes) {
            if (node.name.find(input) != std::string::npos) {
                //found
                return node;
            }
        }
        return empty_node;
    }
    
}

void k_nearest_nodes(Node &node, std::vector<Node> &nodes, int &k) {
    std::vector<std::pair<double, Node>> distances;

    for(Node n: nodes) {
        if(n == node) {
            continue;
        }

        distances.push_back(std::make_pair(haversine(node, n), n));
    }

    std::sort(distances.begin(), distances.end());

    std::cout << k << " nearest nodes are :" << std::endl;
    for(int i=0; i<k; i++) {
        std::cout << "Node: " << distances[i].second.id << " at a distance: " << distances[i].first << "km." << std::endl;
    }
}

int main() {
    Node empty_node;
    empty_node.id = "";
    empty_node.name = "";
    empty_node.lat = 0.0;
    empty_node.lon = 0.0;

    std::vector<Node> nodes;
    std::vector<Way> ways;

    parse(nodes, ways);
    count(nodes, ways);

    int choice=1;
    while(choice == 1) {
        int flag;
        std::cout << "Do you want to search the node by ID(Enter 1) or by name(Enter 0)?" << std::endl;
        std::cin >> flag;
        Node node = search(nodes, flag);
        if(node == empty_node) {
            std::cout << "Node not found." << std::endl;
        }
        else if(node.name.empty()) {
            std::cout << "Node found! ID: " << node.id << ", Latitude: " << node.lat << "and Longitude: " << node.lon << std::endl;
        }
        else {
            std::cout << "Node found! Name: " << node.name << ", with ID: " << node.id << ", Latitude: " << node.lat << " and Longitude: " << node.lon << std::endl;
        }
        std::cout << "Do you want to continue searching elements?(Enter 1 if yes, 0 if no)" << std::endl;
        std::cin >> choice;
    }

    int id, k;
    std::cout << "The program will now find the nearest nodes to the node ID you give as input." << std::endl;
    Node node = search(nodes, 1);
    std::cout << "Enter the value of k." << std::endl;
    std::cin >> k;
    k_nearest_nodes(node, nodes, k);

    exit(0);
}