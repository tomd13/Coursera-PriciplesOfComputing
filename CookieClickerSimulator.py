"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor

codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0


class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self.time = 0.0
        self.cookies = 0.0
        self.total_cookies = 0.0
        self.cps = 1.0
        self.history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        return ("\nTotal cookies: " + str(self.total_cookies) +
                "\nCurrent cookies: " + str(self.get_cookies()) +
                "\nCPS: " + str(self.get_cps()) +
                "\nTime: " + str(self.get_time()))

    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)

        Should return a float
        """
        return self.cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self.cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self.time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self.history[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self.cookies:
            return float(0)
        else:
            return math.ceil((cookies - self.cookies) / self.cps)

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self.time += time
            self.cookies += time * self.cps
            self.total_cookies += time * self.cps
        else:
            return

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self.cookies >= cost:
            self.cookies -= cost
            self.cps += additional_cps
            self.history.append((self.time, item_name, cost, self.total_cookies))
        else:
            return

    def print_history(self):
        """
        Prints the entire history
        """
        for item in self.history:
            print(item)


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    build_info_clone = build_info.clone()
    state = ClickerState()
    while state.get_time() <= duration:
        remaining_time = duration - state.get_time()
        new_item = strategy(state.get_cookies(), state.get_cps(), state.get_history(), +
        remaining_time, build_info_clone)
        if new_item == None:
            state.wait(remaining_time)
            break
        cost = build_info_clone.get_cost(new_item)
        new_item_time = state.time_until(cost)
        if new_item_time > remaining_time:
            state.wait(remaining_time)
            break
        else:
            state.wait(new_item_time)
            state.buy_item(new_item, cost, build_info_clone.get_cps(new_item))
            build_info_clone.update_item(new_item)

    # state.print_history()
    return state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None


def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    new_item_cost = float("inf")
    for potential_item in build_info.build_items():
        item_cost = build_info.get_cost(potential_item)
        if item_cost <= (cookies + cps * time_left):
            if item_cost < new_item_cost:
                new_item_cost = item_cost
                new_item = potential_item

    if new_item_cost == float("inf"):
        return None
    else:
        return new_item


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    new_item_cost = 0
    for potential_item in build_info.build_items():
        item_cost = build_info.get_cost(potential_item)
        if item_cost <= (cookies + cps * time_left):
            if item_cost > new_item_cost:
                new_item_cost = item_cost
                new_item = potential_item

    if new_item_cost == 0:
        return None
    else:
        return new_item


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    item_value = 0
    for item in build_info.build_items():
        item_cps = build_info.get_cps(item)
        item_cost = build_info.get_cost(item)
        new_item_value = item_cps / item_cost
        if new_item_value > item_value:
            item_value = new_item_value
            best_item = item
            best_item_cost = build_info.get_cost(best_item)
            best_item_cps = build_info.get_cps(best_item)

    if time_left > (best_item_cost / best_item_cps):
        return best_item
    else:
        return None


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print
    strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)
    # state.print_history()


def run():
    """
    Run the simulator.
    """
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)


run()

