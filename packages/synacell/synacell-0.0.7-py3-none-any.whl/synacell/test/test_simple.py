import synacell.cmodule
import synacell.signal
from synacell.test.testfunc import Test


def test_simple_1() -> (int, str):
    """
    Test creating net in the memory space of snn.dll.

    net1 is deleted throuh the api, net2 is deleted throgh Net method and on net3
    destructor is called when this function exits. The destructor call on net3
    can be seen in the log file.

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """

    api = synacell.cmodule.SnnAPI
    net1 = api.new_net()
    net2 = api.new_net()
    net3 = api.new_net()
    api.delete_net(net1)
    net2.delete()

    if net1.ptr is None and net2.ptr is None:
        return 0, "Success"
    else:
        return 1, f"Net id not deleted"


def test_simple_2() -> (int, str):
    """
    Test creating net wit parts in snn.dll. Changing part parameters

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """

    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellData")
    params = net.get_params(0)
    if params != 'id=0,type=CellData,file=,pos=0,dataSize=0,sampleRate=0':
        return 1, "Add part params error"
    net.set_params(0, "pos=120")
    params = net.get_params(0)
    if params != 'id=0,type=CellData,file=,pos=120,dataSize=0,sampleRate=0':
        return 2, "Set params error"
    return 0, "Success"


def test_simple_3() -> (int, str):
    """
    Run net on generated wav data. Gather output.

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """

    # Generate wav file
    signal = synacell.signal
    sin1 = signal.func_generator(func_name="sin", freq=100.0, amp=30.0, phase=0.0)
    sin2 = signal.func_generator(func_name="sin", freq=300.0, amp=40.0, phase=0.0)
    sin3 = signal.func_generator(func_name="sin", freq=633.0, amp=20.0, phase=0.0)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
    sin2_arr = signal.func_to_nparray(func=sin2, t_min=0.5, t_max=1.0)
    sin3_arr = signal.func_to_nparray(func=sin3, t_min=0.3, t_max=1.0)
    signal.make_wav(sin1_arr + sin2_arr + sin3_arr, "./test_simple_3.wav")

    api = synacell.cmodule.SnnAPI
    api.set_log_file("./test_simple_3.log")
    net = api.new_net()
    net.add_part("id=0,type=CellData,file=./test_simple_3.wav")
    params = net.get_params(0)
    if params != ("id=0,type=CellData,file=./test_simple_3.wav," +
                  "pos=0,dataSize=16000,sampleRate=16000"):
        return 1, "Add part params error"
    net.set_recorder("id=0,pid=0,value=vo,beg=0,size=1000")
    net.reset()
    net.run(14118, 1.0/16000.0)
    record = net.get_record(0)
    api.print_log_file()
    if record.size == 1000:
        return 0, "Success"
    else:
        return 1, "Record data loading error"


def run_all_simple():
    import sys
    finame = sys.prefix
    test_li = [test_simple_1, test_simple_2, test_simple_3]
    return Test.run_test_li(test_li, "test_simple")


if __name__ == '__main__':
    '''
    1. If the module is ran (not imported) the interpreter sets this at the top of your module:
    ```
    __name__ = "__main__"
    ```
    2. If the module is imported: 
    ```
    import rk
    ```
    The interpreter sets this at the top of your module:
    ```
    __name__ = "rk"
    ```
    '''
    run_all_simple()
