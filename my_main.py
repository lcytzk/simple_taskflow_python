import threading
import os
from name_to_cmd import name_to_cmd
from parent_to_children import parent_to_children

threads = []
child_to_parents = {}
children_num = {}

class Task(threading.Thread):

    def __init__(self, name, parents) :
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.name = name
        self.parents = parents

    def self_finish(self) :
        for p in self.parents :
            children_num[p] -= 1
            if children_num[p] == 0:
                task = Task(p, child_to_parents[p])
                threads.append(task)
                task.start()

    def run(self) :
        os.system(name_to_cmd[self.name])
        print self.name+" finish"
        self.self_finish()


def do_main() :

    for p_key in name_to_cmd :
        child_to_parents[p_key] = {}
        children_num[p_key] = 0
    for p_key in parent_to_children :
        children_num[p_key] = len(parent_to_children[p_key])
        for child in parent_to_children[p_key] :
            child_to_parents[child][p_key] = True
#    print children_num
#    print child_to_parents
    exec_queue = []
    for t in children_num :
        if children_num[t] == 0 :
            exec_queue.append(t)
    
    for t in exec_queue :
        task = Task(t, child_to_parents[t])
        threads.append(task)
        task.start()

    for t in threads:
        t.join()

if __name__ == "__main__" :
    do_main()