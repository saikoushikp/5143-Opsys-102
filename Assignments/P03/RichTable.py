from rich.table import Table
from rich.live import Live
import time
from rich.console import Console

class RichTable:
    def __init__(self):
        self.terminal_width = Console().width
        self.live = Live(self.generate_table([], [], [], [], [], []), refresh_per_second=500)
        self.live.start()
        self.new = []
        self.ready = []
        self.running = []
        self.waiting = []
        self.io = []
        self.exit = []

    def update(self, new, ready, running, waiting, io, exit):
        self.new = new
        self.ready = ready
        self.running = running
        self.waiting = waiting
        self.io = io
        self.exit = exit


    def show_tables(self, new, ready, running, waiting, io, exit):
        self.live.update(self.generate_table(new, ready, running, waiting, io, exit))
        time.sleep(0.05)
        
    def show_message(self,message):

        table = self.generate_table(self.new, self.ready, self.running, self.waiting, self.io, self.exit)
        table.add_row("Message", message, style="bold green", end_section=False)
        self.live.update(table)
        time.sleep(0.05)

    def make_row(self, queueName, queue):
        processes = ""
        for pcb in queue:
            processes += str(f"[bold][[/bold][bold blue]{pcb.pid} {pcb.priority}[/bold blue][bold]][/bold]")
        return [queueName, processes]
    

    def generate_table(self, new, ready, running, waiting, io, exit):
        self.new = new
        self.ready = ready
        self.running = running
        self.waiting = waiting
        self.io = io
        self.exit = exit

        # Create the table
        table = Table(show_header=False)
        #table.add_column("Queue", style="bold yellow on blue dim", width=int(terminal_width*.1))
        table.add_column("Queue", style="bold red", width=int(self.terminal_width*.1))
        table.add_column("Processes", width=int(self.terminal_width*.9))
        table.add_row(*self.make_row("New", new), end_section=True)
        table.add_row(*self.make_row("Ready", ready), end_section=True)
        table.add_row(*self.make_row("Running", running), end_section=True)
        table.add_row(*self.make_row("Waiting", waiting), end_section=True)
        table.add_row(*self.make_row("Peripheral", io), end_section=True)
        table.add_row(*self.make_row("Exit", exit), end_section=True)

        return table

