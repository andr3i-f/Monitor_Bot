import monitors.ShopifyMonitor as ShopifyMonitor
import monitors.SupremeMonitor as SupremeMonitor
import monitors.FootLockerMonitor as FootLockerMonitor
import monitors.SNKRSMonitor as SNKRSMonitor
import monitor_threading
import webhooks
import json
import time
import datetime

def main():
    # Initiate everything, make sure everything is OK
    active_monitors_names = []
    shopify_monitors = []
    nike_snkrs_monitors = []

    notify_webhooks = webhooks.DiscordNotify()

    with open('config/keywords.json') as f:  # Get the keywords that the monitors will use
        keywords = json.load(f)
    
    with open('config/unwanted.json') as f:  # Get all the black-listed keywords that monitors will use
        unwanted = json.load(f)

    with open('config/shopify_websites.json') as f:  # Get all the shopify websites to monitor 
        websites = json.load(f) 

    for website in websites:  # Create objects for all shopify monitors
        shopify_monitors.append(
            ShopifyMonitor.Monitor(
                website['link'],
                website['name'],
                website['collections'],
                keywords,
                unwanted,
                notify_webhooks,
                3
            )
        )
    

    # Manually add Supreme Monitor
    Supreme = SupremeMonitor.SupremeMonitor(
        "Supreme",
        notify_webhooks,
        10
    )

    # Manually add SNKRS Monitor
    SNKRS = SNKRSMonitor.SNKRSMonitor(
            "SNKRS",
            notify_webhooks,
            keywords,
            3
    )
    nike_snkrs_monitors.append(SNKRS)

    # Fix Footlocker Monitor Before Adding

    # Get all current monitor names
    active_monitors_names = [s.name for s in shopify_monitors]
    active_monitors_names.append(Supreme.name)
    active_monitors_names.append(SNKRS.name)

    main_loop(active_monitors_names, notify_webhooks, shopify_monitors, nike_snkrs_monitors, Supreme, "footlocker")


def main_loop(monitor_names, notify_webhooks, ShopifyMonitors, NikeSNKRSMonitors, SupremeMonitor, FootlockerMonitor2):
    monitor_threads = monitor_threading.monitor_thread(ShopifyMonitors, NikeSNKRSMonitors, SupremeMonitor, "Footlocker")
    print("WELCOME TO A1 MONITORS")
    print("Current Monitors: ")
    print(monitor_names)
    print(" enter 'q' to exit , enter '1' to start, enter '2' to stop")

    start = time.time()
    
    while True:
        x = 'nothing'
        x = input(" do you want to exit? ")

        if x == 'q':
            break

        if x == '1':
            print("STATUS: RUNNING")
            update_log_start(notify_webhooks)
            monitor_threads.Start()
            
        
        if x == '2':
            print("STATUS: STOPPING")
            update_log_end(notify_webhooks, start)
            monitor_threads.Stop()
        

def update_log_start(webhook_bot):
    log = "```"
    log += f"Setting up at: \n{datetime.datetime.now()}"
    log += "```"
    webhook_bot.update_log(log)

def update_log_end(webhook_bot, start):
    end = time.time()
    log = "```"
    log += f'Ending task at: \n{datetime.datetime.now()} \nRan for {end - start} seconds.'
    log += "```"
    webhook_bot.update_log(log)

if __name__ == "__main__":
    main()