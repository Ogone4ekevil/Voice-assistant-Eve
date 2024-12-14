import tkinter as tk
from tkinter import ttk, messagebox
from queue import Queue, Empty
import threading
from eva_core import speak, listen_and_process, execute_command, load_commands, save_commands
import traceback

def add_command():
    new_command = entry_command.get()
    new_action = entry_action.get()
    if new_command and new_action:
        commands[new_command] = new_action
        update_list()
        save_commands(commands)
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните оба поля.")
    entry_command.delete(0, tk.END)
    entry_action.delete(0, tk.END)

def delete_command():
    selected_item = command_list.curselection()
    if selected_item:
        command = command_list.get(selected_item[0])
        del commands[command]
        update_list()
        save_commands(commands)
    else:
         messagebox.showerror("Ошибка", "Пожалуйста, выберите команду для удаления.")

def update_list():
    command_list.delete(0, tk.END)
    for command in commands.keys():
        command_list.insert(tk.END, command)

def main():
    global commands, entry_command, entry_action, command_list, text_area, main_window

    main_window = tk.Tk()
    main_window.title("Голосовой помощник Ева")
    main_window.geometry("600x400")

    commands = load_commands()

    frame_commands = ttk.Frame(main_window)
    frame_commands.pack(pady=10)

    ttk.Label(frame_commands, text="Команда:").grid(row=0, column=0, padx=5)
    entry_command = ttk.Entry(frame_commands)
    entry_command.grid(row=0, column=1, padx=5)

    ttk.Label(frame_commands, text="Действие:").grid(row=1, column=0, padx=5)
    entry_action = ttk.Entry(frame_commands)
    entry_action.grid(row=1, column=1, padx=5)

    btn_add = ttk.Button(frame_commands, text="Добавить", command=add_command)
    btn_add.grid(row=2, column=0, pady=5, sticky=tk.W + tk.E, columnspan=2)

    btn_delete = ttk.Button(frame_commands, text="Удалить", command=delete_command)
    btn_delete.grid(row=3, column=0, pady=5, sticky=tk.W + tk.E, columnspan=2)

    command_list = tk.Listbox(main_window, width=50)
    command_list.pack(pady=10)
    update_list()

    text_area = tk.Text(main_window, height=5, wrap="word")
    text_area.pack(padx=10, pady=5)

    output_queue = Queue()
    listener_thread = threading.Thread(target=listen_and_process, args=(output_queue, commands))
    listener_thread.start()

    def process_queue():
      try:
          item = output_queue.get(block=False)
          execute_command(item[0], item[1], commands, main_window)
          text_area.insert(tk.END, f"Выполнено: {item}\n")
          text_area.see(tk.END)
      except Empty:
          pass
      main_window.after(100, process_queue)
    main_window.after(100, process_queue)

    main_window.mainloop()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Произошла ошибка:")
        traceback.print_exc()