#ifndef __SIMPLE_PERIODIC_CORE_H__
#define __SIMPLE_PERIODIC_CORE_H__

typedef double real;
typedef int bool;

int* new_counts( int order, int radix );
void free_counts( int* v, int order );
void fill_in_counts( int order, int radix, int* counts, int* string, int string_len, int phase, int period );
real* counts_to_probs( int order, int radix, int* counts );
void free_probs( real* probs, int order );
real* new_real_array( int size );
real* probs_to_score_matrix( int order, int radix, real* pos_probs, real* neg_probs );
void free_scores( real* scores );
bool score_string( int order, int radix, real** score_matrix, int* string, int start, int length, real* rval, int period );
/*bool score_string_positions( int order, int radix, real** score_matrix, int* string, float* target, int start, int length );*/

#endif
