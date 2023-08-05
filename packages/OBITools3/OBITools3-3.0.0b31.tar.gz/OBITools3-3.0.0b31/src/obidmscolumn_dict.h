/****************************************************************************
 * Dictionary columns header file                                           *
 ****************************************************************************/

/**
 * @file obidsmcolumn_dict.h
 * @author Celine Mercier
 * @date June 10th 2020
 * @brief Header file for the functions handling OBIColumns containing data in the form of dictionaries.
 */


#ifndef OBIDMSCOLUMN_DICT_H_
#define OBIDMSCOLUMN_DICT_H_


#include <stdlib.h>
#include <stdio.h>

#include "obidmscolumn.h"
#include "obitypes.h"


/**
 * @brief Sets a value in an OBIDMS column containing data in the form of dictionaries.
 *
 * @warning Pointers returned by obi_open_column() don't allow writing.
 *
 * @param column A pointer as returned by obi_create_column().
 * @param line_nb The number of the line where the value should be recovered.
 *
 * @returns The recovered value.
 * @retval NULL if an error occurred and obi_errno is set.
 *
 * @since June 2020
 * @author Celine Mercier (celine.mercier@metabarcoding.org)
 */
const void* obi_column_get_str_dict(OBIDMS_column_p column, index_t line_nb);

#endif /* OBIDMSCOLUMN_DICT_H_ */

