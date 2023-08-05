import sys, os

mpi_available = True
try:
    from mpi4py import MPI
except:
    mpi_available = False

# Windows has a bug that causes mpi4_py to not function
if mpi_available and not sys.platform.startswith('win32'):
    comm = MPI.COMM_WORLD
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    def get_process_rank():
        return comm.Get_rank()
    def get_process_size():
        return comm.Get_size()
    def is_first_process():
        return get_process_rank() == 0
    def world_allgather(data):
        return comm.allgather(data)
    def Bcast(data, root=0):
        return comm.Bcast(data, root)
    def bcast(data, root=0):
        return comm.bcast(data, root)
else:
    # We don't have support for MPI on Windows yet due to a bug in mpi4py,
    # so we add stub functions
    def get_process_rank():
        return 0
    def get_process_size():
        return 1
    def is_first_process():
        return get_process_rank() == 0
    def world_allgather(data):
        return [data]
    def Bcast(data, root=0):
        return data
    def bcast(data, root=0):
        return data