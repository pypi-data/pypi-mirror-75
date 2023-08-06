#include <string.h>
#include <stdlib.h>
#include <memory.h>
#include <ctype.h>
#include <stdbool.h>

#include "code_cleaner.h"


/**
 * @brief is_space_line - determines if next line in a string only builds up from whitespaces
 * @param str - the string to check, needs to be null terminated
 *
 * @return 0 if the next line contains non whitespace characters, otherwise the number
 *         of whitespace characters will be returned (if the next line only contains whitespaces)
 */
unsigned long long is_space_line(const char* str)
{
    const char* c = str;
    unsigned long long bytes = 0;
    while (*c)
    {
        /* if we found a non whitespace character, return with zero */
        if (!isspace(*c))
            return 0;

        /* if we ate a new line character exit with skipping that, too */
        if (*c == '\n')
            return bytes + 1;

        ++bytes;
        ++c;
    }

    /* number of characters skipped */
    return bytes;
}


/**
 * @brief clean_nl - clears unnecessary new line characters from code
 * @param src - the code to be cleaned from double or higher order new lines
 *
 * @return the cleaned code without duplicate new lines or empty lines
 */
char* clean_nl(const char* src)
{
    if (!src)
        return NULL;

    unsigned long long len, bytes = 0;

    /* get length of input string and return empty string if it is empty */
    if (!(len = strlen(src)))
    {
        char* out_src = (char*) malloc(sizeof(char));
        out_src[0] = '\x0';
        return out_src;
    }


    /* allocate just enough memory for the return buffer */
    char* in_src = (char*) malloc((len + 1) * sizeof(char));
    if (!in_src)
        return NULL;

    in_src[len] = '\x0';

    bool counted = false;
    unsigned long long skipping;
    unsigned long long i = is_space_line(src);
    for (; i < len; ++i)
    {
        char c = src[i];
        char* cc = &in_src[bytes];

        if (c == '\n' || c == '\r')
        {
            if (counted)
                continue;
            counted = true;

            skipping = is_space_line(src + i + 1);
            i += skipping;
            if (skipping)
            {
                *cc = '\n';
                ++bytes;
                continue;
            }

            if (c == '\r') c = '\n';
        }
        else if (counted && (skipping = is_space_line(src + i)))
        { i += skipping; }
        else
        { counted = false; }

        *cc = c;
        ++bytes;
    }


    char* out_src = (char*)realloc(in_src, (bytes + 1)*sizeof(char));
    /* should be able to reallocate less than or equal to the original memory, but checking to be safe */
    if (!out_src)
    {
        free(in_src);
        return NULL;
    }

    out_src[bytes] = '\x0';


    return out_src;
}
