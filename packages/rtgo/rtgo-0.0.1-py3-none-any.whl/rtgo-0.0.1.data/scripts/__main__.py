from threading import Thread
import multiprocessing
import copy
import numpy


class MyThread(Thread):
    def __init__(self, thread_id, name, func, args, logger, data_index):
        """
        Constructor
        :param int thread_id: ID number
        :param str name: thread name
        :param function func: function to run on the thread
        :param list args: list of args to be passed to the function
        :param logging.Logger logger: project logger
        :param int data_index: list index of data within the args list
        """
        Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.__result = MyThreadResult(self.thread_id)
        self.__func = func
        self.__args = args
        self.__logger = logger
        self.__data_index = data_index

    def run(self):
        """
        Run the supplied function
        :return: value returned by function
        """
        self.__logger.info(f"Thread-{self.thread_id} running")
        try:
            # Check if the data must be run individually or passed as is.
            func_args = self.__args
            temp_args = copy.deepcopy(func_args)
            for i in range(len(func_args[self.__data_index])):
                temp_args[self.__data_index] = copy.deepcopy(func_args[self.__data_index][i])
                self.__result.set_return_value(self.__func(*temp_args))

        except Exception as e:
            self.__result.set_error(e)

    def join(self, timeout=None):
        """
        returns the result of the run
        :return: result
        :rtype: MyThreadResult
        """
        Thread.join(self)
        self.__logger.info(f"Thread-{self.thread_id} finishing")
        return self.__result


class MyBasicThread(Thread):
    def __init__(self, thread_id, name, func, logger):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.__result = MyThreadResult(self.thread_id)
        self.__func = func
        self.__logger = logger

    def run(self):
        """
        Run the supplied function
        :return: value returned by function
        """
        self.__logger.info(f"Thread-{self.thread_id} running")
        try:
            self.__result.set_return_value(self.__func())
        except Exception as e:
            self.__result.set_error(e)

    def join(self, timeout=None):
        """
        returns the result of the run
        :return: result
        :rtype: MyThreadResult
        """
        Thread.join(self)
        self.__logger.info(f"Thread-{self.thread_id} finishing")
        return self.__result


class MyThreadResult:
    def __init__(self, thread_id):
        """
        Stores results of MyThread objects
        :param int thread_id: thread ID
        """
        self.thread_id = thread_id
        self.__return_value = []
        self.__error = None

    def set_return_value(self, val):
        self.__return_value.append(val)

    def get_return_value(self):
        return self.__return_value

    def set_error(self, error):
        self.__error = error

    def get_error(self):
        return self.__error


class ReadyThready:
    from logging import Logger

    def __init__(self, logger=Logger("JobHandler Logger")):
        """
        splits jobs over specified/determined number of CPUs
        :param logging.Logger logger: project logger
        """
        self.logger = logger

    def __get_results_from_threads(self, running_threads):
        """
        for each running thread, get the results and return as a flat list
        :param running_threads:
        :return: list of results or Error
        """
        thread_results = []

        if running_threads:
            for thread in running_threads:
                try:
                    result = thread.join()
                    return_data = result.get_return_value()
                    error = result.get_error()

                    if return_data:
                        thread_results.append(return_data)
                    else:
                        thread_results.append(error)
                        self.logger.error(f"{error.__class__}: Results error from {thread.name}: {error}")

                except Exception as e:
                    self.logger.error(f"{e.__class__}: Unable to collect results from {thread.name} "
                                      f"({thread.__func.__name__})")

            try:
                # Re-combine the results to return as if a single thread was used (flatten list)
                return_val = [item for sublist in thread_results for item in sublist]

                return return_val

            except Exception as e:
                self.logger.error(f"{e.__class__}: could not process the following results:\n\t\t{thread_results}")
                return e

    def go_cluster(self, funcs):
        """
        runs the given functions concurrently
        :param funcs: list of functions to run
        :return: list containing results from each function executed
        """
        running_threads = []

        # create a thread for each supplied function
        for i in range(len(funcs)):
            thread_id = i + 1
            thread = MyBasicThread(thread_id, f"Thread-{thread_id}", funcs[i], self.logger)
            thread.daemon = True
            running_threads.append(thread)
            thread.start()

        return self.__get_results_from_threads(running_threads)

    def go(self, func, args, arg_data_index, n_threads=0):
        """
        runs the function across n CPU threads
        :param function func: function to run
        :param list args: args to be passed to the function
        :param int arg_data_index: list index of the arg
        :param int n_threads: number of threads
        :return: list of results from running the function
        """
        # initialise lists of running thread objects and results, data count, and an args copy
        running_threads = []
        data_count = len(args[arg_data_index])

        # set number of threads to use: specified, CPU core count, or data count (to prevent use of excess resources)
        if n_threads == 0:
            n_threads = multiprocessing.cpu_count()
        if data_count / n_threads <= 1:
            n_threads = data_count

        # split data by number of threads (works with DataFrames)
        data = [x.tolist() for x in numpy.array_split(args[arg_data_index], n_threads)]

        # spool up new threads
        for i in range(n_threads):
            # initialise thread ID, thread arg and thread object
            thread_id = i + 1  # Thread 0 handles the additional threads, so start at index 1
            thread_args = copy.deepcopy(args)
            thread_args[arg_data_index] = copy.deepcopy(data[i])
            thread = MyThread(thread_id, f"Thread-{thread_id}", func, thread_args, self.logger, arg_data_index)

            # terminate daemon threads if the host process terminates
            thread.daemon = True

            # keep track of running threads for future joining and start
            running_threads.append(thread)
            thread.start()

        return self.__get_results_from_threads(running_threads)
