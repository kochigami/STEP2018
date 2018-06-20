#include <iostream>
#include <fstream>
#include <vector>
#include <list>
#include <string>
#include <boost/graph/vector_as_graph.hpp>
#include <boost/graph/graph_utility.hpp>

static const std::string LINKS_FILE_PATH ="./wikipedia/links.txt";
static const std::string PAGES_FILE_PATH="./wikipedia/pages.txt";

// TODO: 関数化

// TODO: BFS
// dequeue
// enqueue

int main()
{
  std::ifstream ifs("./wikipedia/links.txt");
  std::ifstream ifs2("./wikipedia/pages.txt");
  
  std::vector< std::vector<int> > g(1483277);
  if (ifs.fail())
    {
      std::cerr << "could not read file" << std::endl;
      return -1;
    }
  static int index = 0;
  int left = -1, right = -1;
  while (true){
    if (ifs.eof())
      break;
    ifs >> left >> right;
    if (left == -1 || right == -1) {
      std::cerr << "unexpected error: " << index << std::endl;
      return -1;
    }
    if (left == index){
      g[index].push_back(right);
      //std::cout << right << std::endl;
    }
    else{
      index += 1;
      g[index].push_back(right);
      //std::cout << "\n" << std::endl;
      //std::cout << right << std::endl;	    
    }

    // TODO: idごとに読み込めていることを確認したい
    // 以下うまくいかない
    
    // bool is_first = true;
    // for (auto& v1 : g) {
    //   std::cout << "{";
    //   for(auto& v2 : v1) {
    // 	std::cout << (is_first ? "" : ", ") << v2;
    // 	is_first = false;
    //   }
    //   std::cout << "}" << std::endl;
    // }
    // std::cout << std::endl;

    //boost::print_graph(g, name.data());
  }
    
  std::vector< std::string > p(1483277);
  if (ifs2.fail())
    {
      std::cerr << "could not read file" << std::endl;
      return -1;
    }

  int id;
  std::string name;
  while (true){
    if (ifs2.eof())
      break;
    ifs2 >> id >> name;
    //std::cout << name << std::endl;
    p.push_back(name);
  }


  // TODO: 読み込めていることを確認したい
  // 以下うまくいかない
  // for (auto& v1 : p) {
  //   std::cout << v1 << " ";
  // }
  // std::cout << std::endl;

  // input word
  std::string from, to;
  std::cout << "from?: " << std::endl;
  std::cin >> from;
  std::cout << "to?: " << std::endl;
  std::cin >> to;
  
  std::cout << "from: " << from << " to: " << to  << std::endl;

  return 0;
}
