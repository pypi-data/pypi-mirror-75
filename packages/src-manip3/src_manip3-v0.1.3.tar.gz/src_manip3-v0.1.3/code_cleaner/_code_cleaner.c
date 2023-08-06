#include <Python.h>
#include "code_cleaner.h"


static PyObject* method_clean_nl(PyObject* self, PyObject* args)
{
    char* source_code = NULL;

    /* Parsing arguments passed by Python */
    if (!PyArg_ParseTuple(args, "s*", &source_code))
        return NULL;

    char* result = clean_nl(source_code);

    if (!result)
    {
        PyErr_SetString(PyErr_NoMemory, "Could not allocate enough memory.");
        return NULL;
    }

    PyObject* result_obj = PyBytes_FromString(result);
    free(result);

    return result_obj;
}


static PyMethodDef code_cleaner_methods[] =
{
    { "clean_nl", method_clean_nl, METH_VARARGS, "Python - C interface for removing unnecessary new line characters from a string." },
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef code_cleaner_module =
{
    PyModuleDef_HEAD_INIT,
    "code_cleaner",
    "Python - C interface for removing unnecessary new line characters from a string.",
    -1,
    code_cleaner_methods
};


PyMODINIT_FUNC PyInit_code_cleaner(void)
{
    return PyModule_Create(&code_cleaner_module);
}
