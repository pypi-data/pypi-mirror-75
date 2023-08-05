#include "igeAutoTest.h"
#include "igeAutoTest_doc_en.h"

PyObject* autoTest_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	autoTest_obj* self = NULL;

	self = (autoTest_obj*)type->tp_alloc(type, 0);
	self->autoTest = AutoTest::Instance();

	return (PyObject*)self;
}

void autoTest_dealloc(autoTest_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* autoTest_str(autoTest_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "autoTest object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* autoTest_IsLoopTest(autoTest_obj* self)
{
    PyObject *result;
    result = Py_BuildValue("O", AutoTest::Instance()->isLoopTest() ? Py_True : Py_False);
    return result;
}

static PyObject* autoTest_FinishLoopTest(autoTest_obj* self)
{
    AutoTest::Instance()->finishLoop();

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* autoTest_WriteResultsTest(autoTest_obj* self, PyObject* args)
{
    char* name;
    char* value;
    if (!PyArg_ParseTuple(args, "ss", &name, &value)) return NULL;
        
    AutoTest::Instance()->writeResults(name, value);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* autoTest_Screenshots(autoTest_obj* self)
{
    AutoTest::Instance()->screenshots();

    Py_INCREF(Py_None);
    return Py_None;
}

PyMethodDef autoTest_methods[] = {
    { "isLoopTest", (PyCFunction)autoTest_IsLoopTest, METH_NOARGS, autoTestIsLoopTest_doc },
    { "finishLoopTest", (PyCFunction)autoTest_FinishLoopTest, METH_NOARGS, autoTestFinishLoopTest_doc },
    { "writeResultsTest", (PyCFunction)autoTest_WriteResultsTest, METH_VARARGS, autoTestWriteResultsTest_doc },
    { "screenshots", (PyCFunction)autoTest_Screenshots, METH_NOARGS, autoTestScreenshots_doc },
	{ NULL,	NULL }
};

PyGetSetDef autoTest_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject AutoTestType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeAutoTest",						/* tp_name */
	sizeof(autoTest_obj),				/* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)autoTest_dealloc,		/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)autoTest_str,				/* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	0,									/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	autoTest_methods,					/* tp_methods */
	0,                                  /* tp_members */
	autoTest_getsets,					/* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	autoTest_new,						/* tp_new */
	0,									/* tp_free */
};

static PyModuleDef autoTest_module = {
	PyModuleDef_HEAD_INIT,
	"igeAutoTest",						// Module name to use with Python import statements
	"igeAutoTest Module.",				// Module description
	0,
	autoTest_methods					// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeAutoTest() {
	PyObject* module = PyModule_Create(&autoTest_module);
    return module;
}
