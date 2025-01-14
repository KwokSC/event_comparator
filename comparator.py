import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd


class AcceptanceTestComparatorApp:
    def __init__(self, root):
        self.report_status = None
        self.result_tree = None
        self.root = root
        self.root.title("大数据埋点验收测试比对")
        self.root.geometry("800x600")
        # Configure root window's row weights for top 40% layout
        self.root.grid_rowconfigure(0, weight=4)  # Top section (40%)
        self.root.grid_rowconfigure(1, weight=6)  # Bottom section (60%)
        self.root.grid_columnconfigure(0, weight=1)  # Center content horizontally

        # File paths
        self.file1_path = tk.StringVar()
        self.file2_path = tk.StringVar()

        # Vehicle Model
        self.vehicle_model = None

        # GUI Layout
        self.create_widgets()

    def create_widgets(self):

        # Create a StringVar to hold the label's text
        self.report_status = tk.StringVar()
        self.report_status.set("已上报: Unknown，未上报：Unknown，上报率：Unknown")  # Initial value

        # Frame to hold the file selection widgets
        selection_frame = tk.Frame(self.root)
        selection_frame.grid(row=0, column=0, sticky="nsew")  # Top section

        # Configure the frame for centering
        selection_frame.grid_rowconfigure(0, weight=1)
        selection_frame.grid_rowconfigure(1, weight=1)
        selection_frame.grid_columnconfigure(0, weight=1)

        # Event List Selection
        tk.Label(selection_frame, text="请选择冻结埋点清单:").grid(row=0, column=0, padx=0, pady=0)
        tk.Entry(selection_frame, textvariable=self.file1_path, width=50).grid(row=0, column=1, padx=10, pady=0)
        tk.Button(selection_frame, text="Browse", command=self.browse_file1).grid(row=0, column=2, padx=10, pady=0)

        # Acceptance Test Selection
        tk.Label(selection_frame, text="请选择验收测试记录:").grid(row=1, column=0, padx=0, pady=0)
        tk.Entry(selection_frame, textvariable=self.file2_path, width=50).grid(row=1, column=1, padx=10, pady=0)
        tk.Button(selection_frame, text="Browse", command=self.browse_file2).grid(row=1, column=2, padx=10, pady=0)

        # Compare Button
        tk.Button(selection_frame, text="下一步", command=self.select_vehicle_model).grid(row=2, column=1, pady=20)

        # Frame for Treeview and Scrollbars
        report_area = tk.Frame(self.root)
        report_area.grid(row=1, column=0, columnspan=2, padx=0, pady=0)

        # Result Display
        self.result_tree = ttk.Treeview(report_area, columns=("Code", "Primary Function", "Secondary Function",
                                                            "Tertiary Function", "Value", "Event Name", "Event Code",
                                                            "Attribute Name", "Attribute Code", "Data Type",
                                                            "Data Format"), show='headings')
        self.result_tree.heading("Code", text="编码")
        self.result_tree.heading("Primary Function", text="一级功能")
        self.result_tree.heading("Secondary Function", text="二级功能")
        self.result_tree.heading("Tertiary Function", text="二级功能")
        self.result_tree.heading("Tertiary Function", text="二级功能")
        self.result_tree.heading("Value", text="数值")
        self.result_tree.heading("Event Name", text="事件名称")
        self.result_tree.heading("Event Code", text="事件编码")
        self.result_tree.heading("Attribute Name", text="属性名称")
        self.result_tree.heading("Attribute Code", text="属性编码")
        self.result_tree.heading("Data Type", text="数据类型")
        self.result_tree.heading("Data Format", text="数据格式")

        # Scrollbars
        vsb = ttk.Scrollbar(report_area, orient="vertical", command=self.result_tree.yview)
        hsb = ttk.Scrollbar(report_area, orient="horizontal", command=self.result_tree.xview)

        self.result_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Layout: Treeview and Scrollbars
        self.result_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        report_area.grid_rowconfigure(0, weight=1)
        report_area.grid_columnconfigure(0, weight=1)

        # Create a Label linked to the StringVar
        tk.Label(report_area, textvariable=self.report_status).grid(row=2, column=0, padx=0, pady=0)

    def browse_file1(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            self.file1_path.set(file_path)

    def browse_file2(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.file2_path.set(file_path)

    def select_vehicle_model(self):
        try:
            if not self.file1_path.get() or not self.file2_path.get():
                messagebox.showerror("Error", "请上传文件")
                return

            popup = tk.Toplevel(self.root)  # Create a new window
            popup.title("请选择打点车型")
            popup.geometry("300x200")

            label = tk.Label(popup, text="This is a popup!", font=("Arial", 14))
            label.pack(pady=20)

            close_button = tk.Button(popup, text="Close", command=popup.destroy)
            close_button.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def compare_files(self):
        try:
            event_list = pd.read_excel(self.file1_path.get(), sheet_name=None)
            test_record = pd.read_csv(self.file2_path.get())
            check_list = ['NO TEST'] * len(event_list)
            failed_list = []

            if len(event_list) > 1:
                messagebox.showerror("Error", "请确保上传的表格仅有一个工作簿")
                return

            self.result_tree.delete(*self.result_tree.get_children())  # Clear previous results

            # Extract Code and Event Code and make them tuple
            event_list_tuple = event_list[['编码', '事件编码']].apply(tuple, axis=1)
            test_record_tuple = test_record[['功能ID', '事件编码']].apply(tuple, axis=1)

            # TODO: Implement compare logics


            uploaded_counts = 0
            failed_counts = 0
            upload_ratio = 0

            self.report_status.set(f"已上报: {uploaded_counts}，未上报：{failed_counts}，上报率：{upload_ratio}")

            messagebox.showinfo("Completed", "Comparison Completed!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = AcceptanceTestComparatorApp(root)
    root.mainloop()
