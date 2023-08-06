
int evaluator(char* cards);
std::vector<double> hand_potential(char* hand_str , char* board_str, int monte_carlo_rounds, int num_opponents);
int is_best_hand(int player_rank, uint64_t* playerHands, int nplayers, uint64_t& board);
std::vector<double> win_percentage(std::vector< std::vector < double > > prs, std::vector<std::string> cards, char* board_str, char* player_cards_str, int monte_carlo_rounds);
std::vector<double> win_percentages(std::vector<std::vector<double>> sum_phs, std::vector<std::string> cards, char* player_cards_str,char* board_str, int monte_carlo_rounds,int player_index);