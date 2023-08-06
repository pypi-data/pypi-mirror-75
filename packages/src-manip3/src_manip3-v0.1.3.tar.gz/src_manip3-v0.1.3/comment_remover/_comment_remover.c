#include <Python.h>
#include "comment_remover.h"


static PyObject* method_js_rem_comments(PyObject* self, PyObject* args)
{
    char* source_code = NULL;

    /* Parsing arguments passed by Python */
    if (!PyArg_ParseTuple(args, "s*", &source_code))
        return NULL;

    char* result = js_rem_comments(source_code);

    if (!result)
    {
        PyErr_SetString(PyErr_NoMemory, "Could not allocate enough memory.");
        return NULL;
    }

    PyObject* result_obj = PyBytes_FromString(result);
    free(result);

    return result_obj;
}


static PyMethodDef comment_remover_methods[] =
{
    { "js_rem_comments", method_js_rem_comments, METH_VARARGS, "Python - C interface for removing comments from JavaScript source code." },
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef comment_remover_module =
{
    PyModuleDef_HEAD_INIT,
    "comment_remover",
    "Python - C interface for removing comments from source code.",
    -1,
    comment_remover_methods
};


PyMODINIT_FUNC PyInit_comment_remover(void)
{
    return PyModule_Create(&comment_remover_module);
}
