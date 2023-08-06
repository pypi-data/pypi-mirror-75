
#include "HandEvaluator.h"
#include "EquityCalculator.h"
#include "Constants.h"
#include "Util.h"
#include "libdivide.h"
#include <string>
#include "omp_wrapper.h"
#include "Random.h"
#include <iostream>
#include <unordered_set>
#include <unordered_map>
#include <vector>
#include <list>
#include <numeric>
#include <cmath>
#include <string>
#include <vector>
#include <random>
#include <algorithm>
#include <cmath>
#include <math.h>

using namespace std;
using namespace omp;

omp::EquityCalculator eq;
HandEvaluator eval;

int evaluator(char* cards)
{
  uint64_t board = CardRange::getCardMask(cards);
  Hand h = eq.getBoardFromBitmask(board);
  return eval.evaluate(h);

}


vector<double> hand_potential(char* hand_str , char* board_str, int monte_carlo_rounds, int num_opponents)
{




	uint64_t board_mask = CardRange::getCardMask(board_str);
	Hand board = eq.getBoardFromBitmask(board_mask);



	int64_t player_cards_mask = CardRange::getCardMask(hand_str);
	Hand player_hand_start = eq.getBoardFromBitmask(board_mask | player_cards_mask);
	

	uint64_t opponent_hands[6] = {};
	int behind = 2;
	int ahead = 1;
	int tied = 0;

	unsigned community_draw = BOARD_CARDS  - board.count();


	

	unsigned player_rank_start = eval.evaluate(player_hand_start);
	
	//cout << (player_hand_mask | board_mask) <<  "\n";
	//cout << player_rank_start << "\n";
	//cout << hand_str << " " << board_str << "\n";

	double total_hp[3] = {};
	double hp[3][3] = {};

	uint64_t usedCardsMask = 0;

	FastUniformIntDistribution<unsigned, 16> cardDist(0, CARD_COUNT - 1);
	typedef XoroShiro128Plus Rng;
	Rng rng{ std::random_device{}() };


	//enumerate monte carlo rounds
	for(unsigned i = 0; i < monte_carlo_rounds; i++){
		//cout << i << "\n";
		board_mask = CardRange::getCardMask(board_str);
		usedCardsMask = player_cards_mask | board_mask;
		for(unsigned j = 0; j < num_opponents; j++){
			opponent_hands[j] = 0;
			usedCardsMask = eq.randomizeBoard(opponent_hands[j],2,usedCardsMask,rng,cardDist);
		}

	

		//get ahead/behind before showdown
		unsigned n = is_best_hand(player_rank_start, opponent_hands, num_opponents, board_mask);
	
		//get ahead/behind behind showdown
		eq.randomizeBoard(board_mask, community_draw ,usedCardsMask,rng,cardDist);
	
		unsigned player_rank_end = eval.evaluate(eq.getBoardFromBitmask(board_mask | player_cards_mask));
		unsigned m = is_best_hand(player_rank_end, opponent_hands, num_opponents, board_mask);
		//cout << player_rank_end << "\n";
		//cout << n << ":" << m << " " << i << " " << monte_carlo_rounds << "\n";
		hp[n][m] += 1;
		total_hp[n] += 1;


		
	}


	

	vector<double> hand_strength_array;
	double npot = (hp[behind][ahead] + hp[behind][tied] / 2 + hp[tied][ahead] / 2) / (total_hp[behind] + total_hp[tied]);
	double ppot = (hp[ahead][behind] + hp[tied][behind] / 2 + hp[ahead][tied] / 2) / (total_hp[ahead] + total_hp[tied]);
	double hs = 1 - (total_hp[ahead] + total_hp[tied] / 2) / (total_hp[behind] + total_hp[tied] + total_hp[ahead]);
	
	if (isnan(ppot))
		ppot = 0;
	if (isnan(npot))
		npot = 0;
	
	hand_strength_array.push_back(hs);
	hand_strength_array.push_back(ppot);
	hand_strength_array.push_back(npot);

	//cout << hs << " " << ppot << " " << npot;

	return hand_strength_array;
}

int is_best_hand(int player_rank,uint64_t* playerHands, int nplayers , uint64_t& board){
	unsigned best_rank = 0;
	unsigned rank;
	for(unsigned i = 0; i < nplayers; i++){
		Hand hand = eq.getBoardFromBitmask(board | playerHands[i]);
		unsigned rank = eval.evaluate<true>(hand);

		if (rank > best_rank)
			best_rank = rank;

		//cout << rank << "\n";

	}


	if (player_rank < best_rank)
		return 1;
	else if(player_rank > best_rank)
		return 2;
	else
		return 0;

}


int best_hand_index(uint64_t* playerHands, int nplayers , uint64_t& board){
	unsigned best_rank = 0;
	unsigned best_rank_index = -1;
	unsigned rank;
	bool tied = false;
	for(unsigned i = 0; i < nplayers; i++){
		Hand hand = eq.getBoardFromBitmask(board | playerHands[i]);
		unsigned rank = eval.evaluate<true>(hand);

		if (rank > best_rank){
			best_rank = rank;
			best_rank_index = i;
			tied = false;
		}
		else if (rank == best_rank){
			tied = true;

		}
		

		//cout << rank << "\n";

	}
	if(tied)
		return -1;
	return best_rank_index;
}



vector<double> win_percentages(vector<vector<double>> sum_phs, vector<string> cards, char* player_cards_str,char* board_str, int monte_carlo_rounds, int player_index){


	unsigned wins = 0;
	uint64_t UsedCardsMask = 0;
	uint64_t all_hands[6] = {};

	vector<double> equities(sum_phs.size(),0); 

	uint64_t board_mask = CardRange::getCardMask(board_str);
	Hand board = eq.getBoardFromBitmask(board_mask);
	uint64_t player_cards_mask = CardRange::getCardMask(player_cards_str);

	unsigned community_draw = BOARD_CARDS - board.count();

	FastUniformIntDistribution<unsigned, 16> cardDist(0, CARD_COUNT - 1);
	typedef XoroShiro128Plus Rng;
	Rng rng{ std::random_device{}() };


	for(unsigned i = 0;i < monte_carlo_rounds; i++ ){
		board_mask = CardRange::getCardMask(board_str);
		UsedCardsMask = board_mask | player_cards_mask;

		for(unsigned j = 0; j < sum_phs.size(); j++){

			if(j == player_index){
				all_hands[j] = player_cards_mask;
				continue;
			}

	
			uint64_t cardsMask;
			do{
				double val = ((double(rand())/RAND_MAX));
				val = *lower_bound(sum_phs[j].begin(),sum_phs[j].end(),val);
				std::vector<double>::iterator itr = std::find(sum_phs[j].begin(),sum_phs[j].end(),val);
				unsigned cards_index = std::distance(sum_phs[j].begin(), itr);
				cardsMask = CardRange::getCardMask(cards[cards_index]);

			} while(UsedCardsMask & cardsMask);

			all_hands[j] = cardsMask;
			UsedCardsMask |= cardsMask;

		}

		eq.randomizeBoard(board_mask, community_draw ,UsedCardsMask,rng,cardDist);


		unsigned winner_index = best_hand_index(all_hands, sum_phs.size(),board_mask);
		if (winner_index != -1)
			equities[winner_index] +=1;
	}

	for(int i =0; i < sum_phs.size(); i++){
		equities[i] /= monte_carlo_rounds;
	
	}

	return equities;


}



vector<double> win_percentage(vector< vector < double > > prs, vector<string> cards, char* board_str, char* player_cards_str, int monte_carlo_rounds)
{
	unsigned wins = 0;
	unsigned losses = 0;
	unsigned ties = 0;

	uint64_t UsedCardsMask = 0;
	uint64_t opponent_hands[6] = {};

	uint64_t board_mask = CardRange::getCardMask(board_str);
	Hand board = eq.getBoardFromBitmask(board_mask);
	uint64_t player_cards_mask = CardRange::getCardMask(player_cards_str);

	unsigned community_draw = BOARD_CARDS - board.count();

	FastUniformIntDistribution<unsigned, 16> cardDist(0, CARD_COUNT - 1);
	typedef XoroShiro128Plus Rng;
	Rng rng{ std::random_device{}() };


	for(unsigned i = 0;i < monte_carlo_rounds; i++ ){
		board_mask = CardRange::getCardMask(board_str);
		UsedCardsMask = board_mask | player_cards_mask;

		for(unsigned j = 0; j < prs.size(); j++){

	
			uint64_t cardsMask;
			do{
				double val = ((double(rand())/RAND_MAX));
				val = *lower_bound(prs[j].begin(),prs[j].end(),val);
				std::vector<double>::iterator itr = std::find(prs[j].begin(),prs[j].end(),val);
				unsigned cards_index = std::distance(prs[j].begin(), itr);
				//cout << cards[cards_index] << "\n";
				cardsMask = CardRange::getCardMask(cards[cards_index]);

			} while(UsedCardsMask & cardsMask);

			opponent_hands[j] = cardsMask;
			UsedCardsMask |= cardsMask;

		}

		eq.randomizeBoard(board_mask, community_draw ,UsedCardsMask,rng,cardDist);


		unsigned player_rank = eval.evaluate(eq.getBoardFromBitmask(board_mask | player_cards_mask));
		unsigned winner = is_best_hand(player_rank,opponent_hands,prs.size(),board_mask);

		if(winner == 1)
			losses +=1;
		else if(winner == 2)
			wins +=1;
		else
			ties +=1;

	}


	vector<double> win_array;
	win_array.push_back(double(losses)/double(monte_carlo_rounds));
	win_array.push_back(double(wins) / double( monte_carlo_rounds));
	win_array.push_back(double(ties)/ double(monte_carlo_rounds));


	return win_array;


}


int main(){
	return 1;
}