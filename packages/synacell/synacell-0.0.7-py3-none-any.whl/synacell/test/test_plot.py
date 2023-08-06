import synacell.cmodule
import synacell.signal
from synacell.test.testfunc import Test
import matplotlib.pyplot as plt
import math


def test_plot_1() -> (int, str):
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
    signal.make_wav(sin1_arr + sin2_arr + sin3_arr, "./test_plot_1.wav")

    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellData,file=./test_plot_1.wav")
    params = net.get_params(0)
    if params != ("id=0,type=CellData,file=./test_plot_1.wav," +
                  "pos=0,dataSize=16000,sampleRate=16000"):
        return 1, "Add part params error"
    net.set_recorder("id=0,pid=0,value=vo,beg=7000,size=3000")
    net.reset()
    net.run(14118, 1.0/16000.0)
    record = net.get_record(0)

    if record.size != 3000:
        return 1, "Record data loading error"

    plt.plot([i * 1.0 / 16000.0 for i in record.pc], record.data, label="CellData[vo]")
    plt.grid(True)
    plt.xlabel("Time [s]")
    plt.legend()
    plt.show()

    return 0, "Success"


def test_plot_2() -> (int, str):
    """
    Run net on generated wav data. Gather output.

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """
    # Generate wav file
    signal = synacell.signal
    sin1 = signal.func_generator(func_name="sin", freq=133.0, amp=30.0, phase=0.0)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
    signal.make_wav(sin1_arr, "./test_plot_2.wav")

    api = synacell.cmodule.SnnAPI
    api.set_log_file("./test_plot_2.log")
    net = api.new_net()
    net.add_part("id=0,type=CellData,file=./test_plot_2.wav")
    net.add_part("id=1,type=CellValve")
    net.add_part("id=1000,type=SynaBuffer,ciid=0,coid=1")
    net.set_recorder("id=0,pid=1,value=vi,beg=0,size=1000")
    net.set_recorder("id=1,pid=1,value=vo,beg=0,size=1000")
    net.connect_syna()

    for i in range(2):
        if i == 1:
            net.set_params(1, "ofs=10,opn=7,cls=14")
        net.reset()
        net.run(16000, 1.0 / 16000.0)
        record = [net.get_record(0), net.get_record(1)]

        if record[0].size != 1000:
            return 1, "Record data loading error"

        plt.plot([i * 1.0 / 16000.0 for i in record[0].pc], record[0].data, label="CellValve[vi]")
        plt.plot([i * 1.0 / 16000.0 for i in record[1].pc], record[1].data, label="CellValve[v0]")
        plt.grid(True)
        plt.xlabel("Time [s]")
        plt.legend()
        plt.show()

    return 0, "Success"


def test_plot_3() -> (int, str):
    """
    Run net on generated wav data. Gather output for verification of
    Runge-Kutta method for circuit solving.

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """
    # Generate wav file
    signal = synacell.signal
    sin1 = signal.func_generator(func_name="sin", freq=123.0, amp=5.0, phase=0.0)
    sin2 = signal.func_generator(func_name="sin", freq=246.0, amp=10.0, phase=0.0)
    sin3 = signal.func_generator(func_name="sin", freq=633.0, amp=7.0, phase=0.0)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
    sin2_arr = signal.func_to_nparray(func=sin2, t_min=0.5, t_max=1.0)
    sin3_arr = signal.func_to_nparray(func=sin3, t_min=0.3, t_max=1.0)
    signal.make_wav(sin1_arr + sin2_arr + sin3_arr, "./test_plot_3.wav")

    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellData,file=./test_plot_3.wav")
    net.add_part("id=1,type=CellValve,ofs=10,opn=7,cls=14")
    net.add_part("id=2,type=CellBuffer")
    net.add_part("id=3,type=CellBuffer")
    net.add_part("id=4,type=CellBuffer")
    net.add_part("id=1000,type=SynaBuffer,ciid=0,coid=1")
    net.add_part("id=1001,type=SynaBuffer,ciid=1,coid=2")
    net.add_part("id=1002,type=SynaRPC,ciid=2,coid=3")
    net.add_part("id=1003,type=SynaBuffer,ciid=3,coid=4")
    net.connect_syna()
    net.set_recorder("id=0,pid=1002,value=vi,beg=0,size=2000")
    net.set_recorder("id=1,pid=1002,value=vo,beg=0,size=2000")

    net.reset()
    net.run(16000, 1.0 / 16000.0)
    record = [
        net.get_record(0),
        net.get_record(1)
    ]

    if record[0].size != 2000:
        return 1, "Record data loading error"

    plt.plot([i * 1.0 / 16000.0 for i in record[0].pc], record[0].data, '.-', label="id_1002_vi")
    plt.plot([i * 1.0 / 16000.0 for i in record[1].pc], record[1].data, '.-', label="id_1002_vo")
    plt.grid(True)
    plt.xlabel("Time [s]")
    plt.legend()
    plt.show()

    return 0, "Success"


def test_plot_4() -> (int, str):
    """
    Run net on generated wav data. Gather output for verification of
    Runge-Kutta method for circuit solving.

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """
    # Generate wav file
    signal = synacell.signal
    sin1 = signal.func_generator(func_name="sin", freq=123.0, amp=1000.0, phase=0.0)
    sin2 = signal.func_generator(func_name="sin", freq=246.0, amp=2000.0, phase=0.0)
    sin3 = signal.func_generator(func_name="sin", freq=73.0, amp=1347.0, phase=0.0)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
    sin2_arr = signal.func_to_nparray(func=sin2, t_min=0.5, t_max=1.0)
    sin3_arr = signal.func_to_nparray(func=sin3, t_min=0.3, t_max=1.0)
    signal.make_wav(sin1_arr + sin2_arr + sin3_arr, "./test_plot_4.wav")

    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellData,file=./test_plot_4.wav")
    net.add_part("id=1000,type=SynaBuffer,ciid=0,coid=1")
    net.add_part("id=1,type=CellValve,ofs=10,opn=9,cls=14")
    net.add_part("id=1001,type=SynaBuffer,ciid=0,coid=2")
    net.add_part("id=2,type=CellValve,ofs=20,opn=7,cls=14")
    net.add_part("id=1002,type=SynaBuffer,ciid=1,coid=3")
    net.add_part("id=1003,type=SynaBuffer,ciid=2,coid=3")
    net.add_part("id=3,type=CellBuffer")
    net.add_part("id=1004,type=SynaRPC,ciid=1,coid=4")
    net.add_part("id=1005,type=SynaRPC,ciid=2,coid=4")
    net.add_part("id=4,type=CellBuffer")

    net.connect_syna()
    net.set_recorder("id=0,pid=0,value=vo,beg=1000,size=500")
    net.set_recorder("id=1,pid=1,value=vi,beg=1000,size=500")
    net.set_recorder("id=2,pid=1,value=vo,beg=1000,size=500")
    net.set_recorder("id=3,pid=2,value=vo,beg=1000,size=500")
    net.set_recorder("id=4,pid=3,value=vi,beg=1000,size=500")
    net.set_recorder("id=5,pid=4,value=vi,beg=1000,size=500")

    net.reset()
    net.run(16000, 1.0 / 16000.0)
    record = [
        net.get_record(0),
        net.get_record(1),
        net.get_record(2),
        net.get_record(3),
        net.get_record(4),
        net.get_record(5)
    ]

    plt.plot([i * 1.0 / 16000.0 for i in record[0].pc], record[0].data, '.-', label="data vo")
    plt.plot([i * 1.0 / 16000.0 for i in record[1].pc], record[1].data, '.--', label="valve 1 vi")
    plt.plot([i * 1.0 / 16000.0 for i in record[2].pc], record[2].data, '--', label="valve 1 vo")
    plt.plot([i * 1.0 / 16000.0 for i in record[3].pc], record[3].data, '--', label="valve 2 vo")
    plt.plot([i * 1.0 / 16000.0 for i in record[4].pc], record[4].data, '-',
             label="valve 1 + valve 2 -> buffer (SynaBuffer)")
    plt.plot([i * 1.0 / 16000.0 for i in record[5].pc], record[5].data, '-',
             label="valve 1 + valve 2 -> buffer (SynaRPC)")
    plt.grid(True)
    plt.xlabel("Time [s]")
    plt.legend()
    plt.show()

    return 0, "Success"


def test_plot_5() -> (int, str):
    """
    Run net on generated wav data. Gather output for verification of
    Runge-Kutta method for circuit solving.

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """
    # Generate wav file
    signal = synacell.signal
    sin1 = signal.func_generator(func_name="sin", freq=123.0, amp=1000.0, phase=0.0)
    sin2 = signal.func_generator(func_name="sin", freq=246.0, amp=2000.0, phase=0.0)
    sin3 = signal.func_generator(func_name="sin", freq=73.0, amp=1347.0, phase=0.0)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
    sin2_arr = signal.func_to_nparray(func=sin2, t_min=0.5, t_max=1.0)
    sin3_arr = signal.func_to_nparray(func=sin3, t_min=0.3, t_max=1.0)
    signal.make_wav(sin1_arr + sin2_arr + sin3_arr, "./test_plot_5.wav")

    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellData,file=./test_plot_5.wav")
    net.add_part("id=1000,type=SynaBuffer,ciid=0,coid=1")
    net.add_part("id=1,type=CellValve,ofs=30,opn=2,cls=14")
    net.add_part("id=1001,type=SynaBuffer,ciid=0,coid=2")
    net.add_part("id=2,type=CellValve,ofs=20,opn=7,cls=14")
    net.add_part("id=1002,type=SynaBuffer,ciid=1,coid=3")
    net.add_part("id=1003,type=SynaBuffer,ciid=2,coid=3")
    net.add_part("id=3,type=CellBuffer")
    net.add_part("id=1004,type=SynaRPC,ciid=1,coid=4")
    net.add_part("id=1005,type=SynaRPC,ciid=2,coid=4")
    net.add_part("id=4,type=CellBuffer")
    net.add_part("id=1006,type=SynaRPC,ciid=1,coid=5")
    net.add_part("id=1007,type=SynaRPC,ciid=2,coid=5")
    net.add_part("id=5,type=CellIntegrator")

    net.connect_syna()
    net.set_recorder("id=0,pid=0,value=vo,beg=0,size=10000")
    net.set_recorder("id=1,pid=1,value=vi,beg=0,size=10000")
    net.set_recorder("id=2,pid=1,value=vo,beg=0,size=10000")
    net.set_recorder("id=3,pid=2,value=vo,beg=0,size=10000")
    net.set_recorder("id=4,pid=3,value=vi,beg=0,size=10000")
    net.set_recorder("id=5,pid=4,value=vi,beg=0,size=10000")
    net.set_recorder("id=6,pid=5,value=vo,beg=0,size=10000")

    net.reset()
    net.run(16000, 1.0 / 16000.0)
    record = [
        net.get_record(0),
        net.get_record(1),
        net.get_record(2),
        net.get_record(3),
        net.get_record(4),
        net.get_record(5),
        net.get_record(6)
    ]

    plt.plot([i * 1.0 / 16000.0 for i in record[4].pc], record[4].data, '-',
             label="valve 1 + valve 2 -> buffer (SynaBuffer)")
    plt.plot([i * 1.0 / 16000.0 for i in record[5].pc], record[5].data*10, '-',
             label="valve 1 + valve 2 -> buffer (SynaRPC)")
    plt.plot([i * 1.0 / 16000.0 for i in record[6].pc], record[6].data, '-',
             label="valve 1 + valve 2 -> integrator (SynaRPC)")
    plt.grid(True)
    plt.xlabel("Time [s]")
    plt.legend()
    plt.show()

    return 0, "Success"


def run_all_plot() -> int:
    test_li = [test_plot_1, test_plot_2, test_plot_3, test_plot_4, test_plot_5]
    return Test.run_test_li(test_li, "test_plot")


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
    run_all_plot()
