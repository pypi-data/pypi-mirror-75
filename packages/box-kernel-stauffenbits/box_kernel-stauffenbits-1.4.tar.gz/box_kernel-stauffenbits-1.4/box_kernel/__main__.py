from ipykernel.kernelapp import IPKernelApp
from . import BoxKernel

IPKernelApp.launch_instance(kernel_class=BoxKernel)
