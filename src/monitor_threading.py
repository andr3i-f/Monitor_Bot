import threading
import time


class monitor_thread:
    def __init__(self, ShopifyMonitors, NikeSNKRSMonitors, SupremeMonitor, FootlockerMonitor):
        self.Shopify_Monitors = ShopifyMonitors
        self.NikeSNKRS_Monitors = NikeSNKRSMonitors
        self.Supreme_Monitor = SupremeMonitor
        self.Footlocker_Monitor = FootlockerMonitor

        self.Shopify = threading.Thread(target=self.ShopifyThread)
        self.NikeSNKRS = threading.Thread(target=self.Nike_SNKRS_Thread)
        self.Supreme = threading.Thread(target=self.Supreme_Thread)
        #Footlocker = threading.Thread()

        self.stop_event = threading.Event()

    def ShopifyThread(self):
     
        while not self.stop_event.is_set():
            for shopify_monitor in self.Shopify_Monitors:
                shopify_monitor.search_wanted_items()
                #print(f" done with {shopify_monitor.name} \n")


        print(f" exiting Shopify thread ")

    def Nike_SNKRS_Thread(self):

        while not self.stop_event.is_set():
            for nike_monitor in self.NikeSNKRS_Monitors:
                nike_monitor.search_wanted_items()
                #print(f" done with {nike_monitor.name} \n")


        print(f" exiting NIKE/SNKRS thread ")


    def Supreme_Thread(self):

        while not self.stop_event.is_set():
            self.Supreme_Monitor.search_wanted_items()
            #print(f" done with {self.Supreme_Monitor.name} \n")

        print(f" exiting Supreme thread ")


    def Footlocker_Thread(self):
        pass

    def Start(self):
        self.Shopify.start()
        self.NikeSNKRS.start()
        self.Supreme.start()

    def Stop(self):
        self.stop_event.set()


def main():
    monitor_thread(1,2,3,4)

if __name__ == "__main__":
    main()