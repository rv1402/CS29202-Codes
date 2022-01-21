#include "./pugixml.hpp"
#include <iostream>
#include <algorithm>
#include <vector>
#include <cmath>
#include <map>
#include <limits>
#include <queue>

using namespace std;

struct Node {
    string id;
    string name="";
    int sl_no;
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
    string id;
    int sl_no;
    vector<Node> nodes;
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

void parse(map<string, Node> &nodes, vector<Way> &ways, map<int, string> &mapping) {
    pugi::xml_document doc;
    pugi::xml_parse_result result = doc.load_file("map.osm");

    //implement error handling here

    int count=0;
    for(pugi::xml_node node: doc.child("osm").children("node")) {
        Node obj;
        obj.id = node.attribute("id").as_string();
        obj.sl_no = count++; //serial numbering starts from 0
        obj.lat = stod(node.attribute("lat").as_string());
        obj.lon = stod(node.attribute("lon").as_string());
        for(pugi::xml_node tag: node.children("tag")) {
            if(string(tag.first_attribute().value()).compare("name") == 0) {
                obj.name = string(tag.last_attribute().value());
                break;
            }
        }
        nodes[obj.id] = obj;
        mapping[obj.sl_no] = obj.id;
    }

    count=0;
    for(pugi::xml_node way: doc.child("osm").children("way")) {
        Way obj;
        obj.id = way.attribute("id").as_string();
        obj.sl_no = count++; //serial numbering starts from 0
        for(pugi::xml_node nd: way.children("nd")) {
            string ID = nd.attribute("ref").as_string();
            Node node = nodes.find(ID)->second;
            obj.nodes.push_back(node);
        }
        ways.push_back(obj);
    }

    doc.reset();
    return;
}

void count(map<string, Node> &nodes, vector<Way> &ways, int &num_nodes, int &num_ways) {
    num_nodes = nodes.size();
    num_ways = ways.size();
    return;
}

Node search(map<string, Node> &nodes, int choice) {
    Node empty_node;
    empty_node.id = "";
    empty_node.name = "";
    empty_node.lat = 0.0;
    empty_node.lon = 0.0;

    string input;
    if(choice == 1) {
        cout << "Enter ID." << endl;
        cin >> input;
        auto obj = nodes.find(input);
        if(obj == nodes.end()){
            return empty_node;
        }
        else{
            return obj->second;
        }
    }
    else {
        cout << "Enter name." << endl;
        cin.ignore();
        getline(cin, input);
        for (const auto& obj: nodes) {
            if (obj.second.name.find(input) != string::npos) {
                //found
                return obj.second;
            }
        }
        return empty_node;
    }
    
}

void k_nearest_nodes(Node &node, map<string, Node> &nodes, int &k) {
    vector<pair<double, Node> > distances;

    if(node.id == "" && node.name == "" && node.lat == 0.0 && node.lon == 0.0){
        cout << "Node with given ID does not exist." << endl;
        return;
    }
    for(auto& obj: nodes) {
        if(node == obj.second) {
            continue;
        }

        distances.push_back(make_pair(haversine(node, obj.second), obj.second));
    }

    sort(distances.begin(), distances.end());

    cout << k << " nearest nodes are :" << endl;
    for(int i=0; i<k; i++) {
        cout << "Node: " << distances[i].second.id << " at a distance: " << distances[i].first << "km." << endl;
    }
}

void addEdge(vector<pair<int, double> > Graph[], Node &u, Node &v){
    double weight = haversine(u, v);
    Graph[u.sl_no].push_back(make_pair(v.sl_no, weight));
    Graph[v.sl_no].push_back(make_pair(u.sl_no, weight));
}

void create_graph(vector<Way> &ways, vector<pair<int, double> > Graph[]){
    for(Way way: ways){
        for(short i=1; i<way.nodes.size(); i++){
            Node u = way.nodes[i-1];
            Node v = way.nodes[i];
            addEdge(Graph, u, v);
        }
    }
}

void print_path(vector<int> &parent, map<int, string> &mapping, int v){
    if (parent[v] == -1) {
        cout << mapping.find(v)->second << endl;
        return ;
    }
    print_path(parent, mapping, parent[v]);
    cout << mapping.find(v)->second << endl;
}

void dijkstra(vector<pair<int, double> > Graph[], int &src, int &dest, int &num_nodes, map<int, string> &mapping){
    int V = num_nodes;

    //min heap
    priority_queue<pair<double, int>, vector<pair<double, int> >, greater<pair<double, int> > > pq;
 
    vector<double> dist(V, numeric_limits<double>::max());
 
    // create a parent to store path info
    vector<int> parent(V);
    parent[src] = -1;
 
    //pair stored in a form of <weight(distance), source>
    pq.push(make_pair(0, src));
    dist[src] = 0.0;

    // looping till priority queue becomes empty
    while(pq.size()){
        //extract minimum element
        int u = pq.top().second;
        pq.pop();
 
        // iterate through all vertices adjacent to 'u'
        for(pair<int, double> p: Graph[u]) {
			int v = p.first;
			double p_weight = p.second;
 
            // if there is a shorter path to v through u
            if (dist[v] > dist[u] + p_weight) {
                dist[v] = dist[u] + p_weight;
                pq.push(make_pair(dist[v], v));
                parent[v] = u;
            }
        }
    }

	//print result
    if(dist[dest] != numeric_limits<double>::max()){
        cout << "Total distance of destination node from source node is: " << dist[dest] << " km" << endl;
        cout << "The path from source to destination is: " << endl;
        print_path(parent, mapping, dest);
    }
    else{
        cout << "These two nodes are not connected." << endl;
    }
    return;
}

int main() {
    Node empty_node;
    empty_node.id = "";
    empty_node.name = "";
    empty_node.lat = 0.0;
    empty_node.lon = 0.0;

    map<string, Node> nodes;
    vector<Way> ways;
    map<int, string> mapping;

    int num_nodes;
    int num_ways;

    parse(nodes, ways, mapping);
    count(nodes, ways, num_nodes, num_ways);
    cout << "Number of nodes: " << num_nodes << ", number of ways: " << num_ways << endl;

    int choice=1;
    while(choice == 1) {
        int flag;
        cout << "Do you want to search the node by ID(Enter 1) or by name(Enter 0)?" << endl;
        cin >> flag;
        Node node = search(nodes, flag);
        if(node == empty_node) {
            cout << "Node not found." << endl;
        }
        else if(node.name.empty()) {
            cout << "Node found! ID: " << node.id << ", Latitude: " << node.lat << " and Longitude: " << node.lon << endl;
        }
        else {
            cout << "Node found! Name: " << node.name << ", with ID: " << node.id << ", Latitude: " << node.lat << " and Longitude: " << node.lon << endl;
        }
        cout << "Do you want to continue searching elements?(Enter 1 if yes, 0 if no)" << endl;
        cin >> choice;
    }

    int k;
    cout << "The program will now find the nearest nodes to the node ID you give as input." << endl;
    Node node = search(nodes, 1);
    cout << "Enter the value of k." << endl;
    cin >> k;
    k_nearest_nodes(node, nodes, k);

    cout << endl;
    
    vector<pair<int, double> > Graph[num_nodes];
    create_graph(ways, Graph);

    // string source_ID, dest_ID;
    // cout << "Enter ID for the source and destination nodes." << endl;
    // cin >> source_ID >> dest_ID;
    // int source = (nodes.find(source_ID)->second).sl_no;
    // int destination = (nodes.find(dest_ID)->second).sl_no;

    int source, destination;
    cout << "Enter serial number of source and destination (Both should lie between 0 and " << num_nodes << ")." << endl;
    cin >> source >> destination;

    dijkstra(Graph, source, destination, num_nodes, mapping);

    exit(0);
}