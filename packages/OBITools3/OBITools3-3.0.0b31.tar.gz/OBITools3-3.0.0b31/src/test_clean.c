#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#include "../src/obidms.h"
#include "../src/obiview.h"
#include "../src/obidmscolumn.h"
#include "../src/obi_clean.h"


// gcc -g -o cleantest test_clean.c ../src/*.c ../src/libecoPCR/*.c ../src/libecoPCR/libapat/*.c ../src/libecoPCR/libthermo/*.c ../src/libjson/*.c
// gcc -g -o cleantest libjson/*.c bloom.c *indexer.c crc64.c encode.c hashtable.c linked_list.c murmurhash2.c obiavl.c obiblob.c obidms*.c obierrno.c obilittlebigman.c obitypes.c obiview.c sse_banded_LCS_alignment.c upperband.c utils.c obi_clean.c obisig.c test_clean.c


int main( int argc, const char* argv[] )
{
	OBIDMS_p dms;
	Obiview_p seq_view;
	Obiview_p score_view;
	OBIDMS_column_p seq_column;
	OBIDMS_column_p id1_column;
	OBIDMS_column_p id2_column;
	OBIDMS_column_p score_column;
	double threshold = 0.97;
	bool normalize = true;
	int reference = 0;
	bool similarity_mode = true;
	
	fprintf(stderr, "\nyah\n");

//	obi_clean("/Users/celinemercier/Documents/Peoples_stuff/Irene/irene",
//			  "v1",
//			  "merged_sample",
//			  "v1_cleaned",
//			  "{}",
//			  1,
//			  0.5,
//			  true,
//			  1);

	obi_clean("/Users/celinemercier/Documents/workspace/OBITools3/giulia",
			  "v1",
			  "sample",
			  "c1",
			  "{}",
			  1,
			  0.5,
			  true,
			  -1);

	fprintf(stderr, "\npouic pouic\n");

	return 0;
}

