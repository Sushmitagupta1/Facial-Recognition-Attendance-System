import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os

class StudentDialog:
    def __init__(self, parent):
        self.dialog = Toplevel(parent)
        self.dialog.title("Student Details")
        
        # Center dialog on screen
        window_width = 400
        window_height = 400  # Increased height for better spacing
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create main frame with padding
        main_frame = Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Style
        label_font = ('Arial', 12)
        entry_font = ('Arial', 12)
        padding = 10
        
        # Student Name
        Label(main_frame, text="Student Name:", font=label_font).pack(pady=(0, 5))
        self.name_entry = Entry(main_frame, font=entry_font, width=30)
        self.name_entry.pack(pady=(0, padding))
        
        # Student Code
        Label(main_frame, text="Student Code:", font=label_font).pack(pady=(0, 5))
        self.code_entry = Entry(main_frame, font=entry_font, width=30)
        self.code_entry.pack(pady=(0, padding))
        
        # Branch Name
        Label(main_frame, text="Branch Name:", font=label_font).pack(pady=(0, 5))
        self.branch_entry = Entry(main_frame, font=entry_font, width=30)
        self.branch_entry.pack(pady=(0, padding))
        
        # Session
        Label(main_frame, text="Session:", font=label_font).pack(pady=(0, 5))
        self.session_entry = Entry(main_frame, font=entry_font, width=30)
        self.session_entry.pack(pady=(0, padding))
        
        # Button frame for multiple buttons
        button_frame = Frame(main_frame)
        button_frame.pack(pady=(20, 0))
        
        # Submit Button
        submit_btn = Button(button_frame, 
                          text="Submit & Start Capture",
                          command=self.submit,
                          bg='#007bff',
                          fg='white',
                          font=('Arial', 12, 'bold'),
                          padx=20,
                          pady=10,
                          relief=RAISED,
                          cursor='hand2')  # Hand cursor on hover
        submit_btn.pack(side=LEFT, padx=5)
        
        # Cancel Button
        cancel_btn = Button(button_frame,
                          text="Cancel",
                          command=self.dialog.destroy,
                          bg='#dc3545',
                          fg='white',
                          font=('Arial', 12, 'bold'),
                          padx=20,
                          pady=10,
                          relief=RAISED,
                          cursor='hand2')
        cancel_btn.pack(side=LEFT, padx=5)
        
        # Bind enter key to submit
        self.dialog.bind('<Return>', lambda e: self.submit())
        
        # Set initial focus to name entry
        self.name_entry.focus()
        
        self.result = None

    def submit(self):
        if not all([self.name_entry.get(), self.code_entry.get(), 
                   self.branch_entry.get(), self.session_entry.get()]):
            messagebox.showerror("Error", "All fields are required!")
            return
            
        self.result = {
            'name': self.name_entry.get(),
            'code': self.code_entry.get(),
            'branch': self.branch_entry.get(),
            'session': self.session_entry.get()
        }
        self.dialog.destroy()

class AdminVerification:
    def __init__(self, parent, callback):
        self.dialog = Toplevel(parent)
        self.dialog.title("Admin Verification")
        self.callback = callback
        
        # Set fixed size and center
        window_width = 400
        window_height = 400
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.dialog.resizable(False, False)
        
        # Main Frame
        main_frame = Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Heading
        heading = Label(main_frame, text="ADMIN PANEL", font=('Arial', 20, 'bold underline'))
        heading.pack(pady=20)
        
        # User ID
        Label(main_frame, text="User ID:", font=('Arial', 12)).pack(pady=(20,5))
        self.userid_entry = Entry(main_frame, font=('Arial', 12), width=30)
        self.userid_entry.pack()
        
        # Password
        Label(main_frame, text="Password:", font=('Arial', 12)).pack(pady=(20,5))
        self.password_entry = Entry(main_frame, font=('Arial', 12), width=30, show="*")
        self.password_entry.pack()
        
        # Warning text
        Label(main_frame, text="* Authorized Person Only", fg="red", font=('Arial', 10, 'italic')).pack(pady=(20,10))
        
        # Submit Button
        Button(main_frame, text="Submit", command=self.verify, bg='#007bff', fg='white',
               font=('Arial', 12, 'bold'), padx=20, pady=5).pack(pady=10)
        
        # Center dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
    def verify(self):
        if (self.userid_entry.get() == "KRISHKRKASHYAP" and 
            self.password_entry.get() == "Bwu145"):
            self.dialog.destroy()
            self.callback(True)
        else:
            messagebox.showerror("Error", "Invalid credentials!")
            self.callback(False)

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        
        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Set window size to full screen
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        # Load and resize background image
        try:
            bg_image = Image.open("bg_main.png")
            bg_image = bg_image.resize((screen_width, screen_height))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            # Create canvas for background
            self.canvas = Canvas(root, width=screen_width, height=screen_height)
            self.canvas.pack(fill="both", expand=True)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            
            # Button styles
            button_width = 20
            button_height = 2
            button_font = ('Arial', 36, 'bold')
            self.button_bg = '#007bff'  # Default blue color
            self.hover_bg = '#0056b3'   # Darker blue for hover
            button_fg = 'white'
            
            # Create custom style for buttons
            buttons_data = [
                ("ADD STUDENT", self.open_add_student),
                ("TAKE ATTENDANCE", self.open_take_attendance),
                ("SHOW ATTENDANCE", self.open_attendance_folder)
            ]
            
            # Calculate vertical positions for buttons (centered)
            center_y = screen_height // 2
            spacing = 150  # Space between buttons
            button_y_positions = [center_y - spacing, center_y, center_y + spacing]
            
            self.buttons = []  # Store button references
            
            # Create and place buttons
            for i, (text, command) in enumerate(buttons_data):
                btn = Button(root, 
                           text=text,
                           width=button_width,
                           height=button_height,
                           font=button_font,
                           bg=self.button_bg,
                           fg=button_fg,
                           command=command,
                           relief=RAISED,
                           cursor='hand2',
                           activebackground=self.hover_bg,
                           activeforeground='white')
                
                # Bind hover events
                btn.bind('<Enter>', lambda e, btn=btn: self.on_hover(btn))
                btn.bind('<Leave>', lambda e, btn=btn: self.on_leave(btn))
                
                # Add pulsing effect
                self.buttons.append(btn)
                self.canvas.create_window(screen_width//2, button_y_positions[i], 
                                       window=btn)
                
            # Start button animation
            self.animate_buttons()
            
        except Exception as e:
            print(f"Error loading background image: {e}")
            exit(1)

    def on_hover(self, button):
        """Handle mouse hover event"""
        button.configure(bg=self.hover_bg)
        # Scale up the button slightly
        button.configure(font=('Arial', 38, 'bold'))

    def on_leave(self, button):
        """Handle mouse leave event"""
        button.configure(bg=self.button_bg)
        # Return to original size
        button.configure(font=('Arial', 36, 'bold'))

    def animate_buttons(self):
        """Create a subtle pulsing animation for buttons"""
        colors = ['#007bff', '#0056b3', '#004085', '#0056b3']
        current_color = 0
        
        def pulse():
            nonlocal current_color
            for btn in self.buttons:
                if not btn.winfo_exists():
                    return
                btn.configure(bg=colors[current_color])
            current_color = (current_color + 1) % len(colors)
            self.root.after(1000, pulse)  # Change color every 1000ms
        
        pulse()

    def open_add_student(self):
        def after_verification(success):
            if success:
                dialog = StudentDialog(self.root)
                self.root.wait_window(dialog.dialog)
                if dialog.result:
                    with open('temp_student_details.txt', 'w') as f:
                        f.write(f"{dialog.result['name']}\n")
                        f.write(f"{dialog.result['code']}\n")
                        f.write(f"{dialog.result['branch']}\n")
                        f.write(f"{dialog.result['session']}\n")
                    subprocess.run(["python", "add_faces.py"])
                    if os.path.exists('temp_student_details.txt'):
                        os.remove('temp_student_details.txt')
        
        AdminVerification(self.root, after_verification)

    def open_take_attendance(self):
        subprocess.run(["python", "test.py"])

    def open_attendance_folder(self):
        def after_verification(success):
            if success:
                attendance_path = os.path.join(os.getcwd(), "Attendance")
                os.startfile(attendance_path)
        
        AdminVerification(self.root, after_verification)

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()