import tkinter as tk
from tkinter import ttk, messagebox
import time

class CPUScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Algorithms Simulator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        self.processes = []
        self.current_algorithm = tk.StringVar(value="FCFS")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="CPU Scheduling Simulator", 
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(pady=10)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Input
        input_frame = tk.LabelFrame(
            main_frame, 
            text="Process Input", 
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=10,
            pady=10
        )
        input_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Algorithm selection
        algo_frame = tk.Frame(input_frame, bg="#ffffff")
        algo_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            algo_frame, 
            text="Algorithm:", 
            font=("Arial", 10),
            bg="#ffffff"
        ).pack(side=tk.LEFT, padx=5)
        
        algorithms = ["FCFS", "SJF", "Round Robin"]
        algo_menu = ttk.Combobox(
            algo_frame, 
            textvariable=self.current_algorithm,
            values=algorithms,
            state="readonly",
            width=15
        )
        algo_menu.pack(side=tk.LEFT, padx=5)
        algo_menu.bind("<<ComboboxSelected>>", lambda e: self.update_input_fields())
        
        # Process input fields
        self.fields_frame = tk.Frame(input_frame, bg="#ffffff")
        self.fields_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            self.fields_frame, 
            text="Process ID:", 
            font=("Arial", 10),
            bg="#ffffff"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.pid_entry = tk.Entry(self.fields_frame, width=15)
        self.pid_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.arrival_label = tk.Label(
            self.fields_frame, 
            text="Arrival Time:", 
            font=("Arial", 10),
            bg="#ffffff"
        )
        self.arrival_entry = tk.Entry(self.fields_frame, width=15)
        
        tk.Label(
            self.fields_frame, 
            text="Burst Time:", 
            font=("Arial", 10),
            bg="#ffffff"
        ).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.burst_entry = tk.Entry(self.fields_frame, width=15)
        self.burst_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Hide arrival time initially (for FCFS and SJF)
        self.update_input_fields()
        
        # Buttons
        button_frame = tk.Frame(input_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(
            button_frame,
            text="Add Process",
            command=self.add_process,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_processes,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Run Simulation",
            command=self.run_simulation,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Process list
        list_frame = tk.LabelFrame(
            input_frame, 
            text="Added Processes", 
            font=("Arial", 10, "bold"),
            bg="#ffffff"
        )
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.process_listbox = tk.Listbox(list_frame, height=10, font=("Courier", 9))
        self.process_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right panel - Visualization
        viz_frame = tk.LabelFrame(
            main_frame, 
            text="Process Execution Visualization", 
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=10,
            pady=10
        )
        viz_frame.grid(row=0, column=1, sticky="nsew")
        
        # Canvas for Gantt chart
        canvas_frame = tk.Frame(viz_frame, bg="#ffffff")
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(
            canvas_frame, 
            bg="white", 
            height=200,
            highlightthickness=1,
            highlightbackground="#ccc"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Results table
        results_frame = tk.LabelFrame(
            viz_frame, 
            text="Results", 
            font=("Arial", 10, "bold"),
            bg="#ffffff"
        )
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create Treeview for results
        columns = ("PID", "Burst", "Waiting", "Turnaround")
        self.results_tree = ttk.Treeview(
            results_frame, 
            columns=columns, 
            show="headings",
            height=8
        )
        
        column_headings = {
            "PID": "Process ID",
            "Burst": "Burst Time",
            "Waiting": "Waiting Time",
            "Turnaround": "Turnaround Time"
        }
        
        for col in columns:
            self.results_tree.heading(col, text=column_headings[col])
            self.results_tree.column(col, width=120, anchor="center")
        
        self.results_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Average times - Make it more visible
        avg_container = tk.Frame(results_frame, bg="#e3f2fd", relief=tk.SOLID, borderwidth=1)
        avg_container.pack(fill=tk.X, padx=5, pady=10)
        
        self.avg_label = tk.Label(
            avg_container,
            text="Run simulation to see average times",
            font=("Arial", 11, "bold"),
            bg="#e3f2fd",
            fg="#1976D2",
            pady=10
        )
        self.avg_label.pack()
        
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
    
    def update_input_fields(self):
        """Update input fields based on selected algorithm"""
        algorithm = self.current_algorithm.get()
        
        # Hide arrival time for all algorithms
        self.arrival_label.grid_forget()
        self.arrival_entry.grid_forget()
    
    def add_process(self):
        try:
            pid = self.pid_entry.get().strip()
            burst = int(self.burst_entry.get().strip())
            
            if not pid:
                messagebox.showerror("Error", "Process ID cannot be empty!")
                return
            
            if burst <= 0:
                messagebox.showerror("Error", "Invalid burst time!")
                return
            
            # For FCFS and SJF, arrival time is the order of entry (0, 1, 2, ...)
            # For Round Robin, all processes arrive at time 0
            arrival = len(self.processes)
            
            process = {
                'pid': pid,
                'arrival': arrival,
                'burst': burst,
                'remaining': burst
            }
            
            self.processes.append(process)
            self.update_process_list()
            
            # Clear entries
            self.pid_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
    
    def update_process_list(self):
        self.process_listbox.delete(0, tk.END)
        for p in self.processes:
            self.process_listbox.insert(
                tk.END, 
                f"PID: {p['pid']:<10} | Burst: {p['burst']:<3}"
            )
    
    def clear_processes(self):
        self.processes = []
        self.update_process_list()
        self.canvas.delete("all")
        self.results_tree.delete(*self.results_tree.get_children())
        self.avg_label.config(text="")
    
    def run_simulation(self):
        if not self.processes:
            messagebox.showerror("Error", "Please add at least one process!")
            return
        
        algorithm = self.current_algorithm.get()
        
        if algorithm == "FCFS":
            self.fcfs()
        elif algorithm == "SJF":
            self.sjf()
        elif algorithm == "Round Robin":
            # Ask for time quantum in a dialog
            quantum = self.ask_time_quantum()
            if quantum is not None:
                self.round_robin(quantum)
    
    def ask_time_quantum(self):
        """Show dialog to ask for time quantum"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Time Quantum")
        dialog.geometry("300x150")
        dialog.configure(bg="#ffffff")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (300 // 2)
        y = (dialog.winfo_screenheight() // 2) - (150 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        result = {'quantum': None}
        
        # Label
        tk.Label(
            dialog,
            text="Enter Time Quantum for Round Robin:",
            font=("Arial", 11),
            bg="#ffffff"
        ).pack(pady=20)
        
        # Entry
        quantum_entry = tk.Entry(dialog, width=15, font=("Arial", 11))
        quantum_entry.pack(pady=10)
        quantum_entry.insert(0, "2")
        quantum_entry.focus()
        
        def on_ok():
            try:
                quantum = int(quantum_entry.get())
                if quantum <= 0:
                    raise ValueError
                result['quantum'] = quantum
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive integer!")
        
        def on_cancel():
            dialog.destroy()
        
        # Buttons
        button_frame = tk.Frame(dialog, bg="#ffffff")
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="OK",
            command=on_ok,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            width=10,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=on_cancel,
            bg="#757575",
            fg="white",
            font=("Arial", 10, "bold"),
            width=10,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to OK
        quantum_entry.bind("<Return>", lambda e: on_ok())
        
        dialog.wait_window()
        return result['quantum']
    
    def fcfs(self):
        # Process in order of entry (arrival time is the order)
        processes = sorted(self.processes, key=lambda x: x['arrival'])
        
        current_time = 0
        gantt_chart = []
        results = []
        
        for p in processes:
            start_time = current_time
            completion_time = current_time + p['burst']
            turnaround_time = completion_time
            waiting_time = turnaround_time - p['burst']
            
            gantt_chart.append({
                'pid': p['pid'],
                'start': start_time,
                'end': completion_time
            })
            
            results.append({
                'pid': p['pid'],
                'arrival': 0,  # Not shown in output
                'burst': p['burst'],
                'completion': completion_time,
                'turnaround': turnaround_time,
                'waiting': waiting_time
            })
            
            current_time = completion_time
        
        self.draw_gantt_chart(gantt_chart)
        self.display_results(results, sort_by_pid=True)
    
    def sjf(self):
        # All processes are available at time 0, sort by burst time
        processes = sorted(self.processes, key=lambda x: (x['burst'], x['pid']))
        
        current_time = 0
        gantt_chart = []
        results = []
        
        for p in processes:
            start_time = current_time
            completion_time = current_time + p['burst']
            turnaround_time = completion_time
            waiting_time = turnaround_time - p['burst']
            
            gantt_chart.append({
                'pid': p['pid'],
                'start': start_time,
                'end': completion_time
            })
            
            results.append({
                'pid': p['pid'],
                'arrival': 0,  # Not shown in output
                'burst': p['burst'],
                'completion': completion_time,
                'turnaround': turnaround_time,
                'waiting': waiting_time
            })
            
            current_time = completion_time
        
        self.draw_gantt_chart(gantt_chart)
        self.display_results(results, sort_by_pid=False)  # Show in execution order (SJF order)
    
    def round_robin(self, quantum):
        # All processes arrive at time 0
        processes = [p.copy() for p in self.processes]
        for p in processes:
            p['remaining'] = p['burst']
        
        current_time = 0
        gantt_chart = []
        queue = processes.copy()
        completed = []
        
        while queue:
            current_process = queue.pop(0)
            
            # Execute process
            execution_time = min(quantum, current_process['remaining'])
            start_time = current_time
            current_time += execution_time
            current_process['remaining'] -= execution_time
            
            gantt_chart.append({
                'pid': current_process['pid'],
                'start': start_time,
                'end': current_time
            })
            
            # Check if process is completed
            if current_process['remaining'] == 0:
                completion_time = current_time
                turnaround_time = completion_time
                waiting_time = turnaround_time - current_process['burst']
                
                completed.append({
                    'pid': current_process['pid'],
                    'arrival': 0,  # Not shown in output
                    'burst': current_process['burst'],
                    'completion': completion_time,
                    'turnaround': turnaround_time,
                    'waiting': waiting_time
                })
            else:
                # Add back to queue
                queue.append(current_process)
        
        self.draw_gantt_chart(gantt_chart)
        self.display_results(completed, sort_by_pid=True)
    
    def draw_gantt_chart(self, gantt_chart):
        self.canvas.delete("all")
        
        if not gantt_chart:
            return
        
        # Calculate dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 200
        
        margin = 50
        chart_height = 60
        y_start = (canvas_height - chart_height) // 2
        
        total_time = max([item['end'] for item in gantt_chart])
        available_width = canvas_width - 2 * margin
        time_scale = available_width / total_time if total_time > 0 else 1
        
        # Colors for different processes
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
                  '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B88B', '#AAB7B8']
        pid_colors = {}
        
        # Draw Gantt chart
        for i, item in enumerate(gantt_chart):
            if item['pid'] not in pid_colors:
                pid_colors[item['pid']] = colors[len(pid_colors) % len(colors)]
            
            x1 = margin + item['start'] * time_scale
            x2 = margin + item['end'] * time_scale
            
            # Draw rectangle
            self.canvas.create_rectangle(
                x1, y_start, x2, y_start + chart_height,
                fill=pid_colors[item['pid']],
                outline="black",
                width=2
            )
            
            # Draw process ID
            self.canvas.create_text(
                (x1 + x2) / 2, y_start + chart_height / 2,
                text=item['pid'],
                font=("Arial", 10, "bold"),
                fill="white"
            )
            
            # Draw start time
            if i == 0 or gantt_chart[i-1]['end'] != item['start']:
                self.canvas.create_text(
                    x1, y_start + chart_height + 15,
                    text=str(item['start']),
                    font=("Arial", 9)
                )
            
            # Draw end time
            if i == len(gantt_chart) - 1 or gantt_chart[i+1]['start'] != item['end']:
                self.canvas.create_text(
                    x2, y_start + chart_height + 15,
                    text=str(item['end']),
                    font=("Arial", 9)
                )
        
        # Draw title
        self.canvas.create_text(
            canvas_width / 2, 20,
            text=f"Gantt Chart - {self.current_algorithm.get()}",
            font=("Arial", 12, "bold"),
            fill="#333"
        )
    
    def display_results(self, results, sort_by_pid=True):
        # Clear previous results
        self.results_tree.delete(*self.results_tree.get_children())
        
        # Sort by process ID for display (except for SJF which is already in execution order)
        if sort_by_pid:
            results.sort(key=lambda x: x['pid'])
        
        total_turnaround = 0
        total_waiting = 0
        
        for r in results:
            self.results_tree.insert(
                "",
                tk.END,
                values=(
                    r['pid'],
                    r['burst'],
                    r['waiting'],
                    r['turnaround']
                )
            )
            total_turnaround += r['turnaround']
            total_waiting += r['waiting']
        
        n = len(results)
        avg_turnaround = total_turnaround / n
        avg_waiting = total_waiting / n
        
        self.avg_label.config(
            text=f"Average Waiting Time: {avg_waiting:.2f}  |  Average Turnaround Time: {avg_turnaround:.2f}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = CPUScheduler(root)
    root.mainloop()
