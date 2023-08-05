#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "sph_groestl.h"

#if _MSC_VER >= 1500
typedef __int32 int32_t;
typedef unsigned __int32 uint32_t;
#endif

static void GroestlCoinHash(const char *input, Py_ssize_t length, char *output)
{
    uint32_t hashA[16], hashB[16];

    sph_groestl512_context ctx_groestl[2];

    sph_groestl512_init(&ctx_groestl[0]);
    sph_groestl512 (&ctx_groestl[0], input, length);
    sph_groestl512_close(&ctx_groestl[0], hashA);

    sph_groestl512_init(&ctx_groestl[1]);
    sph_groestl512 (&ctx_groestl[1], hashA, 64);
    sph_groestl512_close(&ctx_groestl[1], hashB);

    memcpy(output, hashB, 32);
}

static PyObject *groestlcoin_gethash(PyObject *self, PyObject *args)
{
    char *output;
    PyObject *value;
#if PY_MAJOR_VERSION >= 3
    PyBytesObject *input;
#else
    PyStringObject *input;
#endif
    Py_ssize_t length;
    if (!PyArg_ParseTuple(args, "Sn", &input, &length))
        return NULL;
    Py_INCREF(input);
    output = PyMem_Malloc(32);

#if PY_MAJOR_VERSION >= 3
    GroestlCoinHash((char *)PyBytes_AsString((PyObject*) input), length, output);
#else
    GroestlCoinHash((char *)PyString_AsString((PyObject*) input), length, output);
#endif
    Py_DECREF(input);
#if PY_MAJOR_VERSION >= 3
    value = Py_BuildValue("y#", output, 32);
#else
    value = Py_BuildValue("s#", output, 32);
#endif
    PyMem_Free(output);
    return value;
}

static PyMethodDef GroestlcoinMethods[] = {
    { "getHash", groestlcoin_gethash, METH_VARARGS, "Returns the groestlcoin hash" },
    { NULL, NULL, 0, NULL }
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef GroestlcoinModule = {
    PyModuleDef_HEAD_INIT,
    "groestlcoin_hash",
    "...",
    -1,
    GroestlcoinMethods
};

PyMODINIT_FUNC PyInit_groestlcoin_hash(void) {
    return PyModule_Create(&GroestlcoinModule);
}

#else

PyMODINIT_FUNC initgroestlcoin_hash(void) {
    (void) Py_InitModule("groestlcoin_hash", GroestlcoinMethods);
}
#endif
