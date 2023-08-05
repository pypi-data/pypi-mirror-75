/****************************************************************************
 * OBIDMS_column_dict functions                                              *
 ****************************************************************************/

/**
 * @file obidsmcolumn_dict.c
 * @author Celine Mercier
 * @date June 10th 2020
 * @brief Functions handling OBIColumns containing dictionaries.
 */


#include <stdlib.h>
#include <stdio.h>

#include "obidmscolumn.h"
#include "obitypes.h"
#include "obidmscolumn_str.h"
#include "hashtable.h"

/**********************************************************************
 *
 * D E F I N I T I O N   O F   T H E   P U B L I C   F U N C T I O N S
 *
 **********************************************************************/



const void* obi_column_get_str_dict(OBIDMS_column_p column, index_t line_nb)
{
	const char* str_dict;
	hashtable_p dict;

	if (obi_column_prepare_to_get_value(column, line_nb) < 0)
	{
//		*value_length_p = -1;
		return OBITuple_NA;
	}

//	str_dict = obi_column_get_obistr_with_elt_idx(column, line_nb, 0);
//	if (str_dict == NULL)
		return NULL;

//	// Check NA
//	if (idx == OBIIdx_NA)
//	{
//		*value_length_p = 0;
//		return OBITuple_NA;
//	}

//	dict = parse_dict(str_dict);  // TODO bypass, return

	return dict;
}


const void* obi_column_get_int_dict(OBIDMS_column_p column, index_t line_nb)
{
	return NULL;
}
