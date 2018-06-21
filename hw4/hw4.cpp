#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <queue>

static const std::string LINKS_FILE_PATH ="./wikipedia/links.txt";
static const std::string PAGES_FILE_PATH="./wikipedia/pages.txt";

int read_links_file(std::vector< std::vector<int> > &g);
int read_pages_file(std::vector< std::string > &p);
std::vector<int> BFS(std::vector< std::vector<int> > &g, int from, int to);

/* 
   link file を読み込むための関数
   std::vector< std::vector<int> > &g の各インデックスにリンクを入れる
*/
int read_links_file(std::vector< std::vector<int> > &g){
  std::ifstream ifs("./wikipedia/links.txt");
  if (ifs.fail())
    {
      std::cerr << "could not read file" << std::endl;
      return -1;
    }
  static int index = 0;
  static int count = 0;

  while(!ifs.eof())
    {
      int word;
      ifs >> word;
      
      // ファイルから，indexとlinkが交互に取り出される
      if (count % 2 == 0){
	// word : index
	if (word != index){
	  index += 1;
	}
      }
      else{
	// word : link
	g[index].push_back(word);
      }
      count += 1;
    } 

  // idごとに読み込めていることを確認したい
  // できた:
  // 30224 {10345, 517061, 406520, 18826, 170103, 851077, 273529, 851107, 95543, 3702, 134374, 11082, 2141, 177927, 10254, 209787, 436365, 174259, 45069, 1313, 127538, 116015, 31645, 700704, 261677, 28052, 9414, 1144051, 229787, 3190, 732790, 449328, 1050474, 78329, 3180, 27822, 24984, 39953, 8, 189207, 6091, 165969, 10852, 18859, 559883, 847580, 449232, 607457, 3415, 11958, 101083, 2125, 41082, 50472, 257074, 7527, 3186, 66136, 306305, 5268, 436394, 1305866, 3875, 1281841, 37156, 37060, 3288, 3352, 1236579, 18837, 16776, 179332, 18470, 221855, 49544, 18835, 67145, 2868, 436383, 436276}
  // 30225 {219595}
  // 30226 {30224}
  // 30227 {219595}
  // 30228 {219595}
  // 30229 {219595}
  // 30230 {219595}
  // 30231 {219595}
  // 30232 {3644}
  // 30233 {1118, 1123, 1029155, 1029156, 1112, 1116, 167027, 331199, 784168, 30235, 158620, 7370, 379503, 1998, 892213, 450734, 241968, 687956, 158933, 34539, 30090, 32498, 154887, 27571, 865580, 12153, 1127, 90654, 1413892, 23827, 8665, 507243, 11302, 531232, 14116, 301807, 34543, 64074, 141099, 656463, 10672}
  // 30234 {30233, 8091, 100093, 7924, 27571}
  // 30235 {331199, 7369, 220356, 30233, 7370, 353021, 1312362, 325049, 16807, 136802, 131852, 9832, 927119, 8138, 82294, 109276, 1786, 8665, 37443, 147541, 730522, 16737, 14116, 34543, 82295, 141099, 656463, 2349, 38378}
  // 30236 {30233}

  // count = 0;  
  // bool is_first = true;
  // for (auto& v1 : g) {
  //   is_first = true; 
  //   std::cout << count << " {";
  //   for(auto& v2 : v1) {
  //     std::cout << (is_first ? "" : ", ") << v2;
  //     is_first = false;
  //   }
  //   count += 1;
  //   std::cout << "}" << std::endl;
  // }

  // std::cout << std::endl;
  
}

/* 
   page file を読み込むための関数
   std::vector< std::string > &p に名前を追加していく
*/
int read_pages_file(std::vector< std::string > &p){
  std::ifstream ifs2("./wikipedia/pages.txt");
  if (ifs2.fail())
    {
      std::cerr << "could not read file" << std::endl;
      return -1;
    }

  // ファイルから，indexとnameが交互に取り出される
  static int count = 0;
  std::string word;
  while(!ifs2.eof())
    {
      ifs2 >> word;
      if (count % 2 == 1){
	// word : name
	p.push_back(word);
      }
      count += 1;
    }
  
  // 読み込めていることを確認
  // for (auto& v1 : p) {
  //   std::cout << v1 << " ";
  // }
  // std::cout << std::endl;

  return 0;
}

/*
  BFSでグラフ構造を使いながら，スタートからゴールまでたどる関数
  std::vector<int> BFS(std::vector< std::vector<int> > &g, int from, int to)
  
  引数：
  std::vector< std::vector<int> > &g: read_links_file 関数で作ったリスト 
  int from: スタートのID 
  int to: ゴールのID
 */
std::vector<int> BFS(std::vector< std::vector<int> > &g, int from, int to){
  std::queue<std::vector<int>> queue;
  // 空のベクタをキューに追加
  queue.push( std::vector<int>() );
  queue.front().push_back(from);
  
  while( !queue.empty() ) {
    // キューの先頭のリストを取得
    const auto& route = queue.front();
    // 末尾の数字を取得
    int cur = route.back();
    // 末尾の数字がゴールに一致していたら探索終了
    if(cur == to) {
      return route;
    }
    /* 
       末尾の数字がゴールに一致していなかったら
       末尾の数字が続く先の数字を順次追加して経路を量産する
       キューの後ろに追加
    */
    else{
      for (const auto& i : g[cur]) {
	auto new_route = route;
	new_route.push_back(i);
	queue.push(new_route);
      }
    }
    // 先頭のリスト（先ほどまで注目していたもの）を削除．キューの後ろに更新したものを追加したため
    queue.pop();
  }
  return std::vector<int>();
}

int main()
{
  
  std::vector< std::vector<int> > g(1483277);
  read_links_file(g);
    
  std::vector< std::string > p(1483277);
  read_pages_file(p);

  // 何も出力されない (*)
  // std::cout << p[0] << std::endl;
  // std::cout << p[0].c_str() << std::endl;

  while(true){
    // input word

    // 本当は文字で入力したかったが，文字での経路表示がうまくいかない(*)ため断念．
    //std::string from, to;

    int from, to;
    std::cout << "from?: " << std::endl;
    std::cin >> from;
    std::cout << "to?: " << std::endl;
    std::cin >> to;
    
    std::cout << "from: " << from << " to: " << to  << std::endl;

    // TODO: convert string to number (*)

    // bfs
    auto path = BFS(g, from, to);
    
    if (path.size() == 0) {
      std::cout << "Path was not found" << std::endl;
      return -1;
    }
    std::cout << path.size() - 1 << " steps" << std::endl;
    
    std::cout << "Path: {";
    bool is_first = true;
    for (auto& v : path) {
      std::cout << (is_first ? "" : ", ") << v;
      // 何も出力されない (*)
      //std::cout << (is_first ? "" : ", ") << p[v];
      is_first = false;
    }
    std::cout << "}" << std::endl;
  }
  return 0;
}

