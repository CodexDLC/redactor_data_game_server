import tkinter as tk
from tkinter import messagebox
from ..core.base_editor import BaseEditor
from ..panels.block_controls import BlockControls
from ..panels.center_panel import CenterPanel
from ..panels.left_panel.universal import UniversalLeftPanel  # Импортируем новую универсальную панель
from ..helpers import utils


class BlockEditor(BaseEditor):
    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_size = 3
        self.tile_size = 50
        self.selected_tile_value = 1

        self.blocks = {}
        self.grid_data = [[1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        self.tile_colors = {
            1: "#888888",  # tile_open
            0: "#000000",  # tile_block
            2: "#ff0000",  # tile_trigger (Красный)
            3: "#ffff00",  # tile_connector (Желтый)
            4: "#00ff00"  # Спавн (Зеленый)
        }

        # Левая панель
        self.left_panel = UniversalLeftPanel(self.left_frame, self, self.blocks, 50, 5, ("Helvetica", 10), 100)
        self.left_panel.pack(fill=tk.BOTH, expand=True)

        self.controls = BlockControls(self.right_frame, self)
        self.controls.pack(fill=tk.BOTH, expand=True)

        self.center_panel = CenterPanel(self.center_frame, self.grid_size, self.tile_size, self.draw_callback,
                                        self.click_callbacks)
        self.center_panel.pack(fill=tk.BOTH, expand=True)

        self.load_all_blocks()
        self.draw_grid()
        self.update_blocks_listbox()

        self.master.bind("<Key>", self.on_key_press)

    def on_key_press(self, event):
        key = event.char
        if self.controls.block_name_entry.focus_get() is not self.controls.block_name_entry:
            if key in "12345":
                tile_value = int(key)
                self.left_panel.tile_type_var.set(tile_value)
                self.selected_tile_value = tile_value
                self.update_border_color()

    @property
    def click_callbacks(self):
        return {
            "left": self.on_left_click,
            "middle": self.on_middle_click,
            "right": self.on_right_click,
        }

    def draw_callback(self, canvas, grid_data, tile_size, tile_colors):
        canvas.delete("all")
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * tile_size
                y1 = row * tile_size
                x2 = x1 + tile_size
                y2 = y1 + tile_size
                fill_color = self.tile_colors[grid_data[row][col]]
                canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill=fill_color)

    def draw_grid(self):
        self.center_panel.draw_grid(self.grid_data, self.tile_colors)

    def update_border_color(self):
        color = self.tile_colors.get(self.selected_tile_value)
        self.center_panel.canvas.config(highlightbackground=color, highlightthickness=3)

    def generate_code(self):
        output_code = utils.generate_code_from_grid(self.grid_data)
        # self.controls.code_output.delete("1.0", tk.END)
        # self.controls.code_output.insert(tk.END, output_code)

    def on_block_select(self, *args):
        selected_index = self.controls.blocks_listbox.curselection()
        if selected_index:
            block_name = self.controls.blocks_listbox.get(selected_index[0])
            self.load_selected_block(block_name)

    def load_selected_block(self, block_name):
        if block_name in self.blocks:
            self.grid_data = [list(row) for row in self.blocks[block_name]]
            self.controls.block_name_var.set(block_name)
            self.draw_grid()
            self.controls.blocks_listbox.selection_clear(0, tk.END)
            self.selected_tile_value = self.grid_data[0][0]
            self.update_border_color()

    def delete_selected_block(self):
        selected_index = self.controls.blocks_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Ошибка", "Сначала выберите блок для удаления.")
            return

        block_name_to_delete = self.controls.blocks_listbox.get(selected_index[0])
        if messagebox.askyesno("Удаление блока", f"Вы уверены, что хотите удалить блок '{block_name_to_delete}'?"):
            success, message = utils.delete_block_from_json(block_name_to_delete)
            if success:
                del self.blocks[block_name_to_delete]
                self.update_blocks_listbox()
                self.grid_data = [[1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
                self.draw_grid()
                self.controls.block_name_var.set("block_")
                messagebox.showinfo("Успех", f"Блок '{block_name_to_delete}' успешно удален.")
            else:
                messagebox.showerror("Ошибка", message)

    def save_all_blocks(self):
        block_name = self.controls.block_name_var.get()
        if not block_name.startswith("block_"):
            messagebox.showerror("Ошибка", "Имя блока должно начинаться с 'block_'")
            return

        self.blocks, _ = utils.load_blocks_from_json()
        self.blocks[block_name] = tuple(tuple(row) for row in self.grid_data)

        success, message = utils.save_blocks_to_json(self.blocks)
        if success:
            messagebox.showinfo("Успех", message)
            self.update_blocks_listbox()
        else:
            messagebox.showerror("Ошибка", message)

    def load_all_blocks(self):
        self.blocks, message = utils.load_blocks_from_json()
        if self.blocks:
            self.update_blocks_listbox()
            messagebox.showinfo("Успех", "Блоки загружены.")
        else:
            messagebox.showinfo("Информация", message)
            self.update_blocks_listbox()

    def update_blocks_listbox(self):
        self.controls.blocks_listbox.delete(0, tk.END)
        for name in sorted(self.blocks.keys()):
            self.controls.blocks_listbox.insert(tk.END, name)