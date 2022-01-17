#include <iostream>
#include <vector>
#include "./pugixml.hpp"

using namespace std;

struct Node {
    std::string id;
    std::string uid;
    std::string name="";
    std::string x;
    std::string y;
};

struct Way {
    std::string id;
    std::string uid;
    std::vector<std::string> node_IDs;
};

void parse(std::vector<Node> &nodes, std::vector<Way> &ways) {
    pugi::xml_document doc;
    pugi::xml_parse_result result = doc.load_file("map.osm");

    //implement error handling here

    for(pugi::xml_node node: doc.child("osm").children("node")) {
        Node obj;
        obj.id = node.attribute("id").as_string();
        obj.uid = node.attribute("uid").as_string();
        obj.y = node.attribute("lat").as_string();
        obj.x = node.attribute("lon").as_string();
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
        obj.uid = way.attribute("uid").as_string();
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

void search(std::vector<Node> &nodes, std::vector<Way> &ways) {
    std::string input;
    int choice;
    std::cout << "Do you want to search the node by ID(Enter 1) or by name(Enter 0)?" << std::endl;
    std::cin >> choice;
    if(choice == 1) {
        std::cout << "Enter ID." << std::endl;
        std::cin >> input;
        for(Node node: nodes) {
            if(node.id.compare(input) == 0) {
                if(node.name.empty()) {
                    std::cout << "Node found! ID: " << node.id << ", UID: " << node.uid << ", Latitude: " << node.y << "and Longitude: " << node.x << std::endl;
                }
                else {
                    std::cout << "Node found! Name: " << node.name << ", with ID: " << node.id << ", UID: " << node.uid << ", Latitude: " << node.y << " and Longitude: " << node.x << std::endl;
                }
                return;
            }
        }
        std::cout << "Node not found." << std::endl;
    }
    else {
        std::cout << "Enter name." << std::endl;
        std::getline(std::cin, input);
        bool found = false;
        for(Node node: nodes) {
            if (node.name.find(input) != std::string::npos) {
                //found
                std::cout << "Node found! Name: " << node.name << ", with ID: " << node.id << ", UID: " << node.uid << ", Latitude: " << node.y << " and Longitude: " << node.x << std::endl;
                found = true;
                return;
            }
        }
        std::cout << "Node not found." << std::endl;
    }
}

void distance(Node &n1, Node &n2) {

}

void k_nearest_nodes() {

}

int main() {
    std::vector<Node> nodes;
    std::vector<Way> ways;

    parse(nodes, ways);
    count(nodes, ways);

    int choice=1;
    while(choice == 1) {
        search(nodes, ways);
        std::cout << "Do you want to continue searching elements?(Enter 1 if yes, 0 if no)" << std::endl;
        std::cin >> choice;
    }

    exit(0);
}